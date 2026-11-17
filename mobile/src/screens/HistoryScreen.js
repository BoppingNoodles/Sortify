// src/screens/HistoryScreen.js
import React, { useCallback, useState } from 'react';
import { ActivityIndicator, View, Text, FlatList, StyleSheet } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { loadSavedScans } from '../services/storage';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function HistoryScreen() {
  const [history, setHistory] = useState(null);

  useFocusEffect(useCallback(() => {
    let active = true;
    setHistory(null);
    loadSavedScans().then((scans) => {
      if (active) setHistory(scans);
    });
    return () => { active = false; };
  }, []));

  const renderItem = ({ item }) => {
    const binColor = COLORS.bins[item.category] || COLORS.bins.landfill;
    return (
      <View style={styles.itemCard}>
        <View style={[styles.badge, { backgroundColor: binColor }]}>
          <Text style={styles.badgeText}>{item.category.toUpperCase()}</Text>
        </View>
        <View style={styles.itemDetails}>
          <Text style={styles.itemName}>{item.item_name}</Text>
          <Text style={styles.itemTime}>{new Date(item.timestamp).toLocaleString()}</Text>
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
          contentContainerStyle={styles.listContent}
          ListEmptyComponent={<Text style={styles.emptyText}>No scans yet.</Text>}
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
});
