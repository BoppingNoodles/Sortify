import React, { useMemo, useState } from 'react';
import { PanResponder, Pressable, StyleSheet, Text, View } from 'react-native';
import { useTheme } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { PrimaryButton } from '../components/DesignPrimitives';

const SLIDES = [
  {
    icon: 'camera-outline',
    title: 'Snap your waste',
    description: 'Take a photo of one item and Sortify will suggest a bin.',
  },
  {
    icon: 'location-outline',
    title: 'Get local guidance',
    description: 'Choose your city to see which bin to use and how to prepare the item.',
  },
  {
    icon: 'flame-outline',
    title: 'Build sorting streaks',
    description: 'Earn points as you scan and see your progress in your profile.',
  },
];

const LAST_SLIDE = SLIDES.length - 1;

export default function OnboardingScreen({ descriptionStyle, finishAction }) {
  const [page, setPage] = useState(0);
  const { colors } = useTheme();
  const slide = SLIDES[page];
  const swipe = useMemo(() => PanResponder.create({
    onMoveShouldSetPanResponder: (_event, { dx, dy }) =>
      Math.abs(dx) > 16 && Math.abs(dx) > Math.abs(dy) * 1.5,
    onPanResponderRelease: (_event, { dx }) => {
      if (dx < -48) setPage((current) => Math.min(current + 1, LAST_SLIDE));
      if (dx > 48) setPage((current) => Math.max(current - 1, 0));
    },
  }), []);

  return (
    <>
      <View style={styles.slide} {...swipe.panHandlers}>
        <View style={[styles.icon, { borderColor: colors.border }]} accessible={false}>
          <Ionicons name={slide.icon} size={38} color={colors.text} accessible={false} />
        </View>
        <Text style={[styles.title, { color: colors.text }]} accessibilityRole="header">
          {slide.title}
        </Text>
        <Text style={[descriptionStyle, styles.copy]}>{slide.description}</Text>
      </View>

      <Text style={[styles.page, { color: colors.text }]} accessibilityLiveRegion="polite">
        {page + 1} of {SLIDES.length}
      </Text>
      {page === LAST_SLIDE
        ? finishAction
        : <PrimaryButton onPress={() => setPage(page + 1)}>Next</PrimaryButton>}
      {page > 0 && (
        <Pressable
          onPress={() => setPage(page - 1)}
          accessibilityRole="button"
          style={styles.back}
        >
          <Text style={[styles.backLabel, { color: colors.text }]}>Back</Text>
        </Pressable>
      )}
    </>
  );
}

const styles = StyleSheet.create({
  slide: { flexGrow: 1, justifyContent: 'center', alignItems: 'center', gap: 14, paddingVertical: 24 },
  icon: {
    width: 82, height: 82, borderWidth: 1, borderRadius: 22,
    justifyContent: 'center', alignItems: 'center',
  },
  title: { fontSize: 30, fontWeight: '800', textAlign: 'center' },
  copy: { maxWidth: 360, textAlign: 'center' },
  page: { fontSize: 14, fontWeight: '600', textAlign: 'center', marginBottom: 6 },
  back: { alignSelf: 'center', minHeight: 44, justifyContent: 'center', paddingHorizontal: 18 },
  backLabel: { fontSize: 15, fontWeight: '700' },
});
