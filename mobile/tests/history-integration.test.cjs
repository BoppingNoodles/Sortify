const assert = require('node:assert/strict');
const { randomUUID } = require('node:crypto');
const { test } = require('node:test');
const React = require('react');
const { create, act } = require('react-test-renderer');
const { loadSource } = require('./load-source.cjs');

global.IS_REACT_ACT_ENVIRONMENT = true;
const theme = loadSource('src/styles/theme.js');
const native = Object.fromEntries([
  'ActivityIndicator', 'FlatList', 'Image', 'RefreshControl', 'ScrollView', 'Text', 'TouchableOpacity', 'View',
].map((name) => [name, name]));
native.StyleSheet = { create: (styles) => styles };
native.useColorScheme = () => 'light';
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
  let scheme = 'light';
  const App = loadSource('App.js', {
    'expo-status-bar': { StatusBar: 'StatusBar' },
    'react-native': { useColorScheme: () => scheme },
    'react-native-safe-area-context': { SafeAreaProvider: 'SafeAreaProvider' },
    '@react-navigation/native': {
      NavigationContainer: 'NavigationContainer',
      DefaultTheme: { dark: false, colors: {} },
      DarkTheme: { dark: true, colors: {} },
    },
    './src/navigation/AppNavigator': 'AppNavigator',
    './src/services/storage': { getOrCreateDeviceUuid },
    './src/styles/theme': theme,
  }).default;

  const renderer = await mount(t, App);
  assert.equal(getOrCreateDeviceUuid.mock.callCount(), 1);
  assert.ok(renderer.root.findByType('AppNavigator'));
  assert.equal(renderer.root.findByType('NavigationContainer').props.theme.dark, false);
  assert.equal(renderer.root.findByType('StatusBar').props.style, 'dark');
  scheme = 'dark';
  await act(async () => { renderer.update(React.createElement(App)); });
  const dark = renderer.root.findByType('NavigationContainer').props.theme;
  assert.equal(dark.dark, true);
  assert.equal(dark.colors.background, theme.getAppColors('dark').background.primary);
  assert.equal(renderer.root.findByType('StatusBar').props.style, 'light');
  assert.equal(getOrCreateDeviceUuid.mock.callCount(), 1);
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
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
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
  const emptyView = await mount(t, () => empty.ListEmptyComponent);
  const labels = emptyView.root.findAllByType('Text').map(({ props }) => props.children);
  assert.ok(labels.includes('No scans yet'));
  assert.ok(labels.includes('Snap an item to start your streak'));
  assert.ok(labels.includes('Scan First Item'));
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
    'expo-file-system': { File: class File { delete() {} } },
    'expo-image-manipulator': {
      ImageManipulator: { manipulate() {} },
      SaveFormat: { JPEG: 'jpeg' },
    },
    '../styles/theme': theme,
  });
  const firstLaunch = openStorage();
  const saved = await firstLaunch.saveScanRecord(classification);
  assert.ok(saved);

  const nextLaunch = openStorage();
  const HistoryScreen = loadSource('src/screens/HistoryScreen.js', {
    'react-native': native,
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
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

test('Profile updates guest streak and points from saved scans on focus', async (t) => {
  const { summarizeScans } = loadSource('src/services/scanStats.js');
  let scans = [];
  let focus;
  const ProfileScreen = loadSource('src/screens/ProfileScreen.js', {
    'react-native': native,
    '@react-navigation/native': { useFocusEffect: (effect) => { focus = effect; } },
    '../styles/theme': theme,
    '../services/scanStats': { summarizeScans },
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
    '../components/DesignPrimitives': { ProgressBar: 'ProgressBar' },
    '../services/storage': { loadSavedScans: async () => scans },
  }).default;

  const renderer = await mount(t, ProfileScreen);
  const labels = () => renderer.root.findAllByType('Text')
    .map(({ props }) => [].concat(props.children).join(''));

  let blur;
  await act(async () => { blur = focus(); });
  assert.ok(labels().includes('0 Days'));
  assert.ok(labels().includes('0'));

  scans = [
    { ...classification, id: 'first', timestamp: new Date().toISOString() },
    { ...classification, id: 'second', timestamp: new Date().toISOString() },
  ];
  await act(async () => { blur(); blur = focus(); });
  assert.ok(labels().includes('1 Day'));
  assert.ok(labels().includes('20'));
  blur();
});
