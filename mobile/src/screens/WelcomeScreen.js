import React from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { PrimaryButton } from '../components/DesignPrimitives';
import { COLORS } from '../styles/theme';

export default function WelcomeScreen({ onContinue }) {
  return (
    <SafeAreaView style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.card}>
          <Text accessibilityRole="header" style={styles.title}>Welcome to Sortify</Text>
          <Text style={styles.copy}>Sort items, build your streak, and keep track of your scans on this device.</Text>
          <PrimaryButton onPress={onContinue}>Continue as guest</PrimaryButton>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#F4FCF6' },
  content: { flexGrow: 1, paddingTop: 28 },
  card: {
    flexGrow: 1, backgroundColor: COLORS.background.card, borderColor: COLORS.design.border,
    borderWidth: 1, borderRadius: 24, paddingHorizontal: 28, paddingVertical: 34, gap: 18,
  },
  title: { color: COLORS.text.primary, fontSize: 30, fontWeight: '800' },
  copy: { color: COLORS.text.secondary, fontSize: 16, lineHeight: 24, marginBottom: 12 },
});
