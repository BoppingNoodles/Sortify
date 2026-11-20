import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View, useColorScheme } from 'react-native';
import { createThemedStyles } from '../styles/theme';

export function PrimaryButton({ children, onPress, disabled = false, subtle = false }) {
  const { styles } = getStyles(useColorScheme());
  return (
    <TouchableOpacity
      accessibilityRole="button"
      accessibilityState={{ disabled }}
      disabled={disabled}
      onPress={onPress}
      style={[styles.button, subtle && styles.subtle, disabled && styles.disabled]}
    >
      <Text style={[styles.label, subtle && styles.subtleLabel]}>{children}</Text>
    </TouchableOpacity>
  );
}

export function ProgressBar({ value, max, label }) {
  const { styles } = getStyles(useColorScheme());
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

const getStyles = createThemedStyles((colors) => StyleSheet.create({
  button: {
    backgroundColor: colors.design.green,
    minHeight: 50,
    borderRadius: 12,
    paddingHorizontal: 18,
    paddingVertical: 13,
    alignItems: 'center',
    justifyContent: 'center',
  },
  subtle: { backgroundColor: colors.design.greenTint },
  subtleLabel: { color: colors.design.greenText },
  disabled: { opacity: 0.55 },
  label: { color: colors.design.onGreen, fontWeight: '800', fontSize: 16, textAlign: 'center' },
  track: { height: 12, borderRadius: 6, backgroundColor: colors.design.progress, overflow: 'hidden' },
  fill: { height: '100%', backgroundColor: colors.design.green, borderRadius: 6 },
}));
