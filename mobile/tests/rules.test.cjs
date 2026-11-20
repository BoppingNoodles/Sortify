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

async function rules(t, api) {
  const Screen = loadSource('src/screens/RulesScreen.js', {
    'react-native': native,
    '@expo/vector-icons': { Ionicons: 'Ionicons' },
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
    '../components/DesignPrimitives': {
      PrimaryButton: ({ children, onPress, disabled }) =>
        React.createElement('PrimaryButton', { onPress, disabled }, children),
    },
    '../services/api': api,
    '../services/municipalities': loadSource('src/services/municipalities.js'),
    '../styles/theme': theme,
  }).default;
  let renderer;
  await act(async () => { renderer = create(React.createElement(Screen)); });
  t.after(async () => { await act(async () => renderer.unmount()); });
  const button = () => renderer.root.findByType('PrimaryButton');
  const labels = () => renderer.root.findAllByType('Text')
    .map(({ props }) => React.Children.toArray(props.children).join(''));
  return { button, labels };
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
