// src/screens/ResultScreen.js
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Image } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function ResultScreen({ route, navigation }) {
  const { 
    itemName = 'Item Classified', 
    category = 'compost', 
    confidence = 0.94,
    tip = 'Compostable in Berkeley if certified BPI or lining is plant-based.',
    photoUri = null,
  } = route?.params || {};

  const binColor = COLORS.bins[category.toLowerCase()] || COLORS.bins.landfill;
  const confidencePercent = Math.round(confidence * 100);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {photoUri && (
        <Image source={{ uri: photoUri }} style={styles.thumbnail} />
      )}

      {/* Top Category Banner */}
      <View style={[styles.badge, { backgroundColor: binColor }]}>
        <Text style={styles.badgeText}>{category.toUpperCase()}</Text>
      </View>

      <Text style={styles.itemName}>{itemName}</Text>

      {/* Confidence Score Bar */}
      <View style={styles.confidenceContainer}>
        <View style={styles.confidenceHeader}>
          <Text style={styles.confidenceLabel}>Detection Confidence</Text>
          <Text style={[styles.confidenceValue, { color: binColor }]}>{confidencePercent}%</Text>
        </View>
        <View style={styles.progressBarBackground}>
          <View style={[styles.progressBarFill, { width: `${confidencePercent}%`, backgroundColor: binColor }]} />
        </View>
      </View>

      {/* Disposal Recommendation Card */}
      <View style={styles.tipCard}>
        <Text style={styles.tipTitle}>Disposal Guideline (Berkeley 📍)</Text>
        <Text style={styles.tipBody}>{tip}</Text>
      </View>

      {/* Action Buttons */}
      <TouchableOpacity 
        style={[styles.primaryButton, { backgroundColor: binColor }]}
        onPress={() => navigation.goBack()}
        activeOpacity={0.8}
      >
        <Text style={styles.primaryButtonText}>Scan Another Item</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background.primary },
  content: { padding: SPACING.lg, alignItems: 'center' },
  thumbnail: { width: 140, height: 140, borderRadius: 16, marginBottom: 16, borderWidth: 2, borderColor: '#CBD5E1' },
  badge: { paddingHorizontal: 20, paddingVertical: 8, borderRadius: 20, marginBottom: 12 },
  badgeText: { color: COLORS.text.inverse, fontWeight: 'bold', fontSize: 16, letterSpacing: 0.5 },
  itemName: { ...TYPOGRAPHY.header, textAlign: 'center', marginBottom: 20 },
  confidenceContainer: { width: '100%', marginBottom: 24 },
  confidenceHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  confidenceLabel: { ...TYPOGRAPHY.caption, color: COLORS.text.secondary },
  confidenceValue: { fontWeight: '700', fontSize: 14 },
  progressBarBackground: { height: 10, backgroundColor: '#E2E8F0', borderRadius: 5, overflow: 'hidden' },
  progressBarFill: { height: '100%', borderRadius: 5 },
  tipCard: { backgroundColor: COLORS.background.card, padding: 18, borderRadius: 14, width: '100%', marginBottom: 28, borderWidth: 1, borderColor: '#E2E8F0' },
  tipTitle: { ...TYPOGRAPHY.subtitle, fontSize: 15, marginBottom: 8, color: COLORS.accent.berkeleyBlue },
  tipBody: { ...TYPOGRAPHY.body, color: COLORS.text.secondary, lineHeight: 22 },
  primaryButton: { width: '100%', padding: 16, borderRadius: 14, alignItems: 'center', elevation: 2 },
  primaryButtonText: { color: COLORS.text.inverse, fontWeight: '700', fontSize: 16 },
});
