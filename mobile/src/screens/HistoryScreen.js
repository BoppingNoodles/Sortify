// src/screens/HistoryScreen.js
import React, { useCallback, useRef, useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  FlatList,
  Image,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useFocusEffect } from '@react-navigation/native';
import { loadSavedScans } from '../services/storage';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function HistoryScreen({ navigation }) {
  const [scans, setScans] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const requestRef = useRef(0);

  const readHistory = (request) => {
    loadSavedScans()
      .then((data) => {
        if (request === requestRef.current) setScans(data ?? []);
      })
      .catch((err) => {
        console.warn('Failed to load history:', err);
        if (request === requestRef.current) setScans([]);
      })
      .finally(() => {
        if (request === requestRef.current) setRefreshing(false);
      });
  };

  useFocusEffect(
    useCallback(() => {
      const request = ++requestRef.current;
      setScans(null);
      setRefreshing(false);
      readHistory(request);
      return () => {
        requestRef.current += 1;
      };
    }, [])
  );

  const onRefresh = () => {
    const request = ++requestRef.current;
    setRefreshing(true);
    readHistory(request);
  };

  const renderItem = ({ item }) => {
    const itemName = item.item_name || item.itemName || 'Waste Item';
    const category = (item.category || item.bin || 'landfill').toLowerCase();
    const binColor = COLORS.bins[category] || COLORS.bins.landfill;
    const formattedDate = item.timestamp
      ? new Date(item.timestamp).toLocaleString()
      : 'Today';

    return (
      <View style={styles.scanCard}>
        {item.photoUri ? (
          <Image source={{ uri: item.photoUri }} style={styles.cardImage} />
        ) : (
          <View style={[styles.cardPlaceholder, { borderColor: binColor }]}>
            <Text style={styles.placeholderEmoji}>♻️</Text>
          </View>
        )}
        <View style={styles.cardContent}>
          <Text style={styles.cardTitle} numberOfLines={1}>
            {itemName}
          </Text>
          <View style={[styles.categoryBadge, { backgroundColor: binColor }]}>
            <Text style={styles.categoryBadgeText}>{category.toUpperCase()}</Text>
          </View>
          <Text style={styles.cardDate}>{formattedDate}</Text>
        </View>
        <View style={styles.pointsBadge}>
          <Text style={styles.pointsText}>+10 pts</Text>
        </View>
      </View>
    );
  };

  return (
    <SafeAreaView edges={['top', 'left', 'right']} style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Scan History</Text>
        {scans?.length > 0 && (
          <TouchableOpacity
            style={styles.statsCtaButton}
            onPress={() => navigation.navigate('Stats')}
            accessibilityRole="button"
            accessibilityLabel="View Impact Stats"
            activeOpacity={0.7}
          >
            <Text style={styles.statsCtaText}>📊 Stats</Text>
          </TouchableOpacity>
        )}
      </View>

      {scans === null ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator
            accessibilityLabel="Loading scan history"
            size="large"
            color={COLORS.accent.berkeleyBlue}
          />
        </View>
      ) : (
        <FlatList
          data={scans}
          keyExtractor={(item, index) => item.id || `scan_${index}`}
          renderItem={renderItem}
          contentContainerStyle={scans.length === 0 ? styles.emptyContainer : styles.listContent}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
          ListEmptyComponent={
            <View style={styles.emptyView}>
              <Text style={styles.emptyEmoji}>📸</Text>
              <Text style={styles.emptyTitle}>No scans yet</Text>
              <Text style={styles.emptyBody}>Snap an item to start your streak</Text>
              <TouchableOpacity
                style={styles.scanNowButton}
                onPress={() => navigation.navigate('Scan')}
                accessibilityRole="button"
                accessibilityLabel="Scan First Item"
                activeOpacity={0.8}
              >
                <Text style={styles.scanNowButtonText}>Scan First Item</Text>
              </TouchableOpacity>
            </View>
          }
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background.primary },
  header: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    backgroundColor: COLORS.background.card,
    borderBottomWidth: 1,
    borderBottomColor: '#E2E8F0',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: { ...TYPOGRAPHY.header, color: COLORS.accent.berkeleyBlue },
  statsCtaButton: {
    backgroundColor: '#EFF6FF',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: '#BFDBFE',
  },
  statsCtaText: { fontSize: 13, fontWeight: '700', color: COLORS.accent.berkeleyBlue },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  listContent: { padding: SPACING.md },
  emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: SPACING.lg },
  scanCard: {
    flexDirection: 'row',
    backgroundColor: COLORS.background.card,
    borderRadius: 14,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
    borderWidth: 1,
    borderColor: '#E2E8F0',
  },
  cardImage: { width: 56, height: 56, borderRadius: 10, marginRight: SPACING.md },
  cardPlaceholder: {
    width: 56,
    height: 56,
    borderRadius: 10,
    backgroundColor: COLORS.background.surface,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
    borderWidth: 2,
  },
  placeholderEmoji: { fontSize: 24 },
  cardContent: { flex: 1, justifyContent: 'center' },
  cardTitle: { ...TYPOGRAPHY.body, fontWeight: '700', color: COLORS.text.primary, marginBottom: 4 },
  categoryBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
    marginBottom: 4,
  },
  categoryBadgeText: { color: COLORS.text.inverse, fontSize: 10, fontWeight: '700' },
  cardDate: { fontSize: 12, color: COLORS.text.muted },
  pointsBadge: { backgroundColor: '#E8F5E9', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  pointsText: { color: '#2E7D32', fontSize: 12, fontWeight: '700' },
  emptyView: { alignItems: 'center', paddingHorizontal: SPACING.lg },
  emptyEmoji: { fontSize: 50, marginBottom: SPACING.sm },
  emptyTitle: { ...TYPOGRAPHY.subtitle, color: COLORS.text.primary, marginBottom: 6 },
  emptyBody: {
    ...TYPOGRAPHY.body,
    color: COLORS.text.secondary,
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: SPACING.md,
  },
  scanNowButton: {
    backgroundColor: COLORS.accent.berkeleyBlue,
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 20,
  },
  scanNowButtonText: { color: COLORS.text.inverse, fontWeight: '700', fontSize: 15 },
});
