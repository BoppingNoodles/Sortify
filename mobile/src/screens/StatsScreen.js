// src/screens/StatsScreen.js
import React, { useCallback, useState } from 'react';
import {
  StyleSheet,
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
import { COLORS, SPACING } from '../styles/theme';

export default function StatsScreen() {
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
          <ActivityIndicator size="large" color={COLORS.accent.berkeleyBlue} />
        </View>
      ) : (
        <ScrollView
          contentContainerStyle={styles.content}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
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
              const binColor = COLORS.bins[cat] || COLORS.bins.landfill;
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

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background.primary },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  content: { padding: 20 },
  screenTitle: { fontSize: 24, fontWeight: '800', color: COLORS.accent.berkeleyBlue, marginBottom: 4 },
  scopeText: { fontSize: 13, color: COLORS.text.secondary, lineHeight: 18, marginBottom: 16 },
  streakCard: {
    backgroundColor: '#FFF3E0',
    borderColor: '#FFE0B2',
    borderWidth: 1,
    borderRadius: 18,
    padding: 24,
    alignItems: 'center',
    marginBottom: 16,
  },
  streakEmoji: { fontSize: 44, marginBottom: 8 },
  streakCount: { fontSize: 22, fontWeight: '800', color: COLORS.design.greenText },
  streakSubtext: { fontSize: 13, color: '#BF360C', marginTop: 4, textAlign: 'center' },
  statsGrid: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 16 },
  statBox: {
    flex: 1,
    backgroundColor: COLORS.background.card,
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 4,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
    borderWidth: 1,
    borderColor: COLORS.design.border,
  },
  statNumber: { fontSize: 26, fontWeight: '800', color: COLORS.accent.berkeleyBlue },
  statLabel: { fontSize: 13, color: COLORS.text.secondary, marginTop: 4, fontWeight: '600' },
  breakdownCard: {
    backgroundColor: COLORS.background.card,
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
    borderWidth: 1,
    borderColor: COLORS.design.border,
  },
  cardHeader: { fontSize: 16, fontWeight: '700', color: COLORS.text.primary, marginBottom: 14 },
  categoryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
  categoryLeft: { flexDirection: 'row', alignItems: 'center' },
  categoryIndicator: { width: 10, height: 10, borderRadius: 5, marginRight: 10 },
  categoryName: { fontSize: 14, fontWeight: '600', color: COLORS.text.primary },
  categoryCount: { fontSize: 14, fontWeight: '700', color: COLORS.accent.berkeleyBlue },
});
