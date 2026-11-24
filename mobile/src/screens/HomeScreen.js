import React, { useCallback, useState } from 'react';
import { ScrollView, StyleSheet, Text, TouchableOpacity, View, useColorScheme } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { PrimaryButton, ProgressBar } from '../components/DesignPrimitives';
import { wakeServer } from '../services/api';
import { summarizeScans } from '../services/scanStats';
import { loadSavedScans } from '../services/storage';
import { createThemedStyles } from '../styles/theme';

const DAILY_GOAL = 10;

export default function HomeScreen({ navigation }) {
  const { styles } = getStyles(useColorScheme());
  const [stats, setStats] = useState(() => summarizeScans([]));
  useFocusEffect(useCallback(() => {
    let active = true;
    loadSavedScans().then((scans) => {
      if (active) setStats(summarizeScans(scans));
    });
    return () => { active = false; };
  }, []));

  const remaining = Math.max(0, DAILY_GOAL - stats.scansToday);

  return (
    <SafeAreaView edges={['top', 'left', 'right']} style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View style={styles.identity}>
            <Text style={styles.avatar} accessible={false}>🐻</Text>
            <View>
              <Text style={styles.name}>Guest</Text>
              <Text style={styles.secondary}>{stats.totalScans} items sorted</Text>
            </View>
          </View>
          <TouchableOpacity
            accessibilityRole="button"
            accessibilityLabel="View streak and impact stats"
            style={styles.streak}
            onPress={() => navigation.navigate('Stats')}
          >
            <Text style={styles.streakLabel}>🔥 {stats.currentStreak} {stats.currentStreak === 1 ? 'day' : 'days'}</Text>
          </TouchableOpacity>
        </View>

        <View style={styles.goal}>
          <Text style={styles.secondary}>Daily goal</Text>
          <Text style={styles.goalCount}>{stats.scansToday}/{DAILY_GOAL} scans</Text>
          <ProgressBar value={stats.scansToday} max={DAILY_GOAL} label="Daily scan goal" />
          <Text style={styles.secondary}>
            {remaining > 0 ? `${remaining} more ${remaining === 1 ? 'scan' : 'scans'} to reach today’s goal` : 'Daily goal reached'}
          </Text>
        </View>

        <Text style={styles.prompt}>Throwing away?</Text>
        <PrimaryButton
          onPress={() => {
            void wakeServer();
            navigation.navigate('Scan');
          }}
        >
          Start
        </PrimaryButton>
      </ScrollView>
    </SafeAreaView>
  );
}

const getStyles = createThemedStyles((colors) => StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.background.card },
  content: { flexGrow: 1, padding: 18, paddingTop: 24, gap: 14 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 10 },
  identity: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  avatar: { fontSize: 25, backgroundColor: colors.design.greenTint, borderRadius: 22, padding: 6 },
  name: { color: colors.text.primary, fontSize: 17, fontWeight: '800' },
  secondary: { color: colors.text.secondary, fontSize: 13, lineHeight: 19 },
  streak: { borderWidth: 1, borderColor: colors.design.border, borderRadius: 20, paddingHorizontal: 12, paddingVertical: 9 },
  streakLabel: { color: colors.text.primary, fontWeight: '700' },
  goal: { flexGrow: 1, minHeight: 224, borderColor: colors.design.border, borderWidth: 1, borderRadius: 20, padding: 16, gap: 10 },
  goalCount: { color: colors.text.primary, fontWeight: '800', fontSize: 25 },
  prompt: { color: colors.accent.berkeleyBlue, fontWeight: '700' },
}));
