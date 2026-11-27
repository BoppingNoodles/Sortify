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
native.useColorScheme = () => 'light';

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
  readPermission = async () => ({ granted: true }),
  requestPermission = readPermission,
  openSettings = async () => {},
  startReady = true,
  platform = 'android',
  impactAsync = async () => {},
  notificationAsync = async () => {},
  stopCamera = null,
  isServerAwake = () => true,
  wakeServer = async () => true,
  announceForAccessibility = () => {},
} = {}) {
  const alerts = [];
  const destinations = [];
  let focusEffect;
  let leave;
  let onAppStateChange;
  const appState = {
    currentState: 'active',
    addEventListener: (_event, listener) => {
      onAppStateChange = listener;
      return { remove: () => { onAppStateChange = null; } };
    },
  };
  const Screen = loadSource('src/screens/ScanScreen.js', {
    'react-native': { ...native, Platform: { OS: platform }, AppState: appState, Linking: { openSettings },
      AccessibilityInfo: { announceForAccessibility },
      findNodeHandle: (camera) => camera.nativeTag,
      Alert: { alert: (...args) => alerts.push(args) } },
    expo: { requireOptionalNativeModule: () => stopCamera && { stop: stopCamera } },
    '@react-navigation/native': { useFocusEffect: (effect) => React.useEffect(() => {
      focusEffect = effect;
      leave = effect();
      return () => leave?.();
    }, [effect]) },
    'expo-camera': {
      CameraView: 'CameraView',
      Camera: {
        getCameraPermissionsAsync: readPermission,
        requestCameraPermissionsAsync: requestPermission,
      },
    },
    'expo-haptics': {
      impactAsync,
      notificationAsync,
      ImpactFeedbackStyle: { Medium: 'medium' },
      NotificationFeedbackType: { Success: 'success', Warning: 'warning' },
    },
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
    '../styles/theme': theme,
    '../services/api': { classifyImage, isServerAwake, wakeServer },
    '../services/storage': { saveScanRecord },
    '../services/municipalities': loadSource('src/services/municipalities.js'),
    '../services/CityPreference': { useCityPreference: () => React.useState('berkeley') },
    '../services/confidence': loadSource('src/services/confidence.js'),
  }).default;
  let renderer;
  await act(async () => {
    renderer = create(React.createElement(Screen, {
      navigation: { navigate: (...args) => destinations.push(args) },
    }), { createNodeMock: (element) => element.type === 'CameraView' ? { takePictureAsync, nativeTag: 42 } : null });
  });
  t.after(async () => { await act(async () => renderer.unmount()); });
  const cameraReady = () => act(async () => {
    renderer.root.findAllByType('CameraView')[0]?.props.onCameraReady?.();
  });
  if (startReady) await cameraReady();
  const handler = (name) => renderer.root.findAllByType('TouchableOpacity')
    .find((node) => node.props.onPress.name === name).props.onPress;
  return {
    renderer, handler, alerts, destinations, cameraReady,
    focus: () => act(async () => { leave = focusEffect(); }),
    blur: () => act(async () => { leave(); leave = null; }),
    setAppState: (state) => act(async () => {
      appState.currentState = state;
      onAppStateChange(state);
    }),
  };
}

test('camera and preview keep controls in safe-area overlays', async (t) => {
  const app = await scan(t, async () => predictionFixture);
  const camera = app.renderer.root.findByType('CameraView');
  const overlay = app.renderer.root.findByType('SafeAreaView');
  assert.equal(camera.parent, overlay.parent);
  assert.equal(camera.children.length, 0);
  assert.deepEqual(Array.from(overlay.props.edges), ['top', 'left', 'right']);
  assert.ok(overlay.findByProps({ accessibilityLabel: 'Take photo' }));

  await act(async () => { await app.handler('handleCapture')(); });
  const preview = app.renderer.root.findByType('SafeAreaView');
  assert.deepEqual(Array.from(preview.props.edges), ['left', 'right']);
  assert.deepEqual(preview.findAllByType('Text').map(({ props }) => props.children),
    ['Retake', 'Identify Bin']);
});

test('shutter feedback runs once per capture and result feedback follows a valid result', async (t) => {
  const takingPhoto = deferred();
  const impactAsync = t.mock.fn(async () => { throw new Error('Feedback unavailable'); });
  const notificationAsync = t.mock.fn(async () => { throw new Error('Feedback unavailable'); });
  const classifyImage = t.mock.fn(async () => predictionFixture);
  classifyImage.mock.mockImplementationOnce(async () => null);
  const app = await scan(t, classifyImage, {
    impactAsync,
    notificationAsync,
    takePictureAsync: () => takingPhoto.promise,
  });
  const shutter = app.handler('handleCapture');
  let capture;
  await act(async () => {
    capture = shutter();
    await shutter();
  });
  assert.equal(impactAsync.mock.callCount(), 1);
  assert.equal(impactAsync.mock.calls[0].arguments[0], 'medium');
  assert.equal(notificationAsync.mock.callCount(), 0);
  await act(async () => {
    takingPhoto.resolve({ uri: 'file:///photo.jpg' });
    await capture;
  });
  await act(async () => { await app.handler('handleAnalyze')(); });
  assert.equal(notificationAsync.mock.callCount(), 0);
  await act(async () => { await app.handler('handleAnalyze')(); });
  assert.equal(notificationAsync.mock.callCount(), 1);
  assert.equal(notificationAsync.mock.calls[0].arguments[0], 'success');
  assert.equal(app.destinations.length, 1);
});

test('iOS plays shutter feedback only after native camera shutdown', async (t) => {
  const stopping = deferred();
  const stopCamera = t.mock.fn(() => stopping.promise);
  const impactAsync = t.mock.fn(async () => {});
  const app = await scan(t, async () => predictionFixture, {
    platform: 'ios', impactAsync, stopCamera,
  });
  let capture;
  await act(async () => { capture = app.handler('handleCapture')(); });
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
  assert.equal(stopCamera.mock.callCount(), 1);
  assert.equal(stopCamera.mock.calls[0].arguments[0], 42);
  assert.equal(impactAsync.mock.callCount(), 0);
  await act(async () => {
    stopping.resolve(true);
    await capture;
  });
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 0);
  assert.equal(impactAsync.mock.callCount(), 1);
  assert.equal(impactAsync.mock.calls[0].arguments[0], 'medium');
});

test('iOS suppresses a pending shutter pulse after leaving Scan', async (t) => {
  const stopping = deferred();
  const impactAsync = t.mock.fn(async () => {});
  const app = await scan(t, async () => predictionFixture, {
    platform: 'ios', impactAsync, stopCamera: () => stopping.promise,
  });
  let capture;
  await act(async () => { capture = app.handler('handleCapture')(); });
  await app.blur();
  await act(async () => {
    stopping.resolve(true);
    await capture;
  });
  assert.equal(impactAsync.mock.callCount(), 0);
  assert.equal(app.renderer.root.findAllByType('Image').length, 0);
});

test('iOS opens the photo preview when native camera shutdown cannot be confirmed', async (t) => {
  const impactAsync = t.mock.fn(async () => {});
  const app = await scan(t, async () => predictionFixture, { platform: 'ios', impactAsync });
  await act(async () => { await app.handler('handleCapture')(); });
  assert.equal(app.renderer.root.findAllByType('Image').length, 1);
  assert.equal(impactAsync.mock.callCount(), 0);
});

test('requestable denial can grant access from the scan screen', async (t) => {
  const requestPermission = t.mock.fn(async () => ({ granted: true }));
  const app = await scan(t, async () => predictionFixture, {
    readPermission: async () => ({ granted: false, canAskAgain: true }),
    requestPermission,
  });
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 0);
  const grant = app.renderer.root.findByType('TouchableOpacity');
  assert.equal(grant.findByType('Text').props.children, 'Grant Permission');
  await act(async () => { await grant.props.onPress(); });
  assert.equal(requestPermission.mock.callCount(), 1);
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
});

test('permanent denial opens Settings, reports a failure, and refreshes on return', async (t) => {
  let permission = { granted: false, canAskAgain: false };
  const requestPermission = t.mock.fn();
  const openSettings = t.mock.fn(async () => {});
  openSettings.mock.mockImplementationOnce(async () => { throw new Error('unavailable'); });
  const app = await scan(t, async () => predictionFixture, {
    readPermission: async () => permission, requestPermission, openSettings,
  });
  const button = app.renderer.root.findByType('TouchableOpacity');
  assert.equal(button.findByType('Text').props.children, 'Open Settings');
  await act(async () => { await button.props.onPress(); });
  assert.match(app.renderer.root.findByProps({ accessibilityRole: 'alert' }).props.children, /manually/);
  await act(async () => { await button.props.onPress(); });
  assert.equal(openSettings.mock.callCount(), 2);
  assert.equal(requestPermission.mock.callCount(), 0);

  await app.setAppState('background');
  permission = { granted: true };
  await app.setAppState('active');
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
});

test('late Settings failure does not overwrite a newer foreground permission state', async (t) => {
  const settings = deferred();
  let permission = { granted: false, canAskAgain: false };
  const app = await scan(t, async () => predictionFixture, {
    readPermission: async () => permission,
    openSettings: () => settings.promise,
  });
  let open;
  await act(async () => { open = app.handler('handlePermission')(); });
  await app.setAppState('background');
  permission = { granted: false, canAskAgain: true };
  await app.setAppState('active');
  await act(async () => { settings.reject(new Error('old Settings failure')); await open; });
  const button = app.renderer.root.findByType('TouchableOpacity');
  assert.equal(button.findByType('Text').props.children, 'Grant Permission');
  assert.equal(app.renderer.root.findAllByProps({ accessibilityRole: 'alert' }).length, 0);
});

test('returning during a native request waits for the permanent-denial decision', async (t) => {
  const request = deferred();
  let permission = { granted: false, canAskAgain: true };
  const readPermission = t.mock.fn(async () => permission);
  const app = await scan(t, async () => predictionFixture, {
    readPermission,
    requestPermission: () => request.promise,
  });
  let pending;
  await act(async () => { pending = app.handler('handlePermission')(); });
  await app.setAppState('background');
  await app.setAppState('active');
  assert.equal(readPermission.mock.callCount(), 1);
  assert.equal(app.renderer.root.findAllByType('TouchableOpacity').length, 0);
  permission = { granted: false, canAskAgain: false };
  await act(async () => { request.resolve(permission); await pending; });
  const button = app.renderer.root.findByType('TouchableOpacity');
  assert.equal(button.findByType('Text').props.children, 'Open Settings');
});

test('capture waits for readiness from each new camera preview', async (t) => {
  const takePictureAsync = t.mock.fn(async () => ({ uri: 'file:///photo.jpg' }));
  const app = await scan(t, async () => predictionFixture, { takePictureAsync, startReady: false });
  const shutter = () => app.renderer.root.findAllByType('TouchableOpacity')
    .find(({ props }) => props.onPress.name === 'handleCapture').props;
  const assertWaiting = async () => {
    assert.equal(shutter().disabled, true);
    await act(async () => { await shutter().onPress(); });
    assert.equal(takePictureAsync.mock.callCount(), 0);
  };

  await assertWaiting();
  const firstReady = app.renderer.root.findByType('CameraView').props.onCameraReady;
  await app.cameraReady();
  assert.equal(shutter().disabled, false);

  await app.blur();
  await app.focus();
  await act(async () => { firstReady(); });
  await assertWaiting();
  await app.cameraReady();
  assert.equal(shutter().disabled, false);

  await app.setAppState('background');
  await app.setAppState('active');
  await assertWaiting();
  await app.cameraReady();
  await act(async () => { await shutter().onPress(); });
  assert.equal(takePictureAsync.mock.callCount(), 1);
  assert.equal(app.renderer.root.findAllByType('Image').length, 1);
  await act(async () => { app.handler('handleRetake')(); });
  assert.equal(shutter().disabled, true);
});

test('refocus can take a new photo while a detached camera capture remains pending', async (t) => {
  const oldPhoto = deferred();
  const newPhoto = deferred();
  const captures = [oldPhoto.promise, newPhoto.promise];
  const takePictureAsync = t.mock.fn(() => captures.shift());
  const app = await scan(t, async () => predictionFixture, { takePictureAsync });
  let oldCapture;
  await act(async () => { oldCapture = app.handler('handleCapture')(); });

  await app.blur();
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 0);
  await app.focus();
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
  await app.cameraReady();
  let newCapture;
  await act(async () => { newCapture = app.handler('handleCapture')(); });
  assert.equal(takePictureAsync.mock.callCount(), 2);

  await act(async () => { oldPhoto.resolve({ uri: 'file:///obsolete.jpg' }); await oldCapture; });
  assert.equal(app.renderer.root.findAllByType('Image').length, 0);
  await act(async () => { await app.handler('handleCapture')(); });
  assert.equal(takePictureAsync.mock.callCount(), 2);

  await act(async () => { newPhoto.resolve({ uri: 'file:///current.jpg' }); await newCapture; });
  assert.equal(app.renderer.root.findByType('Image').props.source.uri, 'file:///current.jpg');
});

test('backgrounding drops stale analysis, preserves the preview, and allows explicit retry', async (t) => {
  const prediction = deferred();
  const classifyImage = t.mock.fn(() => prediction.promise);
  const saveScanRecord = t.mock.fn(async () => ({ id: 'saved' }));
  const app = await scan(t, classifyImage, { saveScanRecord });

  await app.setAppState('background');
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 0);
  await app.setAppState('active');
  await app.cameraReady();
  await act(async () => { await app.handler('handleCapture')(); });
  let analyze;
  await act(async () => { analyze = app.handler('handleAnalyze')(); });
  await app.setAppState('inactive');
  await app.setAppState('active');
  assert.equal(app.renderer.root.findAllByType('ActivityIndicator').length, 0);
  await act(async () => { await app.handler('handleAnalyze')(); });
  assert.equal(classifyImage.mock.callCount(), 1);

  await act(async () => { prediction.resolve(predictionFixture); await analyze; });
  assert.equal(app.destinations.length, 0);
  assert.equal(saveScanRecord.mock.callCount(), 0);
  assert.equal(app.renderer.root.findAllByType('Image').length, 1);
  await act(async () => { await app.handler('handleAnalyze')(); });
  assert.equal(saveScanRecord.mock.callCount(), 1);
  assert.equal(app.destinations.length, 1);
});

test('leaving during an in-flight save suppresses the modal and ends that preview', async (t) => {
  const pendingSave = deferred();
  const saveStarted = deferred();
  const saveScanRecord = t.mock.fn(() => {
    saveStarted.resolve();
    return pendingSave.promise;
  });
  const app = await scan(t, async () => predictionFixture, { saveScanRecord });
  await act(async () => { await app.handler('handleCapture')(); });
  let analyze;
  await act(async () => { analyze = app.handler('handleAnalyze')(); await saveStarted.promise; });

  await app.blur();
  await act(async () => { pendingSave.resolve({ id: 'saved' }); await analyze; });
  assert.equal(app.destinations.length, 0);
  assert.equal(saveScanRecord.mock.callCount(), 1);
  await app.focus();
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
  await app.cameraReady();
  const shutter = app.renderer.root.findAllByType('TouchableOpacity')
    .find(({ props }) => props.onPress.name === 'handleCapture');
  assert.equal(shutter.props.disabled, false);
});

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
    prediction.resolve({ ...predictionFixture, disposal_tips: { notes: 'San Francisco accepts empty rigid bottles.' } });
    await saveStarted.promise;
  });
  assert.equal(app.destinations.length, 0);
  await act(async () => { await analyze(); });
  assert.equal(requests.length, 1);
  assert.equal(saveScanRecord.mock.callCount(), 1);
  assert.equal(saveScanRecord.mock.calls[0].arguments[0].disposal_tip, 'San Francisco accepts empty rigid bottles.');

  await act(async () => { pendingSave.resolve({ id: 'saved' }); await analyzeTask; });
  assert.equal(app.destinations.length, 1);
  const [route, params] = app.destinations[0];
  assert.equal(route, 'ResultModal');
  assert.equal(params.itemName, 'Bottle');
  assert.equal(params.disposalTip, 'San Francisco accepts empty rigid bottles.');
  assert.equal(params.confidence, 0.91);
  assert.equal(params.bin, 'Blue Plastic Bin');
  assert.equal(params.location, 'san-francisco');
  assert.equal(params.photoUri, 'file:///photo.jpg');
  assert.equal(params.historySaved, true);
  assert.equal(params.uncertain, false);
  assert.equal(app.renderer.root.findAllByType('CameraView').length, 1);
});

test('a sleeping server is woken before upload with a visible waiting message', async (t) => {
  const wake = deferred();
  let awake = false;
  const wakeServer = t.mock.fn(() => wake.promise);
  const requests = [];
  const app = await scan(t, async (...args) => { requests.push(args); return predictionFixture; }, {
    isServerAwake: () => awake,
    wakeServer,
  });
  await act(async () => { await app.handler('handleCapture')(); });
  let analyzeTask;
  await act(async () => { analyzeTask = app.handler('handleAnalyze')(); });

  const labels = () => app.renderer.root.findAllByType('Text')
    .map(({ props }) => React.Children.toArray(props.children).join(''));
  assert.equal(wakeServer.mock.callCount(), 1);
  assert.equal(requests.length, 0);
  assert.ok(labels().includes('Waking up the server…'));

  awake = true;
  await act(async () => { wake.resolve(true); await analyzeTask; });
  assert.equal(requests.length, 1);
  assert.equal(app.destinations.length, 1);
  assert.equal(app.destinations[0][0], 'ResultModal');
  assert.ok(!labels().includes('Waking up the server…'));
});

test('leaving during wake-up releases the preview instead of leaving it disabled', async (t) => {
  const wake = deferred();
  const classifyImage = t.mock.fn(async () => predictionFixture);
  const announceForAccessibility = t.mock.fn();
  const app = await scan(t, classifyImage, {
    isServerAwake: () => false,
    wakeServer: () => wake.promise,
    announceForAccessibility,
  });
  await act(async () => { await app.handler('handleCapture')(); });
  let analyzeTask;
  await act(async () => { analyzeTask = app.handler('handleAnalyze')(); });
  assert.equal(announceForAccessibility.mock.callCount(), 1);
  assert.match(announceForAccessibility.mock.calls[0].arguments[0], /Waking up the server/);
  assert.equal(app.renderer.root.findAllByType('View')
    .filter(({ props }) => props.accessibilityLiveRegion === 'polite').length, 1);

  await app.setAppState('background');
  await app.setAppState('active');
  const buttons = app.renderer.root.findAllByType('TouchableOpacity');
  const retake = buttons.find(({ props }) => props.onPress.name === 'handleRetake');
  const identify = buttons.find(({ props }) => props.onPress.name === 'handleAnalyze');
  assert.equal(retake.props.disabled, false);
  assert.equal(identify.props.disabled, false);

  // The abandoned wake finishing later must not upload, alert or relock the preview.
  await act(async () => { wake.resolve(true); await analyzeTask; });
  assert.equal(classifyImage.mock.callCount(), 0);
  assert.equal(app.alerts.length, 0);
  assert.equal(app.destinations.length, 0);
  assert.equal(app.renderer.root.findAllByType('TouchableOpacity')
    .find(({ props }) => props.onPress.name === 'handleAnalyze').props.disabled, false);
});

test('an unreachable server fails fast with a retryable alert and no upload', async (t) => {
  const classifyImage = t.mock.fn(async () => predictionFixture);
  const app = await scan(t, classifyImage, {
    isServerAwake: () => false,
    wakeServer: async () => false,
  });
  await act(async () => { await app.handler('handleCapture')(); });
  await act(async () => { await app.handler('handleAnalyze')(); });

  assert.equal(classifyImage.mock.callCount(), 0);
  assert.equal(app.destinations.length, 0);
  assert.equal(app.alerts.length, 1);
  assert.equal(app.alerts[0][0], 'Scan Failed');
  assert.match(app.alerts[0][1], /Could not reach the Sortify server/);
  assert.equal(app.alerts[0][2].map(({ text }) => text).join(','), 'Retake,Try Again');
  // The photo is kept so Try Again can retry the same scan.
  assert.equal(app.renderer.root.findAllByType('Image').length, 1);
});

test('a low-confidence result opens as not sure and is kept out of History', async (t) => {
  const saveScanRecord = t.mock.fn(async () => ({ id: 'saved' }));
  const notificationAsync = t.mock.fn(async () => {});
  const lowConfidence = {
    ...predictionFixture,
    confidence: 0.52,
    alternatives: [{ category: 'paper', confidence: 0.3 }],
  };
  const app = await scan(t, async () => lowConfidence, { saveScanRecord, notificationAsync });
  await act(async () => { await app.handler('handleCapture')(); });
  await act(async () => { await app.handler('handleAnalyze')(); });

  assert.equal(saveScanRecord.mock.callCount(), 0);
  assert.equal(app.destinations.length, 1);
  const [route, params] = app.destinations[0];
  assert.equal(route, 'ResultModal');
  assert.equal(params.uncertain, true);
  assert.equal(params.historySaved, null);
  assert.equal(params.confidence, 0.52);
  assert.equal(params.category, 'plastic');
  assert.equal(notificationAsync.mock.calls[0].arguments[0], 'warning');
  // The preview resets so Retake Photo returns to a live camera.
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
    const badge = renderer.root.findAllByType('Text')
      .find(({ props }) => props.children === category.toUpperCase()).parent;
    assert.equal(badge.props.style[1].backgroundColor, theme.COLORS.bins[category]);
    assert.equal(renderer.root.findByType('TouchableOpacity').props.style.backgroundColor, theme.COLORS.design.green);
    await act(async () => renderer.unmount());
  }
});

test('result item name and background follow the current appearance', async (t) => {
  let scheme = 'dark';
  const ResultScreen = loadSource('src/screens/ResultScreen.js', {
    'react-native': { ...native, useColorScheme: () => scheme },
    '../styles/theme': theme,
  }).default;
  const itemName = 'Bottle';
  const screenProps = { route: { params: { itemName } } };
  let renderer;
  await act(async () => {
    renderer = create(React.createElement(ResultScreen, screenProps));
  });
  t.after(async () => { await act(async () => renderer.unmount()); });

  const checkColors = () => {
    const colors = theme.getAppColors(scheme);
    const item = renderer.root.findAllByType('Text')
      .find(({ props }) => props.children === itemName);
    assert.equal(renderer.root.findByType('ScrollView').props.style.backgroundColor, colors.background.primary);
    assert.equal(item.props.style.color, colors.text.primary);
  };

  checkColors();
  scheme = 'light';
  await act(async () => { renderer.update(React.createElement(ResultScreen, screenProps)); });
  checkColors();
});

test('result bounds confidence and displays the backend disposal guidance', async () => {
  const ResultScreen = loadSource('src/screens/ResultScreen.js', {
    'react-native': native,
    '../styles/theme': theme,
  }).default;
  const params = {
    category: 'paper',
    bin: 'Blue Paper Bin',
    location: 'san-francisco',
    disposalTip: 'Keep paper dry.',
  };
  for (const [confidence, expected] of [[1.2, 100], [-0.2, 0], ['0.75', 75], ['invalid', 0]]) {
    let renderer;
    await act(async () => {
      renderer = create(React.createElement(ResultScreen, {
        route: { params: { ...params, confidence } },
      }));
    });
    try {
      const labels = renderer.root.findAllByType('Text')
        .map(({ props }) => React.Children.toArray(props.children).join(''));
      assert.ok(labels.includes(expected + '%'));
      assert.ok(labels.includes('Target: Blue Paper Bin'));
      assert.ok(labels.includes('Disposal Guideline (San Francisco 📍)'));
      assert.ok(labels.includes('Keep paper dry.'));
    } finally {
      await act(async () => renderer.unmount());
    }
  }
});

test('confidence cutoff flags results strictly below 0.60', () => {
  const { isUncertain, UNCERTAIN_BELOW } = loadSource('src/services/confidence.js');
  assert.equal(UNCERTAIN_BELOW, 0.6);
  assert.equal(isUncertain(0.6), false);
  assert.equal(isUncertain(0.95), false);
  assert.equal(isUncertain(0.5999), true);
  assert.equal(isUncertain(0), true);
  assert.equal(isUncertain(Number.NaN), true);
  assert.equal(isUncertain(undefined), true);
});

test('not-sure result shows the best guess, alternatives and a retake path', async (t) => {
  const ResultScreen = loadSource('src/screens/ResultScreen.js', {
    'react-native': native,
    '../styles/theme': theme,
  }).default;
  let wentBack = 0;
  let renderer;
  await act(async () => {
    renderer = create(React.createElement(ResultScreen, {
      route: { params: {
        itemName: 'Plastic',
        category: 'plastic',
        confidence: 0.52,
        bin: 'Blue Recycling Bin',
        location: 'san-jose',
        disposalTip: 'Rinse before recycling.',
        alternatives: [{ category: 'paper', confidence: 0.3 }, { category: 'landfill', confidence: 0.1 }],
        uncertain: true,
        historySaved: null,
      } },
      navigation: { goBack: () => { wentBack++; } },
    }));
  });
  t.after(async () => { await act(async () => renderer.unmount()); });
  const labels = renderer.root.findAllByType('Text')
    .map(({ props }) => React.Children.toArray(props.children).join(''));
  assert.ok(labels.includes('NOT SURE'));
  assert.ok(labels.includes('Not sure what this is'));
  assert.ok(labels.includes('Best guess: Plastic, but the confidence is too low to trust.'));
  assert.ok(labels.includes('Could also be: Paper 30%, Landfill 10%'));
  assert.ok(labels.includes('52%'));
  assert.ok(labels.includes('If it is Plastic (San Jose 📍)'));
  assert.ok(labels.includes('Rinse before recycling.'));
  assert.ok(labels.includes('Not added to History.'));
  assert.ok(labels.includes('Retake Photo'));
  assert.ok(!labels.includes('PLASTIC'));
  assert.ok(!labels.some((label) => label.startsWith('Target:')));
  assert.ok(!labels.some((label) => label.includes('be saved to History')));
  const badge = renderer.root.findAllByType('Text').find(({ props }) => props.children === 'NOT SURE').parent;
  assert.equal(badge.props.style[1].backgroundColor, theme.COLORS.design.streak);
  await act(async () => { renderer.root.findByType('TouchableOpacity').props.onPress(); });
  assert.equal(wentBack, 1);
});

test('confident results keep the normal layout', async (t) => {
  const ResultScreen = loadSource('src/screens/ResultScreen.js', {
    'react-native': native,
    '../styles/theme': theme,
  }).default;
  let renderer;
  await act(async () => {
    renderer = create(React.createElement(ResultScreen, {
      route: { params: { category: 'glass', confidence: 0.9, uncertain: false, bin: 'Blue Bin' } },
    }));
  });
  t.after(async () => { await act(async () => renderer.unmount()); });
  const labels = renderer.root.findAllByType('Text')
    .map(({ props }) => React.Children.toArray(props.children).join(''));
  assert.ok(labels.includes('GLASS'));
  assert.ok(labels.includes('Target: Blue Bin'));
  assert.ok(labels.includes('Scan Another Item'));
  assert.ok(!labels.includes('NOT SURE'));
  assert.ok(!labels.includes('Not added to History.'));
});
