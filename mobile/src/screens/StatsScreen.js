// src/screens/StatsScreen.js
import React, { useCallback, useState } from 'react';
import {
  StyleSheet,
  useColorScheme,
  Text,
  View,
  ScrollView,
  SafeAreaView,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { HISTORY_LIMIT, loadSavedScans } from '../services/storage';
import { summarizeScans } from '../services/scanStats';
import { createThemedStyles, SPACING } from '../styles/theme';

export default function StatsScreen() {
  const { colors, styles } = getStyles(useColorScheme());
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState(() => summarizeScans([]));

  const computeStats = async () => {
    try {
      setStats(summarizeScans(await loadSavedScans()));
    } catch (err) {
      console.warn('Failed to compute stats:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      computeStats();
    }, [])
  );

  const onRefresh = () => {
    setRefreshing(true);
    computeStats();
  };

  return (
    <SafeAreaView style={styles.container}>
      {loading ? (
        <View style={styles.centered}>
          <ActivityIndicator size="large" color={colors.accent.berkeleyBlue} />
        </View>
      ) : (
        <ScrollView
          contentContainerStyle={styles.content}
          refreshControl={(
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              tintColor={colors.accent.berkeleyBlue}
              colors={[colors.accent.berkeleyBlue]}
              progressBackgroundColor={colors.background.card}
            />
          )}
        >
          <Text style={styles.screenTitle}>Recent Scan Activity</Text>
          <Text style={styles.scopeText}>
            Based on your last {HISTORY_LIMIT} saved scans on this device.
          </Text>

          {/* Streak Flame Card */}
          <View style={styles.streakCard}>
            <Text style={styles.streakEmoji}>🔥</Text>
            <Text style={styles.streakCount}>
              {stats.currentStreak} Day{stats.currentStreak === 1 ? '' : 's'} Streak!
            </Text>
            <Text style={styles.streakSubtext}>
              {stats.currentStreak > 0
                ? 'Great job! Scan daily to keep your streak alive.'
                : 'Scan an item today to start your streak!'}
            </Text>
          </View>

          {/* Impact Counters Grid */}
          <View style={styles.statsGrid}>
            <View style={styles.statBox}>
              <Text style={styles.statNumber}>{stats.totalScans}</Text>
              <Text style={styles.statLabel}>Saved Scans</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statNumber}>{stats.ecoPoints}</Text>
              <Text style={styles.statLabel}>Points from Saved Scans</Text>
            </View>
          </View>

          {/* Sorting Category Breakdown */}
          <View style={styles.breakdownCard}>
            <Text style={styles.cardHeader}>Category Distribution</Text>
            {Object.entries(stats.breakdown).map(([cat, count]) => {
              const binColor = colors.bins[cat] || colors.bins.landfill;
              return (
                <View key={cat} style={styles.categoryRow}>
                  <View style={styles.categoryLeft}>
                    <View style={[styles.categoryIndicator, { backgroundColor: binColor }]} />
                    <Text style={styles.categoryName}>{cat.toUpperCase()}</Text>
                  </View>
                  <Text style={styles.categoryCount}>
                    {count} {count === 1 ? 'item' : 'items'}
                  </Text>
                </View>
              );
            })}
          </View>
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const getStyles = createThemedStyles((colors) => StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background.primary },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  content: { padding: 20 },
  screenTitle: { fontSize: 24, fontWeight: '800', color: colors.accent.berkeleyBlue, marginBottom: 4 },
  scopeText: { fontSize: 13, color: colors.text.secondary, lineHeight: 18, marginBottom: 16 },
  streakCard: {
    backgroundColor: colors.design.streak,
    borderColor: colors.design.streakBorder,
    borderWidth: 1,
    borderRadius: 18,
    padding: 24,
    alignItems: 'center',
    marginBottom: 16,
  },
  streakEmoji: { fontSize: 44, marginBottom: 8 },
  streakCount: { fontSize: 22, fontWeight: '800', color: colors.design.greenText },
  streakSubtext: { fontSize: 13, color: colors.design.streakText, marginTop: 4, textAlign: 'center' },
  statsGrid: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 16 },
  statBox: {
    flex: 1,
    backgroundColor: colors.background.card,
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 4,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
    borderWidth: 1,
    borderColor: colors.design.border,
  },
  statNumber: { fontSize: 26, fontWeight: '800', color: colors.accent.berkeleyBlue },
  statLabel: { fontSize: 13, color: colors.text.secondary, marginTop: 4, fontWeight: '600' },
  breakdownCard: {
    backgroundColor: colors.background.card,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
    borderWidth: 1,
    borderColor: colors.design.border,
  },
  cardHeader: { fontSize: 16, fontWeight: '700', color: colors.text.primary, marginBottom: 14 },
  categoryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: colors.design.border,
  },
  categoryLeft: { flexDirection: 'row', alignItems: 'center' },
  categoryIndicator: { width: 10, height: 10, borderRadius: 5, marginRight: 10 },
  categoryName: { fontSize: 14, fontWeight: '600', color: colors.text.primary },
  categoryCount: { fontSize: 14, fontWeight: '700', color: colors.accent.berkeleyBlue },
}));
