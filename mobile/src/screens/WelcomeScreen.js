import React from 'react';
import { ScrollView, StyleSheet, Text, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { PrimaryButton } from '../components/DesignPrimitives';
import { COLORS } from '../styles/theme';

import OnboardingScreen from './OnboardingScreen';

export default function WelcomeScreen({ onContinue, onContinueWithoutSaving, saving, saveFailed }) {
  let continueLabel = saveFailed ? 'Try again' : 'Continue as guest';
  if (saving) continueLabel = 'Saving…';

  return (
    <SafeAreaView style={styles.screen}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.card}>
          <Text style={styles.title}>Sortify</Text>
          <OnboardingScreen
            descriptionStyle={styles.copy}
            finishAction={(
              <>
                {saveFailed && (
                  <Text style={styles.copy} accessibilityRole="alert" accessibilityLiveRegion="polite">
                    Couldn’t save your progress. The walkthrough may appear again if you continue without saving.
                  </Text>
                )}
                <PrimaryButton onPress={onContinue} disabled={saving}>
                  {continueLabel}
                </PrimaryButton>
                {saveFailed && (
                  <PrimaryButton onPress={onContinueWithoutSaving} subtle>
                    Continue without saving
                  </PrimaryButton>
                )}
              </>
            )}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: '#F4FCF6' },
  content: { flexGrow: 1, paddingTop: 28 },
  card: {
    flexGrow: 1, backgroundColor: COLORS.background.card, borderColor: COLORS.design.border,
    borderWidth: 1, borderRadius: 24, paddingHorizontal: 28, paddingVertical: 34, gap: 18,
  },
  title: { color: COLORS.text.primary, fontSize: 30, fontWeight: '800' },
  copy: { color: COLORS.text.secondary, fontSize: 16, lineHeight: 24, marginBottom: 12 },
});
