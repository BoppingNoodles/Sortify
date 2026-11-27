// mobile/App.js
import React, { useEffect } from 'react';
import { AppState, useColorScheme } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { DarkTheme, DefaultTheme, NavigationContainer } from '@react-navigation/native';
import AppNavigator from './src/navigation/AppNavigator';
import { wakeServer } from './src/services/api';
import { getOrCreateDeviceUuid } from './src/services/storage';
import { CityPreferenceProvider } from './src/services/CityPreference';
import { getAppColors } from './src/styles/theme';

function createNavigationTheme(theme, colors) {
  return {
    ...theme,
    colors: {
      ...theme.colors,
      background: colors.background.primary,
      card: colors.background.card,
      text: colors.text.primary,
      border: colors.design.border,
      primary: colors.accent.berkeleyBlue,
    },
  };
}

const lightNavigationTheme = createNavigationTheme(DefaultTheme, getAppColors('light'));
const darkNavigationTheme = createNavigationTheme(DarkTheme, getAppColors('dark'));

export default function App() {
  const isDark = useColorScheme() === 'dark';
  useEffect(() => {
    void getOrCreateDeviceUuid();
  }, []);

  // Start waking the backend early so the first scan doesn't wait for it.
  useEffect(() => {
    void wakeServer();
    const subscription = AppState.addEventListener('change', (state) => {
      if (state === 'active') void wakeServer();
    });
    return () => subscription.remove();
  }, []);

  return (
    <SafeAreaProvider>
      <NavigationContainer theme={isDark ? darkNavigationTheme : lightNavigationTheme}>
        <CityPreferenceProvider><AppNavigator /></CityPreferenceProvider>
        <StatusBar style={isDark ? 'light' : 'dark'} />
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
