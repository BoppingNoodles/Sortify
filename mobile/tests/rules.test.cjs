const assert = require('node:assert/strict');
const { test } = require('node:test');
const React = require('react');
const { create, act } = require('react-test-renderer');
const { loadSource } = require('./load-source.cjs');

global.IS_REACT_ACT_ENVIRONMENT = true;
const theme = loadSource('src/styles/theme.js');
const native = Object.fromEntries(['ScrollView', 'Text', 'TouchableOpacity', 'View'].map((name) => [name, name]));
native.StyleSheet = { create: (styles) => styles };
native.useColorScheme = () => 'light';

async function rules(t, api, { useCityPreference = () => React.useState('berkeley'), openURL } = {}) {
  const Screen = loadSource('src/screens/RulesScreen.js', {
    'react-native': { ...native, Linking: { openURL } },
    '@expo/vector-icons': { Ionicons: 'Ionicons' },
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
    '../components/DesignPrimitives': {
      PrimaryButton: ({ children, onPress, disabled }) =>
        React.createElement('PrimaryButton', { onPress, disabled }, children),
    },
    '../services/api': api,
    '../services/municipalities': loadSource('src/services/municipalities.js'),
    '../services/CityPreference': { useCityPreference },
    '../styles/theme': theme,
  }).default;
  let renderer;
  await act(async () => { renderer = create(React.createElement(Screen)); });
  t.after(async () => { await act(async () => renderer.unmount()); });
  const button = () => renderer.root.findByType('PrimaryButton');
  const labels = () => renderer.root.findAllByType('Text')
    .map(({ props }) => React.Children.toArray(props.children).join(''));
  return { button, labels, renderer, Screen };
}

test('Rules waits for a sleeping server before fetching and says so', async (t) => {
  const wake = Promise.withResolvers();
  const fetchLocationRules = t.mock.fn(async () => ({ rules: { compost: ['Food scraps'] } }));
  let awake = false;
  const screen = await rules(t, {
    fetchLocationRules,
    isServerAwake: () => awake,
    wakeServer: () => wake.promise,
  });
  let searching;
  await act(async () => { searching = screen.button().props.onPress(); });
  assert.equal(screen.button().props.children, 'Waking up the server…');
  assert.equal(screen.button().props.disabled, true);
  assert.equal(fetchLocationRules.mock.callCount(), 0);

  awake = true;
  await act(async () => { wake.resolve(true); await searching; });
  assert.equal(fetchLocationRules.mock.callCount(), 1);
  assert.equal(fetchLocationRules.mock.calls[0].arguments[0], 'berkeley');
  assert.equal(screen.button().props.children, 'Search');
  assert.ok(!screen.labels().some((label) => label.startsWith('Could not')));
});

test('Rules opens the official guide for the selected city and hides it after the city changes', async (t) => {
  const source = 'https://www.oaklandrecycles.com/';
  const openURL = t.mock.fn(async () => {});
  let city = 'oakland';
  const screen = await rules(t, {
    fetchLocationRules: async () => ({ rules: { compost: 'Food scraps' }, source_url: source }),
    isServerAwake: () => true,
  }, { useCityPreference: () => [city, () => {}], openURL });
  await act(async () => { await screen.button().props.onPress(); });
  const link = screen.renderer.root.findByProps({ accessibilityRole: 'link' });
  await act(async () => { await link.props.onPress(); });
  assert.equal(openURL.mock.calls[0].arguments[0], source);
  city = 'san-jose';
  await act(async () => { screen.renderer.update(React.createElement(screen.Screen)); });
  assert.equal(screen.renderer.root.findAllByProps({ accessibilityRole: 'link' }).length, 0);
});

test('city preference is shared across screens and survives provider remount', async (t) => {
  const stored = new Map();
  const read = t.mock.fn(async (key) => stored.get(key) ?? null);
  const { CityPreferenceProvider, useCityPreference } = loadSource('src/services/CityPreference.js', {
    '@react-native-async-storage/async-storage': {
      getItem: read,
      setItem: async (key, value) => { stored.set(key, value); },
    },
    './municipalities': loadSource('src/services/municipalities.js'),
  });
  function CityConsumer({ label }) {
    const [city, selectCity] = useCityPreference();
    return React.createElement('CityConsumer', { label, city, selectCity });
  }
  const tree = () => React.createElement(CityPreferenceProvider, null,
    React.createElement(CityConsumer, { label: 'Scan' }),
    React.createElement(CityConsumer, { label: 'Rules' }));
  let renderer;
  await act(async () => { renderer = create(tree()); });
  t.after(async () => { await act(async () => renderer.unmount()); });
  const city = (label) => renderer.root.findAllByType('CityConsumer')
    .find(({ props }) => props.label === label).props;
  assert.equal(city('Scan').city, 'berkeley');
  await act(async () => { city('Rules').selectCity('sunnyvale'); });
  assert.equal(city('Scan').city, 'sunnyvale');
  await act(async () => { renderer.unmount(); renderer = create(tree()); });
  assert.equal(city('Scan').city, 'sunnyvale');
  assert.equal(city('Rules').city, 'sunnyvale');
});

test('Rules reports an unreachable server without fetching', async (t) => {
  const fetchLocationRules = t.mock.fn();
  const screen = await rules(t, {
    fetchLocationRules,
    isServerAwake: () => false,
    wakeServer: async () => false,
  });
  await act(async () => { await screen.button().props.onPress(); });
  assert.equal(fetchLocationRules.mock.callCount(), 0);
  assert.ok(screen.labels().includes(
    'Could not reach the Sortify server. Check your internet connection and try again.'));
  assert.equal(screen.button().props.children, 'Search');
  assert.equal(screen.button().props.disabled, false);
});
