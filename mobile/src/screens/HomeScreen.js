// src/screens/HomeScreen.js
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function HomeScreen({ navigation }) {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Bear Mascot & Campus Greeting */}
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Welcome back, Cal Bear! 🐻</Text>
        <Text style={styles.subText}>UC Berkeley Sustainable Campus</Text>
      </View>

      {/* Daily Streak Card */}
      <View style={styles.streakCard}>
        <Text style={styles.streakEmoji}>🔥</Text>
        <View>
          <Text style={styles.streakNumber}>3 Day Streak</Text>
          <Text style={styles.streakSubtext}>Scan an item today to keep it active!</Text>
        </View>
      </View>

      {/* Main Scan Button CTA */}
      <TouchableOpacity 
        style={styles.scanCta}
        onPress={() => navigation.navigate('Scan')}
        activeOpacity={0.8}
      >
        <Text style={styles.scanCtaText}>📸 Scan Waste Item</Text>
      </TouchableOpacity>

      {/* Did You Know? Tip Card */}
      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>Did you know?</Text>
        <Text style={styles.infoBody}>
          Pizza boxes with grease belong in the green Compost bin at Berkeley, not paper recycling!
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background.primary },
  content: { padding: SPACING.lg, paddingTop: SPACING.xl },
  header: { marginBottom: SPACING.lg },
  welcomeText: { ...TYPOGRAPHY.header, color: COLORS.accent.berkeleyBlue },
  subText: { ...TYPOGRAPHY.caption, color: COLORS.text.secondary, marginTop: 4 },
  streakCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFFBEB', padding: SPACING.md, borderRadius: 12, borderWidth: 1, borderColor: '#FDE68A', marginBottom: SPACING.lg },
  streakEmoji: { fontSize: 32, marginRight: 12 },
  streakNumber: { fontWeight: '700', fontSize: 16, color: '#B45309' },
  streakSubtext: { fontSize: 12, color: '#92400E' },
  scanCta: { backgroundColor: COLORS.bins.compost, padding: 18, borderRadius: 16, alignItems: 'center', marginBottom: SPACING.lg, elevation: 3 },
  scanCtaText: { color: COLORS.text.inverse, fontSize: 18, fontWeight: '700' },
  infoCard: { backgroundColor: COLORS.background.card, padding: SPACING.md, borderRadius: 12, borderWidth: 1, borderColor: '#E2E8F0' },
  infoTitle: { ...TYPOGRAPHY.subtitle, fontSize: 16, marginBottom: 4 },
  infoBody: { ...TYPOGRAPHY.body, color: COLORS.text.secondary, lineHeight: 20 },
});
