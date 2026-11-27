// src/screens/ResultScreen.js
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView, Image, useColorScheme } from 'react-native';
import { createThemedStyles, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function ResultScreen({ route, navigation }) {
  const { colors, styles } = getStyles(useColorScheme());
  const {
    itemName = 'Item Classified',
    category = 'compost',
    confidence = 0.94,
    bin = null,
    tip = null,
    disposalTip = null,
    location = 'berkeley',
    photoUri = null,
    alternatives = [],
    uncertain = false,
    historySaved,
    savedScan = false,
  } = route?.params || {};
  const notSure = uncertain === true;

  const effectiveTip = disposalTip || tip || 'No disposal guidance is available for this scan.';
  // API bin_color values are display labels ("Green"), not native style colors.
  const binColor = colors.bins[category?.toLowerCase()] || colors.bins.landfill;
  const confidenceScore = typeof confidence === 'number' || typeof confidence === 'string'
    ? Number(confidence)
    : NaN;
  const confidencePercent = Number.isFinite(confidenceScore)
    ? Math.round(Math.max(0, Math.min(1, confidenceScore)) * 100)
    : 0;
  const categoryLabel = (value) => value.charAt(0).toUpperCase() + value.slice(1);
  const otherGuesses = (Array.isArray(alternatives) ? alternatives : [])
    .filter((alt) => typeof alt?.category === 'string' && Number.isFinite(Number(alt.confidence)))
    .slice(0, 2)
    .map((alt) => `${categoryLabel(alt.category)} ${Math.round(Math.max(0, Math.min(1, Number(alt.confidence))) * 100)}%`)
    .join(', ');
  const accentColor = notSure ? colors.design.streakText : binColor;
  const locationLabel = location
    ? location
        .split('-')
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(' ')
    : null;
  const tipHeading = notSure
    ? `If it is ${categoryLabel(category || 'landfill')}`
    : 'Disposal Guideline';

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {photoUri && (
        <Image source={{ uri: photoUri }} style={styles.thumbnail} />
      )}

      {notSure ? (
        <>
          <View style={[styles.badge, styles.notSureBadge]}>
            <Text style={[styles.badgeText, styles.notSureBadgeText]}>NOT SURE</Text>
          </View>
          <Text style={styles.itemName} accessibilityRole="header">Not sure what this is</Text>
          <Text style={styles.notSureBody}>
            {`Best guess: ${categoryLabel(category || 'landfill')}, but the confidence is too low to trust.`}
          </Text>
          {otherGuesses ? (
            <Text style={styles.notSureBody}>{`Could also be: ${otherGuesses}`}</Text>
          ) : null}
          <View style={[styles.tipCard, styles.notSureCard]}>
            <Text style={[styles.tipTitle, styles.notSureTitle]}>Try another photo</Text>
            <Text style={styles.tipBody}>
              {`Fill most of the frame with one item, in good light, against a plain background. If it's still unclear, check the Municipal Rules tab for ${locationLabel || 'your city'}.`}
            </Text>
          </View>
        </>
      ) : (
        <>
          {/* Top Category Banner */}
          <View style={[styles.badge, { backgroundColor: binColor }]}>
            <Text style={styles.badgeText}>{(category || 'LANDFILL').toUpperCase()}</Text>
          </View>

          <Text style={styles.itemName}>{itemName}</Text>
          {bin ? <Text style={styles.binName}>Target: {bin}</Text> : null}
        </>
      )}

      {/* Confidence Score Bar */}
      <View style={styles.confidenceContainer}>
        <View style={styles.confidenceHeader}>
          <Text style={styles.confidenceLabel}>Detection Confidence</Text>
          <Text style={[styles.confidenceValue, { color: accentColor }]}>{confidencePercent}%</Text>
        </View>
        <View style={styles.progressBarBackground}>
          <View style={[styles.progressBarFill, { width: `${confidencePercent}%`, backgroundColor: accentColor }]} />
        </View>
      </View>

      {/* Disposal Recommendation Card */}
      <View style={styles.tipCard}>
        <Text style={styles.tipTitle}>{locationLabel ? `${tipHeading} (${locationLabel} 📍)` : tipHeading}</Text>
        <Text style={styles.tipBody}>{effectiveTip}</Text>
      </View>

      {notSure && (
        <Text style={styles.historyWarning}>Not added to History.</Text>
      )}

      {historySaved === false && (
        <Text accessibilityRole="alert" style={styles.historyWarning}>
          {'This scan couldn’t be saved to History.'}
        </Text>
      )}

      {/* Action Buttons */}
      <TouchableOpacity 
        style={styles.primaryButton}
        onPress={() => navigation.goBack()}
        accessibilityRole="button"
        activeOpacity={0.8}
      >
        <Text style={styles.primaryButtonText}>{savedScan ? 'Back to History' : notSure ? 'Retake Photo' : 'Scan Another Item'}</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const getStyles = createThemedStyles((colors) => StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background.primary },
  content: { padding: SPACING.lg, paddingBottom: SPACING.xl, alignItems: 'center' },
  thumbnail: { width: 140, height: 140, borderRadius: 16, marginBottom: 16, borderWidth: 2, borderColor: colors.design.thumbnailBorder },
  badge: { paddingHorizontal: 20, paddingVertical: 8, borderRadius: 20, marginBottom: 12 },
  badgeText: { color: colors.text.inverse, fontWeight: 'bold', fontSize: 16, letterSpacing: 0.5 },
  itemName: { ...TYPOGRAPHY.header, color: colors.text.primary, textAlign: 'center', marginBottom: 6 },
  binName: { fontSize: 15, fontWeight: '600', color: colors.text.secondary, marginBottom: 18 },
  confidenceContainer: { width: '100%', marginBottom: 24 },
  confidenceHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  confidenceLabel: { ...TYPOGRAPHY.caption, color: colors.text.secondary },
  confidenceValue: { fontWeight: '700', fontSize: 14 },
  progressBarBackground: { height: 10, backgroundColor: colors.design.border, borderRadius: 5, overflow: 'hidden' },
  progressBarFill: { height: '100%', borderRadius: 5 },
  tipCard: { backgroundColor: colors.background.card, padding: 18, borderRadius: 14, width: '100%', marginBottom: 28, borderWidth: 1, borderColor: colors.design.border },
  tipTitle: { ...TYPOGRAPHY.subtitle, fontSize: 15, marginBottom: 8, color: colors.accent.berkeleyBlue },
  tipBody: { ...TYPOGRAPHY.body, color: colors.text.secondary, lineHeight: 22 },
  historyWarning: { ...TYPOGRAPHY.caption, color: colors.text.secondary, marginBottom: SPACING.md },
  notSureBadge: { backgroundColor: colors.design.streak, borderWidth: 1, borderColor: colors.design.streakBorder },
  notSureBadgeText: { color: colors.design.streakText },
  notSureBody: { ...TYPOGRAPHY.body, color: colors.text.secondary, textAlign: 'center', marginBottom: 10 },
  notSureCard: { backgroundColor: colors.design.streak, borderColor: colors.design.streakBorder, marginTop: 8, marginBottom: 20 },
  notSureTitle: { color: colors.design.streakText },
  primaryButton: { backgroundColor: colors.design.green, width: '100%', padding: 16, borderRadius: 14, alignItems: 'center', elevation: 2 },
  primaryButtonText: { color: colors.design.onGreen, fontWeight: '700', fontSize: 16 },
}));
