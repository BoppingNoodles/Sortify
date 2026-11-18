import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { COLORS } from '../styles/theme';

export function PrimaryButton({ children, onPress, disabled = false, subtle = false }) {
  return (
    <TouchableOpacity
      accessibilityRole="button"
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      style={[styles.button, subtle && styles.subtle, disabled && styles.disabled]}
    >
      <Text style={styles.label}>{children}</Text>
    </TouchableOpacity>
  );
}

export function ProgressBar({ value, max, label }) {
  return (
    <View
      accessibilityRole="progressbar"
      accessibilityLabel={label}
      accessibilityValue={{ min: 0, now: Math.min(value, max), max }}
      style={styles.track}
    >
      <View style={[styles.fill, { width: `${Math.min(value / max, 1) * 100}%` }]} />
    </View>
  );
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: COLORS.design.green,
    minHeight: 50,
    borderRadius: 12,
    paddingHorizontal: 18,
    paddingVertical: 13,
    alignItems: 'center',
    justifyContent: 'center',
  },
  subtle: { backgroundColor: COLORS.design.greenTint },
  disabled: { opacity: 0.55 },
  label: { color: '#173208', fontWeight: '800', fontSize: 16, textAlign: 'center' },
  track: { height: 12, borderRadius: 6, backgroundColor: COLORS.design.progress, overflow: 'hidden' },
  fill: { height: '100%', backgroundColor: COLORS.design.green, borderRadius: 6 },
});
