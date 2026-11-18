import React, { useEffect, useState } from 'react';
import { ActivityIndicator, StyleSheet, View, useColorScheme } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';
import HomeScreen from '../screens/HomeScreen';
import ScanScreen from '../screens/ScanScreen';
import HistoryScreen from '../screens/HistoryScreen';
import ProfileScreen from '../screens/ProfileScreen';
import ResultScreen from '../screens/ResultScreen';
import StatsScreen from '../screens/StatsScreen';
import RulesScreen from '../screens/RulesScreen';
import WelcomeScreen from '../screens/WelcomeScreen';
import { hasSeenWelcome, markWelcomeSeen } from '../services/storage';
import { getAppColors } from '../styles/theme';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();
const TAB_ICONS = { Profile: 'person-outline', Rules: 'shield-checkmark-outline', Home: 'home-outline' };

function MainTabs() {
  const colors = getAppColors(useColorScheme());
  return (
    <Tab.Navigator
      initialRouteName="Home"
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: colors.text.primary,
        tabBarInactiveTintColor: colors.text.muted,
        tabBarStyle: { backgroundColor: colors.background.card, borderTopColor: colors.design.border },
        tabBarLabelStyle: { fontWeight: '700' },
        tabBarIcon: ({ color, size }) => <Ionicons name={TAB_ICONS[route.name]} size={size} color={color} />,
      })}
    >
      <Tab.Screen name="Profile" component={ProfileScreen} />
      <Tab.Screen name="Rules" component={RulesScreen} options={{ title: 'Municipal Rules' }} />
      <Tab.Screen name="Home" component={HomeScreen} />
    </Tab.Navigator>
  );
}

function GuestWelcome({ navigation }) {
  const finishing = React.useRef(false);
  const [completion, setCompletion] = useState('idle');

  async function continueAsGuest(saveCompletion) {
    if (finishing.current) return;
    finishing.current = true;
    setCompletion('saving');

    try {
      if (saveCompletion) await markWelcomeSeen();
    } catch {
      finishing.current = false;
      setCompletion('failed');
      return;
    }

    navigation.replace('MainTabs');
  }

  return (
    <WelcomeScreen
      saving={completion === 'saving'}
      saveFailed={completion === 'failed'}
      onContinue={() => continueAsGuest(true)}
      onContinueWithoutSaving={() => continueAsGuest(false)}
    />
  );
}

export default function AppNavigator() {
  const colors = getAppColors(useColorScheme());
  const [seenWelcome, setSeenWelcome] = useState(null);

  useEffect(() => {
    let active = true;
    hasSeenWelcome().then((seen) => {
      if (active) setSeenWelcome(seen);
    });
    return () => { active = false; };
  }, []);

  if (seenWelcome === null) {
    return <View style={[styles.loading, { backgroundColor: colors.background.card }]}><ActivityIndicator accessibilityLabel="Loading Sortify" /></View>;
  }

  return (
    <Stack.Navigator
      initialRouteName={seenWelcome ? 'MainTabs' : 'Welcome'}
      screenOptions={{
        headerTintColor: colors.text.primary,
        headerShadowVisible: false,
        headerStyle: { backgroundColor: colors.background.card },
        contentStyle: { backgroundColor: colors.background.primary },
      }}
    >
      <Stack.Screen name="Welcome" component={GuestWelcome} options={{ headerShown: false }} />
      <Stack.Screen name="MainTabs" component={MainTabs} options={{ headerShown: false }} />
      <Stack.Screen name="Scan" component={ScanScreen} options={{ title: 'Camera preview' }} />
      <Stack.Screen name="History" component={HistoryScreen} options={{ title: 'History' }} />
      <Stack.Screen name="ResultModal" component={ResultScreen} options={{ presentation: 'modal', title: 'Classification Result' }} />
      <Stack.Screen name="Stats" component={StatsScreen} options={{ title: 'Impact Dashboard' }} />
    </Stack.Navigator>
  );
}

const styles = StyleSheet.create({
  loading: { flex: 1, alignItems: 'center', justifyContent: 'center' },
});
