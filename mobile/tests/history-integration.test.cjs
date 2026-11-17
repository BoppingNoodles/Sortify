const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { test } = require('node:test');
const React = require('react');
const { create, act } = require('react-test-renderer');
const { loadSource } = require('./load-source.cjs');

global.IS_REACT_ACT_ENVIRONMENT = true;
const theme = loadSource('src/styles/theme.js');
const native = Object.fromEntries([
  'ActivityIndicator', 'FlatList', 'Text', 'View',
].map((name) => [name, name]));
native.StyleSheet = { create: (styles) => styles };
const classification = {
  item_name: 'Bottle',
  category: 'plastic',
  confidence: 0.92,
  disposal_tip: 'Empty and rinse.',
  location: 'berkeley',
};

async function mount(t, Screen) {
  let renderer;
  await act(async () => { renderer = create(React.createElement(Screen)); });
  t.after(async () => { await act(async () => renderer.unmount()); });
  return renderer;
}

test('startup initializes guest identity while the navigator renders', async (t) => {
  const pending = Promise.withResolvers();
  const getOrCreateDeviceUuid = t.mock.fn(() => pending.promise);
  const App = loadSource('App.js', {
    'expo-status-bar': { StatusBar: 'StatusBar' },
    'react-native-safe-area-context': { SafeAreaProvider: 'SafeAreaProvider' },
    '@react-navigation/native': { NavigationContainer: 'NavigationContainer' },
    './src/navigation/AppNavigator': 'AppNavigator',
    './src/services/storage': { getOrCreateDeviceUuid },
  }).default;

  const renderer = await mount(t, App);
  assert.equal(getOrCreateDeviceUuid.mock.callCount(), 1);
  assert.ok(renderer.root.findByType('AppNavigator'));
  pending.resolve(null);
});

test('History reloads on focus and ignores reads after leaving the tab', async (t) => {
  const stale = Promise.withResolvers();
  const current = Promise.withResolvers();
  const recentScan = { ...classification, id: 'latest', timestamp: '2026-11-15T18:00:00.000Z' };
  const loadSavedScans = t.mock.fn(async () => []);
  loadSavedScans.mock.mockImplementationOnce(() => stale.promise);
  loadSavedScans.mock.mockImplementationOnce(() => current.promise, 1);

  let focus;
  const HistoryScreen = loadSource('src/screens/HistoryScreen.js', {
    'react-native': native,
    '@react-navigation/native': { useFocusEffect: (effect) => { focus = effect; } },
    '../styles/theme': theme,
    '../services/storage': { loadSavedScans },
  }).default;
  const renderer = await mount(t, HistoryScreen);
  let blur;
  await act(async () => { blur = focus(); });
  assert.ok(renderer.root.findByType('ActivityIndicator'));

  await act(async () => { blur(); blur = focus(); });
  assert.equal(loadSavedScans.mock.callCount(), 2);
  await act(async () => { current.resolve([recentScan]); });
  await act(async () => { stale.resolve([{ ...recentScan, id: 'stale' }]); });

  const { props } = renderer.root.findByType('FlatList');
  assert.deepEqual(props.data, [recentScan]);
  assert.equal(props.keyExtractor(recentScan), recentScan.id);
  const row = await mount(t, () => props.renderItem({ item: recentScan }));
  assert.ok(row.root.findAllByType('Text').some(({ props }) =>
    props.children === new Date(recentScan.timestamp).toLocaleString()));

  await act(async () => { blur(); blur = focus(); });
  assert.equal(loadSavedScans.mock.callCount(), 3);
  const empty = renderer.root.findByType('FlatList').props;
  assert.equal(empty.data.length, 0);
  assert.equal(empty.ListEmptyComponent.props.children, 'No scans yet.');
  blur();
});

test('History displays saved scan metadata after a simulated app relaunch', async (t) => {
  const persisted = new Map();
  const asyncStorage = {
    getItem: async (key) => persisted.get(key) ?? null,
    setItem: async (key, value) => { persisted.set(key, value); },
  };
  const openStorage = () => loadSource('src/services/storage.js', {
    '@react-native-async-storage/async-storage': asyncStorage,
    'expo-crypto': { randomUUID },
    '../styles/theme': theme,
  });
  const firstLaunch = openStorage();
  const saved = await firstLaunch.saveScanRecord(classification);
  assert.ok(saved);

  const nextLaunch = openStorage();
  const HistoryScreen = loadSource('src/screens/HistoryScreen.js', {
    'react-native': native,
    '@react-navigation/native': { useFocusEffect: (effect) => React.useEffect(effect, [effect]) },
    '../styles/theme': theme,
    '../services/storage': nextLaunch,
  }).default;
  const renderer = await mount(t, HistoryScreen);
  const { data, renderItem } = renderer.root.findByType('FlatList').props;
  assert.equal(data.length, 1);
  assert.deepEqual({ ...data[0] }, { ...saved });
  const row = await mount(t, () => renderItem({ item: data[0] }));
  assert.ok(row.root.findAllByType('Text').some(({ props }) =>
    props.children === classification.item_name));
});
