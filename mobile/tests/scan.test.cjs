const assert = require('node:assert/strict');
const { test } = require('node:test');
const React = require('react');
const { create, act } = require('react-test-renderer');
const { loadSource } = require('./load-source.cjs');

global.IS_REACT_ACT_ENVIRONMENT = true;
const theme = loadSource('src/styles/theme.js');
const native = Object.fromEntries([
  'Text', 'View', 'TouchableOpacity', 'Image', 'SafeAreaView', 'ActivityIndicator', 'ScrollView',
].map((name) => [name, name]));
native.StyleSheet = { create: (styles) => styles, absoluteFillObject: {} };

function deferred() {
  let resolve;
  let reject;
  const promise = new Promise((res, rej) => { resolve = res; reject = rej; });
  return { promise, resolve, reject };
}

const predictionFixture = {
  item_name: 'Bottle',
  category: 'plastic',
  confidence: 0.91,
  bin: 'Blue Plastic Bin',
  bin_color: 'Blue',
  disposal_tip: 'Empty and rinse.',
  location: 'san-francisco',
};

async function scan(t, classifyImage, {
  takePictureAsync = async () => ({ uri: 'file:///photo.jpg' }),
  saveScanRecord = async () => ({ id: 'saved' }),
} = {}) {
  const alerts = [];
  const destinations = [];
  const Screen = loadSource('src/screens/ScanScreen.js', {
    'react-native': { ...native, Alert: { alert: (...args) => alerts.push(args) } },
    'expo-camera': { CameraView: 'CameraView', useCameraPermissions: () => [{ granted: true }, () => {}] },
    '../styles/theme': theme,
    '../services/api': { classifyImage },
    '../services/storage': { saveScanRecord },
  }).default;
  let renderer;
  await act(async () => {
    renderer = create(React.createElement(Screen, {
      navigation: { navigate: (...args) => destinations.push(args) },
    }), { createNodeMock: (element) => element.type === 'CameraView' ? { takePictureAsync } : null });
  });
  t.after(async () => { await act(async () => renderer.unmount()); });
  const handler = (name) => renderer.root.findAllByType('TouchableOpacity')
    .find((node) => node.props.onPress.name === name).props.onPress;
  return { renderer, handler, alerts, destinations };
}

test('capture and live scan prevent overlap, map the API contract, and reset preview', async (t) => {
  const photo = deferred();
  const prediction = deferred();
  const pendingSave = deferred();
  const saveStarted = deferred();
  const saveScanRecord = t.mock.fn(() => {
    saveStarted.resolve();
    return pendingSave.promise;
  });
  let captures = 0;
  const requests = [];
  const app = await scan(t, (...args) => { requests.push(args); return prediction.promise; },
    { takePictureAsync: () => { captures++; return photo.promise; }, saveScanRecord });
  await act(async () => { app.handler('handleCycleCity')(); });
  const capture = app.handler('handleCapture');
  let captureTask;
  await act(async () => { captureTask = capture(); await capture(); });
  assert.equal(captures, 1);
  await act(async () => { photo.resolve({ uri: 'file:///photo.jpg' }); await captureTask; });
  const analyze = app.handler('handleAnalyze');
  let analyzeTask;
  await act(async () => { analyzeTask = analyze(); await analyze(); });
  assert.equal(requests.length, 1);
  assert.deepEqual(requests[0], ['file:///photo.jpg', 'san-francisco']);
  assert.equal(app.renderer.root.findAllByType('ActivityIndicator').length, 1);
  await act(async () => {
    prediction.resolve(predictionFixture);
    await saveStarted.promise;
  });
  assert.equal(app.destinations.length, 0);
  await act(async () => { await analyze(); });
  assert.equal(requests.length, 1);
  assert.equal(saveScanRecord.mock.callCount(), 1);
  assert.equal(saveScanRecord.mock.calls[0].arguments[0], predictionFixture);

  await act(async () => { pendingSave.resolve({ id: 'saved' }); await analyzeTask; });
  assert.equal(app.destinations.length, 1);
  const [route, params] = app.destinations[0];
  assert.equal(route, 'ResultModal');
  assert.equal(params.itemName, 'Bottle');
  assert.equal(params.disposalTip, 'Empty and rinse.');
  assert.equal(params.confidence, 0.91);
  assert.equal(params.bin, 'Blue Plastic Bin');
  assert.equal(params.location, 'san-francisco');
  assert.equal(params.photoUri, 'file:///photo.jpg');
  assert.equal(params.historySaved, true);
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
});

test('invalid classification responses retain the photo for a successful retry', async (t) => {
  t.mock.method(console, 'error', () => {});
  const valid = {
    item_name: 'Bottle', category: 'plastic', confidence: 0.91,
    disposal_tip: 'Empty and rinse.', location: 'berkeley',
  };
  const invalid = [
    {},
    { ...valid, item_name: null },
    { ...valid, disposal_tip: null },
    { ...valid, category: 123 },
    { ...valid, category: 'toString' },
    { ...valid, confidence: 1.1 },
    { ...valid, confidence: NaN },
    { ...valid, location: 123 },
    { ...valid, bin: {} },
  ];
  const responses = [...invalid, valid];
  const saveScanRecord = t.mock.fn(async () => ({ id: 'saved' }));
  const app = await scan(t, async () => responses.shift(), { saveScanRecord });
  await act(async () => { await app.handler('handleCapture')(); });
  let analyze = app.handler('handleAnalyze');

  for (let index = 0; index < invalid.length; index++) {
    await act(async () => { await analyze(); });
    assert.equal(app.destinations.length, 0);
    assert.equal(saveScanRecord.mock.callCount(), 0);
    assert.equal(app.renderer.root.findByType('Image').props.source.uri, 'file:///photo.jpg');
    assert.equal(app.alerts[index][1], 'Classification server returned an invalid response.');
    analyze = app.alerts[index][2].find((button) => button.text === 'Try Again').onPress;
  }

  await act(async () => { await analyze(); });
  assert.equal(app.destinations[0][1].category, 'plastic');
  assert.equal(saveScanRecord.mock.callCount(), 1);
  assert.equal(app.destinations[0][1].bin, null);
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
});

test('failed classification supports retry and retake without losing the photo', async (t) => {
  t.mock.method(console, 'error', () => {});
  let requests = 0;
  const app = await scan(t, async () => { requests++; throw new Error('Network disconnected'); });
  await act(async () => { await app.handler('handleCapture')(); });
  await act(async () => { await app.handler('handleAnalyze')(); });
  assert.equal(app.renderer.root.findAllByType('Image').length, 1);
  assert.equal(app.destinations.length, 0);
  await act(async () => { await app.alerts[0][2].find((button) => button.text === 'Try Again').onPress(); });
  assert.equal(requests, 2);
  await act(async () => { app.alerts[1][2].find((button) => button.text === 'Retake').onPress(); });
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
});

test('failed capture unlocks the shutter for another photo', async (t) => {
  t.mock.method(console, 'error', () => {});
  let captures = 0;
  const app = await scan(t, async () => ({}), {
    takePictureAsync: async () => {
      if (++captures === 1) throw new Error('Camera busy');
      return { uri: 'file:///photo.jpg' };
    },
  });
  await act(async () => { await app.handler('handleCapture')(); });
  assert.equal(app.alerts[0][0], 'Camera Error');
  await act(async () => { await app.handler('handleCapture')(); });
  assert.equal(app.renderer.root.findAllByType('Image').length, 1);
});

test('a history save failure still renders the classification with a warning', async (t) => {
  const app = await scan(t, async () => predictionFixture, { saveScanRecord: async () => null });
  await act(async () => { await app.handler('handleCapture')(); });
  await act(async () => { await app.handler('handleAnalyze')(); });

  assert.equal(app.alerts.length, 0);
  assert.equal(app.destinations.length, 1);
  const [, params] = app.destinations[0];
  assert.equal(params.historySaved, false);

  const ResultScreen = loadSource('src/screens/ResultScreen.js', {
    'react-native': native,
    '../styles/theme': theme,
  }).default;
  let renderer;
  await act(async () => {
    renderer = create(React.createElement(ResultScreen, { route: { params } }));
  });
  t.after(async () => { await act(async () => renderer.unmount()); });
  assert.ok(renderer.root.findAllByType('Text').some(({ props }) =>
    props.children === predictionFixture.item_name));
  const warning = renderer.root.findByProps({ accessibilityRole: 'alert' });
  assert.equal(warning.props.children, 'This scan couldn\u2019t be saved to History.');

  await act(async () => {
    renderer.update(React.createElement(ResultScreen, { route: { params: { ...params, historySaved: true } } }));
  });
  assert.equal(renderer.root.findAllByProps({ accessibilityRole: 'alert' }).length, 0);
});

test('result styles use native-compatible category colors for every backend color label', async () => {
  const ResultScreen = loadSource('src/screens/ResultScreen.js', {
    'react-native': native, '../styles/theme': theme,
  }).default;
  for (const [category, binColor] of Object.entries({
    compost: 'Green', plastic: 'Blue', paper: 'Brown', glass: 'Teal', landfill: 'Gray',
  })) {
    let renderer;
    await act(async () => {
      renderer = create(React.createElement(ResultScreen, {
        route: { params: { category, binColor } }, navigation: { goBack() {} },
      }));
    });
    const button = renderer.root.findByType('TouchableOpacity');
    assert.equal(button.props.style[1].backgroundColor, theme.COLORS.bins[category]);
    await act(async () => renderer.unmount());
  }
});
