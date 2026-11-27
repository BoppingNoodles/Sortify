// src/screens/HistoryScreen.js
import React, { useCallback, useRef, useState } from 'react';
import {
  StyleSheet,
  useColorScheme,
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
import { clearHistory, deleteScanRecord, loadSavedScans } from '../services/storage';
import { createThemedStyles, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function HistoryScreen({ navigation }) {
  const { colors, styles } = getStyles(useColorScheme());
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [deletion, setDeletion] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState(null);
  const deleteInProgress = useRef(false);
  const requestVersion = useRef(0);

  const fetchHistory = useCallback(async () => {
    const version = ++requestVersion.current;
    try {
      const data = await loadSavedScans();
      if (version === requestVersion.current) setScans(data);
    } catch (error) {
      if (version === requestVersion.current) {
        console.warn('Failed to load history:', error);
        setScans([]);
      }
    } finally {
      if (version === requestVersion.current) {
        setLoading(false);
        setRefreshing(false);
      }
    }
  }, []);

  useFocusEffect(useCallback(() => {
    setLoading(true);
    setRefreshing(false);
    fetchHistory();
    return () => { requestVersion.current += 1; };
  }, [fetchHistory]));

  const onRefresh = () => {
    setRefreshing(true);
    fetchHistory();
  };

  const confirmDeletion = async () => {
    if (!deletion || deleteInProgress.current) return;
    deleteInProgress.current = true;
    setDeleting(true);
    setDeleteError(null);
    try {
      const deleted = deletion.all ? await clearHistory() : await deleteScanRecord(deletion.id);
      if (!deleted) {
        setDeleteError('Could not delete scan history. Try again.');
        return;
      }
      setDeletion(null);
      await fetchHistory();
    } finally {
      deleteInProgress.current = false;
      setDeleting(false);
    }
  };

  const renderItem = ({ item }) => {
    const itemName = item.item_name || item.itemName || 'Waste Item';
    const category = (item.category || item.bin || 'landfill').toLowerCase();
    const binColor = colors.bins[category] || colors.bins.landfill;
    const formattedDate = item.timestamp
      ? new Date(item.timestamp).toLocaleString()
      : 'Today';
    const photoUri = item.thumbnail ? 'data:image/jpeg;base64,' + item.thumbnail : null;

    return (
      <View style={styles.scanCard}>
        <TouchableOpacity
          style={styles.scanDetails}
          accessibilityRole="button"
          accessibilityLabel={`View ${itemName} scan from ${formattedDate}`}
          disabled={deleting}
          onPress={() => navigation.navigate('ResultModal', {
            itemName,
            category,
            confidence: item.confidence,
            disposalTip: item.disposal_tip,
            location: item.location ?? null,
            photoUri,
            savedScan: true,
          })}
        >
          {photoUri ? (
            <Image source={{ uri: photoUri }} style={styles.cardImage} />
          ) : (
            <View style={[styles.cardPlaceholder, { borderColor: binColor }]}>
              <Text style={styles.placeholderEmoji}>♻️</Text>
            </View>
          )}
          <View style={styles.cardContent}>
            <Text style={styles.cardTitle} numberOfLines={1}>{itemName}</Text>
            <View style={[styles.categoryBadge, { backgroundColor: binColor }]}>
              <Text style={styles.categoryBadgeText}>{category.toUpperCase()}</Text>
            </View>
            <Text style={styles.cardDate}>{formattedDate}</Text>
          </View>
          <View style={styles.pointsBadge}>
            <Text style={styles.pointsText}>+10 pts</Text>
          </View>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.deleteButton}
          accessibilityRole="button"
          accessibilityLabel={`Delete ${itemName} scan from ${formattedDate}`}
          disabled={deleting}
          onPress={() => { setDeleteError(null); setDeletion({ id: item.id, itemName }); }}
        >
          <Text style={styles.deleteText}>Delete</Text>
        </TouchableOpacity>
      </View>
    );
  };

  return (
    <SafeAreaView edges={['left', 'right', 'bottom']} style={styles.container}>
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
            <Text style={styles.statsCtaText}>Impact stats</Text>
          </TouchableOpacity>
        )}
      </View>

      {!loading && scans.length > 0 && (
        <View style={styles.historyActions}>
          {deletion ? (
            <>
              <Text accessibilityRole="header" style={styles.cardTitle}>
                {deletion.all ? 'Clear all scan history?' : `Delete the ${deletion.itemName} scan?`}
              </Text>
              <Text style={styles.cardDate}>This updates your local history, points, and streak.</Text>
              <View style={styles.confirmActions}>
                <TouchableOpacity accessibilityRole="button" style={styles.deleteButton} disabled={deleting}
                  onPress={() => { setDeletion(null); setDeleteError(null); }}>
                  <Text style={styles.statsCtaText}>Cancel</Text>
                </TouchableOpacity>
                <TouchableOpacity accessibilityRole="button" style={styles.deleteButton} disabled={deleting}
                  onPress={confirmDeletion}>
                  <Text style={styles.deleteText}>{deleting ? 'Deleting…' : deletion.all ? 'Clear all scans' : 'Delete scan'}</Text>
                </TouchableOpacity>
              </View>
            </>
          ) : (
            <TouchableOpacity accessibilityRole="button" style={styles.deleteButton} onPress={() => setDeletion({ all: true })}>
              <Text style={styles.deleteText}>Clear history</Text>
            </TouchableOpacity>
          )}
          {deleteError && <Text accessibilityRole="alert" style={styles.deleteText}>{deleteError}</Text>}
        </View>
      )}

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator
            accessibilityLabel="Loading scan history"
            size="large"
            color={colors.accent.berkeleyBlue}
          />
        </View>
      ) : (
        <FlatList
          data={scans}
          keyExtractor={(item, index) => item.id || `scan_${index}`}
          renderItem={renderItem}
          contentContainerStyle={scans.length === 0 ? styles.emptyContainer : styles.listContent}
          refreshControl={(
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              tintColor={colors.accent.berkeleyBlue}
              colors={[colors.accent.berkeleyBlue]}
              progressBackgroundColor={colors.background.card}
            />
          )}
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

const getStyles = createThemedStyles((colors) => StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background.primary },
  header: {
    paddingHorizontal: SPACING.md,
    paddingVertical: SPACING.md,
    backgroundColor: colors.background.card,
    borderBottomWidth: 1,
    borderBottomColor: colors.design.border,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: { ...TYPOGRAPHY.header, color: colors.accent.berkeleyBlue },
  statsCtaButton: {
    backgroundColor: colors.design.blueTint,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 14,
    borderWidth: 1,
    borderColor: colors.design.border,
  },
  statsCtaText: { fontSize: 13, fontWeight: '700', color: colors.accent.berkeleyBlue },
  historyActions: { paddingHorizontal: SPACING.md, backgroundColor: colors.background.card },
  confirmActions: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  deleteButton: { minHeight: 44, paddingHorizontal: 10, alignItems: 'center', justifyContent: 'center', alignSelf: 'flex-start' },
  deleteText: { fontSize: 13, fontWeight: '700', color: colors.text.primary },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  listContent: { padding: SPACING.md },
  emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: SPACING.lg },
  scanCard: {
    flexDirection: 'row',
    backgroundColor: colors.background.card,
    borderRadius: 14,
    padding: SPACING.md,
    marginBottom: SPACING.sm,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
    borderWidth: 1,
    borderColor: colors.design.border,
  },
  scanDetails: { flex: 1, flexDirection: 'row', alignItems: 'center' },
  cardImage: { width: 56, height: 56, borderRadius: 10, marginRight: SPACING.md },
  cardPlaceholder: {
    width: 56,
    height: 56,
    borderRadius: 10,
    backgroundColor: colors.background.surface,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: SPACING.md,
    borderWidth: 2,
  },
  placeholderEmoji: { fontSize: 24 },
  cardContent: { flex: 1, justifyContent: 'center' },
  cardTitle: { ...TYPOGRAPHY.body, fontWeight: '700', color: colors.text.primary, marginBottom: 4 },
  categoryBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 6,
    marginBottom: 4,
  },
  categoryBadgeText: { color: colors.text.inverse, fontSize: 10, fontWeight: '700' },
  cardDate: { fontSize: 12, color: colors.text.muted },
  pointsBadge: { backgroundColor: colors.design.points, paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  pointsText: { color: colors.design.pointsText, fontSize: 12, fontWeight: '700' },
  emptyView: { alignItems: 'center', paddingHorizontal: SPACING.lg },
  emptyEmoji: { fontSize: 50, marginBottom: SPACING.sm },
  emptyTitle: { ...TYPOGRAPHY.subtitle, color: colors.text.primary, marginBottom: 6 },
  emptyBody: {
    ...TYPOGRAPHY.body,
    color: colors.text.secondary,
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: SPACING.md,
  },
  scanNowButton: {
    backgroundColor: colors.design.green,
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 20,
  },
  scanNowButtonText: { color: colors.design.onGreen, fontWeight: '700', fontSize: 15 },
}));
