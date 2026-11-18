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
import { loadSavedScans } from '../services/storage';
import { COLORS, SPACING } from '../styles/theme';

function calculateStreak(timestamps) {
  if (!Array.isArray(timestamps) || timestamps.length === 0) return 0;

  const dates = [
    ...new Set(
      timestamps
        .filter((ts) => typeof ts === 'string')
        .map((ts) => {
          try {
            return new Date(ts).toISOString().split('T')[0];
          } catch {
            return null;
          }
        })
        .filter(Boolean)
    ),
  ].sort((a, b) => (a < b ? 1 : -1));

  if (dates.length === 0) return 0;

  const today = new Date().toISOString().split('T')[0];
  const yesterday = new Date(Date.now() - 86400000).toISOString().split('T')[0];

  if (dates[0] !== today && dates[0] !== yesterday) {
    return 0;
  }

  let streak = 0;
  let checkDate = new Date(dates[0]);

  for (const dateStr of dates) {
    const current = new Date(dateStr);
    const diffDays = Math.round((checkDate - current) / 86400000);
    if (diffDays <= 1) {
      streak += 1;
      checkDate = current;
    } else {
      break;
    }
  }

  return streak;
}

export default function StatsScreen() {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({
    currentStreak: 0,
    totalScans: 0,
    ecoPoints: 0,
    breakdown: { compost: 0, plastic: 0, paper: 0, glass: 0, landfill: 0 },
  });

  const computeStats = async () => {
    try {
      const scans = await loadSavedScans();
      const total = scans.length;
      const points = total * 10;

      const counts = { compost: 0, plastic: 0, paper: 0, glass: 0, landfill: 0 };
      const timestamps = [];

      scans.forEach((scan) => {
        const cat = (scan.category || '').toLowerCase();
        if (Object.prototype.hasOwnProperty.call(counts, cat)) {
          counts[cat] += 1;
        } else {
          counts.landfill += 1;
        }
        if (scan.timestamp) timestamps.push(scan.timestamp);
      });

      const streak = calculateStreak(timestamps);

      setStats({
        currentStreak: streak,
        totalScans: total,
        ecoPoints: points,
        breakdown: counts,
      });
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
          <Text style={styles.screenTitle}>Impact Dashboard</Text>

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
              <Text style={styles.statLabel}>Total Scans</Text>
            </View>
            <View style={styles.statBox}>
              <Text style={styles.statNumber}>{stats.ecoPoints}</Text>
              <Text style={styles.statLabel}>Eco Points</Text>
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
  screenTitle: { fontSize: 24, fontWeight: '800', color: COLORS.accent.berkeleyBlue, marginBottom: 16 },
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
  streakCount: { fontSize: 22, fontWeight: '800', color: '#E65100' },
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
    borderColor: '#E2E8F0',
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
    borderColor: '#E2E8F0',
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
