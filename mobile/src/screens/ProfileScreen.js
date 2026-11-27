import React, { useCallback, useState } from 'react';
import { ScrollView, StyleSheet, Text, TouchableOpacity, View, useColorScheme } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ProgressBar } from '../components/DesignPrimitives';
import { summarizeScans } from '../services/scanStats';
import { loadSavedScans } from '../services/storage';
import { createThemedStyles } from '../styles/theme';

const MILESTONE_STEP = 100;

export default function ProfileScreen({ navigation }) {
  const { colors, styles } = getStyles(useColorScheme());
  const [scans, setScans] = useState([]);
  useFocusEffect(useCallback(() => {
    let active = true;
    loadSavedScans().then((saved) => {
      if (active) setScans(saved);
    });
    return () => { active = false; };
  }, []));

  const { currentStreak, ecoPoints, totalScans } = summarizeScans(scans);
  const milestone = Math.max(1, Math.ceil(ecoPoints / MILESTONE_STEP)) * MILESTONE_STEP;
  const milestoneProgress = ecoPoints - (milestone - MILESTONE_STEP);

  return (
    <SafeAreaView edges={['top', 'left', 'right']} style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text accessibilityRole="header" style={styles.title}>Current points</Text>
        <View style={styles.identity}>
          <Text style={styles.avatar} accessible={false}>🐻</Text>
          <View>
            <Text style={styles.name}>Guest</Text>
            <Text style={styles.caption}>Current streak</Text>
            <Text style={styles.bold}>{currentStreak} Day{currentStreak === 1 ? '' : 's'}</Text>
          </View>
        </View>
        <View style={styles.card}>
          <Text style={styles.caption}>Total items sorted</Text>
          <Text style={styles.total}>{totalScans}</Text>
          <View style={styles.row}>
            <Text style={styles.bold}>{ecoPoints}</Text>
            <Text style={styles.caption}>{milestone} point milestone</Text>
          </View>
          <ProgressBar value={milestoneProgress} max={MILESTONE_STEP} label={`Progress toward ${milestone} points`} />
        </View>
        <View style={styles.row}>
          <Text accessibilityRole="header" style={styles.section}>Recent History</Text>
          <TouchableOpacity accessibilityRole="button" onPress={() => navigation.navigate('History')}>
            <Text style={styles.link}>View all</Text>
          </TouchableOpacity>
        </View>
        {scans.length === 0 && (
          <View style={styles.historyRow}><Text style={styles.caption}>No scans yet</Text></View>
        )}
        {scans.slice(0, 3).map((scan) => (
          <View key={scan.id} style={styles.historyRow}>
            <View style={[styles.swatch, { backgroundColor: colors.bins[scan.category] || colors.bins.landfill }]} />
            <View style={styles.historyCopy}>
              <Text style={styles.bold}>{scan.item_name}</Text>
              <Text style={styles.caption}>{scan.disposal_tip}</Text>
            </View>
          </View>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const getStyles = createThemedStyles((colors) => StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background.primary },
  content: { padding: 18, paddingTop: 24, gap: 14 },
  title: { fontSize: 26, fontWeight: '800', color: colors.text.primary },
  identity: { flexDirection: 'row', gap: 14, alignItems: 'center' },
  avatar: { fontSize: 35, borderRadius: 32, padding: 9, backgroundColor: colors.design.greenTint },
  name: { fontSize: 21, fontWeight: '800', color: colors.text.primary },
  card: { padding: 18, borderRadius: 20, backgroundColor: colors.background.card, borderWidth: 1, borderColor: colors.design.border, gap: 8 },
  caption: { color: colors.text.secondary, fontSize: 13, lineHeight: 19 },
  total: { color: colors.text.primary, fontSize: 26, fontWeight: '800' },
  bold: { color: colors.text.primary, fontWeight: '800' },
  row: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 8 },
  section: { fontSize: 19, fontWeight: '800', color: colors.text.primary },
  link: { paddingVertical: 8, color: colors.accent.berkeleyBlue, fontWeight: '700' },
  historyRow: { flexDirection: 'row', alignItems: 'center', gap: 12, padding: 12, backgroundColor: colors.background.card, borderWidth: 1, borderColor: colors.design.border, borderRadius: 14 },
  swatch: { width: 42, height: 42, borderRadius: 9 },
  historyCopy: { flex: 1 },
}));
