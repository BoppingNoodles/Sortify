// src/screens/ProfileScreen.js
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function ProfileScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Student Profile</Text>
      <View style={styles.card}>
        <Text style={styles.avatar}>🐻</Text>
        <Text style={styles.name}>Cal Bear Eco Champion</Text>
        <Text style={styles.email}>student@berkeley.edu</Text>
        <View style={styles.divider} />
        <View style={styles.statRow}>
          <View style={styles.statItem}>
            <Text style={styles.statVal}>3 Days</Text>
            <Text style={styles.statLabel}>Current Streak</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statVal}>120</Text>
            <Text style={styles.statLabel}>Eco Points</Text>
          </View>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background.primary, padding: SPACING.md, paddingTop: SPACING.xl },
  title: { ...TYPOGRAPHY.header, marginBottom: SPACING.md, color: COLORS.accent.berkeleyBlue },
  card: { backgroundColor: COLORS.background.card, borderRadius: 16, padding: SPACING.lg, alignItems: 'center', borderWidth: 1, borderColor: '#E2E8F0' },
  avatar: { fontSize: 48, marginBottom: 8 },
  name: { ...TYPOGRAPHY.subtitle, fontSize: 18, color: COLORS.text.primary },
  email: { ...TYPOGRAPHY.caption, color: COLORS.text.secondary, marginTop: 2 },
  divider: { height: 1, width: '100%', backgroundColor: '#E2E8F0', marginVertical: 16 },
  statRow: { flexDirection: 'row', width: '100%', justifyContent: 'space-around' },
  statItem: { alignItems: 'center' },
  statVal: { fontSize: 18, fontWeight: '700', color: COLORS.accent.berkeleyBlue },
  statLabel: { fontSize: 12, color: COLORS.text.secondary, marginTop: 4 },
});
