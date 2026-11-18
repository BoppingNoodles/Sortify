import React, { useState } from 'react';
import { ScrollView, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';
import { PrimaryButton } from '../components/DesignPrimitives';
import { fetchLocationRules } from '../services/api';
import { MUNICIPALITIES } from '../services/municipalities';
import { COLORS } from '../styles/theme';

const GROUPS = [
  { label: 'Compost', categories: ['compost'] },
  { label: 'Landfill', categories: ['landfill'] },
  { label: 'Recycling', categories: ['plastic', 'paper', 'glass'] },
];

export default function RulesScreen() {
  const [city, setCity] = useState('berkeley');
  const [choosingCity, setChoosingCity] = useState(false);
  const [group, setGroup] = useState(null);
  const [rules, setRules] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = async () => {
    setLoading(true);
    setError(null);
    setRules(null);
    try {
      const response = await fetchLocationRules(city);
      if (!response?.rules || typeof response.rules !== 'object' || Array.isArray(response.rules)) {
        throw new Error('Invalid municipal rules response.');
      }
      setRules(response.rules);
    } catch {
      setError('Could not load municipal rules. Try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView edges={['top', 'left', 'right']} style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text accessibilityRole="header" style={styles.title}>Municipal Rules</Text>
        <TouchableOpacity
          accessibilityRole="button"
          accessibilityState={{ expanded: choosingCity }}
          disabled={loading}
          onPress={() => setChoosingCity(!choosingCity)}
          style={styles.location}
        >
          <View accessible={false} style={styles.marker}><Ionicons name="location-outline" size={23} color="#FFFFFF" /></View>
          <View>
            <Text style={styles.caption}>Sorting location</Text>
            <Text style={styles.city}>{MUNICIPALITIES[city]}, CA</Text>
          </View>
        </TouchableOpacity>

        {choosingCity && Object.entries(MUNICIPALITIES).map(([value, name]) => (
          <TouchableOpacity
            key={value}
            accessibilityRole="button"
            accessibilityState={{ selected: city === value }}
            disabled={loading}
            onPress={() => { setCity(value); setChoosingCity(false); setRules(null); setError(null); }}
            style={styles.row}
          >
            <Text style={styles.label}>{name}</Text>
          </TouchableOpacity>
        ))}

        <View style={styles.groups}>
          {GROUPS.map((entry) => (
            <TouchableOpacity
              key={entry.label}
              accessibilityRole="button"
              accessibilityState={{ selected: group === entry }}
              style={[styles.row, group === entry && styles.selected]}
              onPress={() => setGroup(group === entry ? null : entry)}
            >
              <Text style={styles.badge}>{entry.label[0]}</Text>
              <Text style={styles.label}>{entry.label}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <PrimaryButton disabled={loading} onPress={search}>{loading ? 'Loading rules…' : 'Search'}</PrimaryButton>
        {error && <Text accessibilityRole="alert" style={styles.caption}>{error}</Text>}
        {rules && (group ? [group] : GROUPS).map((entry) => (
          <View key={entry.label} style={styles.details}>
            <Text accessibilityRole="header" style={styles.label}>{entry.label}</Text>
            {entry.categories.map((category) => (
              <Text key={category} style={styles.rule}>
                {entry.categories.length > 1 && <Text style={styles.label}>{category[0].toUpperCase() + category.slice(1)}. </Text>}
                {typeof rules[category] === 'string' && rules[category] ? rules[category] : 'No guidance available.'}
              </Text>
            ))}
          </View>
        ))}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: COLORS.background.card },
  content: { padding: 20, paddingTop: 24, gap: 14 },
  title: { color: COLORS.text.primary, fontWeight: '800', fontSize: 26, marginBottom: 8 },
  location: { backgroundColor: COLORS.design.blueTint, borderRadius: 20, padding: 16, flexDirection: 'row', alignItems: 'center', gap: 14 },
  marker: { backgroundColor: '#17AECB', borderRadius: 24, width: 46, height: 46, justifyContent: 'center', alignItems: 'center' },
  caption: { color: COLORS.text.secondary, fontSize: 13 },
  city: { color: COLORS.accent.berkeleyBlue, fontWeight: '800', marginTop: 4 },
  groups: { gap: 10, marginVertical: 8 },
  row: { flexDirection: 'row', alignItems: 'center', gap: 12, minHeight: 54, padding: 12, borderRadius: 13, borderWidth: 1, borderColor: COLORS.design.border },
  selected: { backgroundColor: COLORS.design.greenTint, borderColor: COLORS.design.greenText },
  badge: { color: COLORS.text.secondary, backgroundColor: COLORS.background.surface, minWidth: 30, borderRadius: 8, padding: 7, textAlign: 'center', fontWeight: '800' },
  label: { color: COLORS.text.primary, fontWeight: '800' },
  details: { padding: 14, borderColor: COLORS.design.border, borderWidth: 1, borderRadius: 13, gap: 8 },
  rule: { color: COLORS.text.secondary, lineHeight: 21 },
});
