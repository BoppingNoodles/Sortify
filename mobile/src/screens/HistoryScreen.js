// src/screens/HistoryScreen.js
import React, { useCallback, useState } from 'react';
import { ActivityIndicator, View, Text, FlatList, StyleSheet } from 'react-native'; 
import { useFocusEffect } from '@react-navigation/native';
import { loadSavedScans } from '../services/storage';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function HistoryScreen() {
  const [history, setHistory] = useState(null);
  const [refreshing, setRefreshing] = useState(false);

  useFocusEffect(useCallback(() => {
    let active = true;
    setHistory(null);
    loadSavedScans().then((scans) => {
      if (active) setHistory(scans);
    });
    return () => { active = false; };
  }, []));

  const onRefresh = async () => 
    {setRefreshing(true);
    try {const scans = await loadSavedScans();
    setHistory(scans);} finally {setRefreshing(false);}};
  const BIN_NAMES = { // Target bin names
    compost: 'Green Compost Bin',
    recycling: 'Blue Recycling Bin',
    landfill: 'Gray/Black Landfill Bin'};
  const renderItem = ({ item }) => {
  const binColor = COLORS.bins[item.category] || COLORS.bins.landfill;
  const binName = BIN_NAMES[item.category] || item.category;
    return (
      <View style={styles.itemCard}>
        <View style={[styles.badge, { backgroundColor: binColor }]}>
          <Text style={styles.badgeText}>{item.category.toUpperCase()}</Text>
        </View>
        <View style={styles.itemDetails}>
          <Text style={styles.itemName}>{item.item_name}</Text>
          <Text style={[styles.binName, { color: binColor }]}>
            {binName}
          </Text>
          <Text style={styles.itemTime}>
            {new Date(item.timestamp).toLocaleString()}
          </Text>
        </View>
        {/* Eco-points badge */}
          <View style={styles.pointsBadge}>
            <Text style={styles.pointsText}>+10 pts</Text>
          </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Scan History</Text>
      {history === null ? (
        <ActivityIndicator accessibilityLabel="Loading scan history" color={COLORS.accent.berkeleyBlue} />
      ) : (
        <FlatList
          data={history}
          keyExtractor={(item) => item.id}
          renderItem={renderItem}
          refreshing={refreshing}
          onRefresh={onRefresh}
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyIcon}>♻️</Text>
              <Text style={styles.emptyTitle}>No scans yet!</Text>
              <Text style={styles.emptyText}>
                Snap an item to start your streak.
              </Text>
            </View>}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background.primary, padding: SPACING.md, paddingTop: SPACING.xl },
  title: { ...TYPOGRAPHY.header, marginBottom: SPACING.md, color: COLORS.accent.berkeleyBlue },
  emptyText: { ...TYPOGRAPHY.body, color: COLORS.text.secondary },
  listContent: { paddingBottom: 24 },
  itemCard: { flexDirection: 'row', backgroundColor: COLORS.background.card, padding: 14, borderRadius: 12, marginBottom: 10, alignItems: 'center', borderWidth: 1, borderColor: '#E2E8F0' },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 6, marginRight: 12 },
  badgeText: { color: COLORS.text.inverse, fontSize: 11, fontWeight: '700' },
  itemDetails: { flex: 1 },
  itemName: { ...TYPOGRAPHY.body, fontWeight: '600', color: COLORS.text.primary },
  itemTime: { ...TYPOGRAPHY.caption, color: COLORS.text.muted, marginTop: 2 },
  binName: {fontSize: 12, fontWeight: '500',marginTop: 4},
  pointsBadge: {backgroundColor: '#DCFCE7', paddingHorizontal: 8, paddingVertical: 6, borderRadius: 8},
  pointsText: {color: '#16A34A', fontSize: 12, fontWeight: '700'},
  emptyContainer: {alignItems: 'center', paddingVertical: 32},
  emptyIcon: {fontSize: 48, marginBottom: 16},
  emptyTitle: {fontSize: 18,fontWeight: '600', color: COLORS.text.primary, marginBottom: 8},
});
