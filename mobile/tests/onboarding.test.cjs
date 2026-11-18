const assert = require('node:assert/strict');
const { test } = require('node:test');
const React = require('react');
const { create, act } = require('react-test-renderer');
const { loadSource } = require('./load-source.cjs');

global.IS_REACT_ACT_ENVIRONMENT = true;

test('first launch offers three swipeable slides and remembers completion', async (t) => {
  const values = new Map();
  const storage = loadSource('src/services/storage.js', {
    '@react-native-async-storage/async-storage': {
      getItem: async (key) => values.get(key) ?? null,
      setItem: async (key, value) => { values.set(key, value); },
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
    assert.equal(values.get('@sortify_guest_welcome'), 'seen');
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
  await act(async () => { renderer = create(React.createElement(AppNavigator)); });
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
  for (let page = 0; page < 2; page += 1) {
    await act(async () => { renderer.root.findByType('PrimaryButton').props.onPress(); });
  }
  assert.equal(heading(), 'Build sorting streaks');
  const finish = renderer.root.findByType('PrimaryButton').props.onPress;
  await act(async () => { await Promise.all([finish(), finish()]); });
  assert.equal(replace.mock.callCount(), 1);
  await act(async () => {
    renderer.unmount();
    renderer = create(React.createElement(AppNavigator));
  });
  assert.ok(renderer.root.findByType('MainTabs'));
});
