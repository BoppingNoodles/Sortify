import React, { useEffect, useState } from 'react';
import { ActivityIndicator, StyleSheet, View } from 'react-native';
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
import { COLORS } from '../styles/theme';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();
const TAB_ICONS = { Profile: 'person-outline', Rules: 'shield-checkmark-outline', Home: 'home-outline' };

function MainTabs() {
  return (
    <Tab.Navigator
      initialRouteName="Home"
      screenOptions={({ route }) => ({
        headerShown: false,
        tabBarActiveTintColor: COLORS.text.primary,
        tabBarInactiveTintColor: COLORS.text.muted,
        tabBarStyle: { backgroundColor: COLORS.background.card, borderTopColor: COLORS.design.border },
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
  return (
    <WelcomeScreen onContinue={() => {
      void markWelcomeSeen();
      navigation.replace('MainTabs');
    }} />
  );
}

export default function AppNavigator() {
  const [seenWelcome, setSeenWelcome] = useState(null);

  useEffect(() => {
    let active = true;
    hasSeenWelcome().then((seen) => {
      if (active) setSeenWelcome(seen);
    });
    return () => { active = false; };
  }, []);

  if (seenWelcome === null) {
    return <View style={styles.loading}><ActivityIndicator accessibilityLabel="Loading Sortify" /></View>;
  }

  return (
    <Stack.Navigator
      initialRouteName={seenWelcome ? 'MainTabs' : 'Welcome'}
      screenOptions={{
        headerTintColor: COLORS.text.primary,
        headerShadowVisible: false,
        headerStyle: { backgroundColor: COLORS.background.card },
        contentStyle: { backgroundColor: COLORS.background.primary },
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
  loading: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: COLORS.background.card },
});
