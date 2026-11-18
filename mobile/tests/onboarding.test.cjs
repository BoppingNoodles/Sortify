const assert = require('node:assert/strict');
const { test } = require('node:test');
const React = require('react');
const { create, act } = require('react-test-renderer');
const { loadSource } = require('./load-source.cjs');

global.IS_REACT_ACT_ENVIRONMENT = true;

async function renderOnboarding(t, beforeWrite = () => {}) {
  const values = new Map();
  const storage = loadSource('src/services/storage.js', {
    '@react-native-async-storage/async-storage': {
      getItem: async (key) => values.get(key) ?? null,
      setItem: async (key, value) => {
        await beforeWrite();
        values.set(key, value);
      },
    },
    'expo-crypto': {},
    'expo-file-system': {},
    'expo-image-manipulator': {},
    '../styles/theme': loadSource('src/styles/theme.js'),
  });
  const native = {
    View: 'View', Text: 'Text', Pressable: 'Pressable',
    ScrollView: 'ScrollView', ActivityIndicator: 'ActivityIndicator',
    useColorScheme: () => 'light',
    StyleSheet: { create: (styles) => styles },
    PanResponder: { create: (handlers) => ({ panHandlers: handlers }) },
  };
  const theme = loadSource('src/styles/theme.js');
  const OnboardingScreen = loadSource('src/screens/OnboardingScreen.js', {
    'react-native': native,
    '@expo/vector-icons': { Ionicons: 'Ionicons' },
    '@react-navigation/native': { useTheme: () => ({ colors: { text: '#111', border: '#ddd' } }) },
    '../components/DesignPrimitives': { PrimaryButton: 'PrimaryButton' },
  }).default;
  const WelcomeScreen = loadSource('src/screens/WelcomeScreen.js', {
    'react-native': native,
    'react-native-safe-area-context': { SafeAreaView: 'SafeAreaView' },
    '../components/DesignPrimitives': { PrimaryButton: 'PrimaryButton' },
    '../styles/theme': theme,
    './OnboardingScreen': OnboardingScreen,
  }).default;
  const replace = t.mock.fn((destination) => {
    assert.equal(destination, 'MainTabs');
    return values.get('@sortify_guest_welcome');
  });
  const AppNavigator = loadSource('src/navigation/AppNavigator.js', {
    'react-native': native,
    '@react-navigation/bottom-tabs': { createBottomTabNavigator: () => ({}) },
    '@react-navigation/native-stack': { createNativeStackNavigator: () => ({
      Screen: 'Screen',
      Navigator: ({ initialRouteName, children }) => {
        if (initialRouteName === 'MainTabs') return React.createElement('MainTabs');
        const route = React.Children.toArray(children).find(({ props }) => props.name === initialRouteName);
        return React.createElement(route.props.component, { navigation: { replace } });
      },
    }) },
    '@expo/vector-icons': {},
    '../screens/HomeScreen': 'HomeScreen',
    '../screens/ScanScreen': 'ScanScreen',
    '../screens/HistoryScreen': 'HistoryScreen',
    '../screens/ProfileScreen': 'ProfileScreen',
    '../screens/ResultScreen': 'ResultScreen',
    '../screens/StatsScreen': 'StatsScreen',
    '../screens/RulesScreen': 'RulesScreen',
    '../screens/WelcomeScreen': WelcomeScreen,
    '../services/storage': storage,
    '../styles/theme': theme,
  }).default;

  let renderer;
  t.after(async () => { await act(async () => renderer.unmount()); });
  const app = React.createElement(AppNavigator);
  await act(async () => { renderer = create(app); });
  async function relaunch() {
    await act(async () => { renderer.update(null); });
    await act(async () => { renderer.update(app); });
  }
  return { renderer, replace, relaunch };
}

async function goToFinalSlide(renderer) {
  for (let page = 0; page < 2; page += 1) {
    await act(async () => { renderer.root.findByType('PrimaryButton').props.onPress(); });
  }
}

test('first launch offers three swipeable slides and remembers completion', async (t) => {
  const { renderer, replace, relaunch } = await renderOnboarding(t);
  const heading = () => renderer.root.findByProps({ accessibilityRole: 'header' }).props.children;
  assert.equal(heading(), 'Snap your waste');
  const gesture = renderer.root.findAllByType('View')
    .find(({ props }) => props.onPanResponderRelease).props;
  assert.equal(gesture.onMoveShouldSetPanResponder(null, { dx: -80, dy: 3 }), true);
  assert.equal(gesture.onMoveShouldSetPanResponder(null, { dx: -20, dy: 80 }), false);
  await act(async () => { gesture.onPanResponderRelease(null, { dx: -80 }); });
  assert.equal(heading(), 'Get local guidance');
  await act(async () => { renderer.root.findByType('Pressable').props.onPress(); });
  assert.equal(heading(), 'Snap your waste');
  await goToFinalSlide(renderer);
  assert.equal(heading(), 'Build sorting streaks');
  const finish = renderer.root.findByType('PrimaryButton').props.onPress;
  await act(async () => { await Promise.all([finish(), finish()]); });
  assert.equal(replace.mock.callCount(), 1);
  assert.equal(replace.mock.calls[0].result, 'seen');
  await relaunch();
  assert.ok(renderer.root.findByType('MainTabs'));
});

test('a failed completion write leaves onboarding open and a retry saves before entering Home', async (t) => {
  let writes = 0;
  const { renderer, replace } = await renderOnboarding(t, () => {
    writes += 1;
    if (writes === 1) throw new Error('Storage temporarily unavailable');
  });
  await goToFinalSlide(renderer);
  await act(async () => { await renderer.root.findByType('PrimaryButton').props.onPress(); });

  assert.equal(replace.mock.callCount(), 0);
  assert.match(renderer.root.findByProps({ accessibilityRole: 'alert' }).props.children, /save your progress/);
  const retry = renderer.root.findAllByType('PrimaryButton')
    .find(({ props }) => props.children === 'Try again').props.onPress;
  await act(async () => { await Promise.all([retry(), retry()]); });
  assert.equal(writes, 2);
  assert.equal(replace.mock.callCount(), 1);
  assert.equal(replace.mock.calls[0].result, 'seen');
});

test('a guest can explicitly continue when storage remains unavailable', async (t) => {
  const write = t.mock.fn(() => { throw new Error('Storage unavailable'); });
  const { renderer, replace } = await renderOnboarding(t, write);
  await goToFinalSlide(renderer);
  await act(async () => { await renderer.root.findByType('PrimaryButton').props.onPress(); });

  const continueWithoutSaving = renderer.root.findAllByType('PrimaryButton')
    .find(({ props }) => props.children === 'Continue without saving').props.onPress;
  await act(async () => { await Promise.all([continueWithoutSaving(), continueWithoutSaving()]); });
  assert.equal(write.mock.callCount(), 1);
  assert.equal(replace.mock.callCount(), 1);
  assert.equal(replace.mock.calls[0].result, undefined);
});
