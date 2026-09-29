// src/screens/HistoryScreen.js
import React, { useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

const MOCK_HISTORY = [
  { id: '1', item_name: 'Starbucks Hot Cup', category: 'compost', time: 'Today, 10:14 AM' },
  { id: '2', item_name: 'Plastic Water Bottle', category: 'plastic', time: 'Yesterday, 3:45 PM' },
  { id: '3', item_name: 'Aluminum Soda Can', category: 'paper', time: 'Sep 20, 1:20 PM' },
];

export default function HistoryScreen() {
  const [history] = useState(MOCK_HISTORY);

  const renderItem = ({ item }) => {
    const binColor = COLORS.bins[item.category] || COLORS.bins.landfill;
    return (
      <View style={styles.itemCard}>
        <View style={[styles.badge, { backgroundColor: binColor }]}>
          <Text style={styles.badgeText}>{item.category.toUpperCase()}</Text>
        </View>
        <View style={styles.itemDetails}>
          <Text style={styles.itemName}>{item.item_name}</Text>
          <Text style={styles.itemTime}>{item.time}</Text>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Scan History</Text>
      <FlatList
        data={history}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background.primary, padding: SPACING.md, paddingTop: SPACING.xl },
  title: { ...TYPOGRAPHY.header, marginBottom: SPACING.md, color: COLORS.accent.berkeleyBlue },
  listContent: { paddingBottom: 24 },
  itemCard: { flexDirection: 'row', backgroundColor: COLORS.background.card, padding: 14, borderRadius: 12, marginBottom: 10, alignItems: 'center', borderWidth: 1, borderColor: '#E2E8F0' },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 6, marginRight: 12 },
  badgeText: { color: COLORS.text.inverse, fontSize: 11, fontWeight: '700' },
  itemDetails: { flex: 1 },
  itemName: { ...TYPOGRAPHY.body, fontWeight: '600', color: COLORS.text.primary },
  itemTime: { ...TYPOGRAPHY.caption, color: COLORS.text.muted, marginTop: 2 },
});
