// src/screens/ScanScreen.js
import React, { useCallback, useEffect, useLayoutEffect, useRef, useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Image,
  ScrollView,
  ActivityIndicator,
  Alert,
  AppState,
  Linking,
} from 'react-native';
import { CameraView, getCameraPermissionsAsync, requestCameraPermissionsAsync } from 'expo-camera';
import { useFocusEffect } from '@react-navigation/native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { COLORS, SPACING } from '../styles/theme';
import { classifyImage } from '../services/api';
import { saveScanRecord } from '../services/storage';

const SUPPORTED_CITIES = ['berkeley', 'san-francisco', 'oakland', 'san-jose', 'sunnyvale'];

function CameraPreview({ formattedCity, onCycleCity, onCapture, onPreviewReady, isBusy }) {
  const cameraRef = useRef(null);
  const [isReady, setIsReady] = useState(false);

  const handleReady = () => {
    if (!cameraRef.current) return;
    onPreviewReady(cameraRef.current);
    setIsReady(true);
  };

  const handleCapture = () => {
    if (!isReady || !cameraRef.current) return;
    return onCapture(cameraRef.current);
  };

  return (
    <>
      <CameraView style={styles.camera} ref={cameraRef} onCameraReady={handleReady} />
      <SafeAreaView edges={['top', 'left', 'right']} style={styles.cameraOverlay}
        pointerEvents="box-none">
        {/* Top Bar with Municipality Selector */}
        <View style={styles.topBar}>
          <TouchableOpacity
            style={styles.cityPill}
            onPress={onCycleCity}
            accessibilityRole="button"
            accessibilityLabel={`Sorting city: ${formattedCity}`}
            accessibilityHint="Switches to the next supported city"
            activeOpacity={0.7}
          >
            <Text style={styles.cityPillText}>📍 {formattedCity}</Text>
          </TouchableOpacity>
        </View>

        {/* Target Reticle Overlay */}
        <View style={styles.reticleContainer}>
          <View style={styles.reticleBox} />
          <Text style={styles.reticleHint}>Center item inside frame</Text>
        </View>

        {/* Shutter Button Controls */}
        <View style={styles.bottomControls}>
          <TouchableOpacity
            style={styles.shutterButton}
            onPress={handleCapture}
            disabled={!isReady || isBusy}
            accessibilityRole="button"
            accessibilityLabel="Take photo"
            activeOpacity={0.7}
          >
            <View style={styles.shutterInner} />
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    </>
  );
}

export default function ScanScreen({ navigation }) {
  const [permission, setPermission] = useState(null);
  const [permissionError, setPermissionError] = useState(null);
  const [permissionCheck, setPermissionCheck] = useState(0);
  const [checkedGeneration, setCheckedGeneration] = useState(null);
  const [generation, setGeneration] = useState(0);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isBusy, setIsBusy] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const [isActive, setIsActive] = useState(AppState.currentState === 'active');
  const [selectedCity, setSelectedCity] = useState('berkeley');
  const mounted = useRef(false);
  const screen = useRef({ focused: false, active: isActive, generation: 0 });
  const operation = useRef(null);
  const permissionRequest = useRef(null);

  const isCurrent = useCallback((generation) => (
    mounted.current && screen.current.focused && screen.current.active &&
    screen.current.generation === generation
  ), []);

  useLayoutEffect(() => {
    mounted.current = true;
    return () => { mounted.current = false; };
  }, []);

  const invalidate = useCallback(() => {
    screen.current.generation += 1;
    if (!mounted.current) return;
    setGeneration(screen.current.generation);
    setIsAnalyzing(false);
    // A scan whose save has started must not be submitted again on return.
    if (operation.current?.saving) setCapturedPhoto(null);
  }, []);

  useFocusEffect(useCallback(() => {
    screen.current.focused = true;
    setIsFocused(true);
    setIsBusy(Boolean(operation.current));
    return () => {
      screen.current.focused = false;
      invalidate();
      if (mounted.current) setIsFocused(false);
    };
  }, [invalidate]));

  useEffect(() => {
    const updateActivity = (state) => {
      const active = state === 'active';
      if (screen.current.active === active) return;
      screen.current.active = active;
      if (!active) invalidate();
      else setIsBusy(Boolean(operation.current));
      setIsActive(active);
    };
    const subscription = AppState.addEventListener('change', updateActivity);
    updateActivity(AppState.currentState);
    return () => subscription.remove();
  }, [invalidate]);

  useEffect(() => {
    if (!isFocused || !isActive) return;
    let current = true;
    setPermissionError(null);
    setCheckedGeneration(null);
    const readPermission = async () => {
      // Android can resume before Expo records the permission prompt's result.
      const pending = permissionRequest.current;
      if (pending) await pending.catch(() => {});
      if (!current || !isCurrent(generation)) return;

      try {
        const status = await getCameraPermissionsAsync();
        if (!current || !isCurrent(generation)) return;
        setPermission(status);
        setCheckedGeneration(generation);
      } catch {
        if (current && isCurrent(generation)) {
          setPermissionError('Could not check camera access. Please try again.');
        }
      }
    };
    readPermission();
    return () => { current = false; };
  }, [generation, isFocused, isActive, isCurrent, permissionCheck]);

  const handlePermission = async () => {
    if (!isCurrent(generation) || permissionRequest.current) return;
    const needsSettings = permission.canAskAgain === false;
    setPermissionError(null);
    try {
      if (needsSettings) {
        await Linking.openSettings();
      } else {
        const pending = requestCameraPermissionsAsync();
        permissionRequest.current = pending;
        const status = await pending;
        if (isCurrent(generation)) setPermission(status);
      }
    } catch {
      if (!isCurrent(generation)) return;
      setPermissionError(needsSettings
        ? 'Could not open Settings. Open it manually and allow camera access for Sortify.'
        : 'Could not request camera access. Please try again.');
    } finally {
      if (!needsSettings) permissionRequest.current = null;
    }
  };

  const beginOperation = (camera = null) => {
    const { generation } = screen.current;
    if (!isCurrent(generation) || operation.current) return null;
    const pending = { generation, saving: false, camera };
    operation.current = pending;
    setIsBusy(true);
    return pending;
  };

  const finishOperation = (pending) => {
    if (operation.current !== pending) return;
    operation.current = null;
    if (!mounted.current || !screen.current.focused || !screen.current.active) return;
    setIsBusy(false);
    if (isCurrent(pending.generation)) setIsAnalyzing(false);
  };

  const handlePreviewReady = (camera) => {
    const pending = operation.current;
    // Android can abandon the previous view's capture promise during teardown.
    if (pending?.camera && pending.camera !== camera && !isCurrent(pending.generation)) {
      finishOperation(pending);
    }
  };

  if (!permission || checkedGeneration !== generation) {
    return (
      <SafeAreaView edges={['top', 'left', 'right']} style={styles.centered}>
        {permissionError ? (
          <>
            <Text style={styles.permissionBody} accessibilityRole="alert">{permissionError}</Text>
            <TouchableOpacity style={styles.primaryButton} accessibilityRole="button"
              onPress={() => setPermissionCheck((previous) => previous + 1)}>
              <Text style={styles.buttonText}>Try Again</Text>
            </TouchableOpacity>
          </>
        ) : (
          <>
            <ActivityIndicator size="large" color={COLORS.accent.berkeleyBlue} />
            <Text style={styles.statusText}>Checking camera access…</Text>
          </>
        )}
      </SafeAreaView>
    );
  }

  if (!permission.granted) {
    const needsSettings = permission.canAskAgain === false;
    return (
      <SafeAreaView edges={['top', 'left', 'right']} style={styles.permissionArea}>
        <ScrollView contentContainerStyle={styles.centered}>
          <Text style={styles.permissionTitle}>Camera Access Required</Text>
          <Text style={styles.permissionBody}>
            {needsSettings
              ? 'Allow camera access in system Settings to scan waste items.'
              : 'Allow camera access to take a photo and identify its bin.'}
          </Text>
          {permissionError && (
            <Text style={styles.permissionBody} accessibilityRole="alert">{permissionError}</Text>
          )}
          <TouchableOpacity style={styles.primaryButton} onPress={handlePermission}
            accessibilityRole="button" activeOpacity={0.8}>
            <Text style={styles.buttonText}>{needsSettings ? 'Open Settings' : 'Grant Permission'}</Text>
          </TouchableOpacity>
        </ScrollView>
      </SafeAreaView>
    );
  }

  const handleCapture = async (camera) => {
    const pending = beginOperation(camera);
    if (!pending) return;
    try {
      const photo = await camera.takePictureAsync({
        quality: 0.8,
        skipProcessing: false,
      });
      if (photo?.uri && isCurrent(pending.generation)) {
        setCapturedPhoto(photo);
      }
    } catch (error) {
      if (isCurrent(pending.generation)) {
        console.error('Failed to capture photo:', error);
        Alert.alert('Camera Error', 'Could not capture photo. Please try again.');
      }
    } finally {
      finishOperation(pending);
    }
  };

  const handleAnalyze = async () => {
    if (!capturedPhoto?.uri) return;
    const pending = beginOperation();
    if (!pending) return;
    setIsAnalyzing(true);
    try {
      const result = await classifyImage(capturedPhoto.uri, selectedCity);
      if (!isCurrent(pending.generation)) return;

      if (
        !result ||
        typeof result.item_name !== 'string' ||
        !result.item_name.trim() ||
        typeof result.category !== 'string' ||
        !Object.hasOwn(COLORS.bins, result.category) ||
        !Number.isFinite(result.confidence) ||
        result.confidence < 0 ||
        result.confidence > 1 ||
        typeof result.disposal_tip !== 'string' ||
        !result.disposal_tip.trim() ||
        (result.bin != null && typeof result.bin !== 'string') ||
        (result.bin_color != null && typeof result.bin_color !== 'string') ||
        (result.location != null && typeof result.location !== 'string')
      ) {
        throw new Error('Classification server returned an invalid response.');
      }

      pending.saving = true;
      const savedRecord = await saveScanRecord(result);
      if (!isCurrent(pending.generation)) return;
      const resultParams = {
        itemName: result.item_name,
        category: result.category,
        confidence: result.confidence,
        bin: result.bin || result.bin_color || null,
        binColor: result.bin_color || null,
        disposalTip: result.disposal_tip,
        tip: result.disposal_tip,
        location: result.location || selectedCity,
        alternatives: result.alternatives || [],
        photoUri: capturedPhoto.uri,
        historySaved: savedRecord !== null,
      };

      setCapturedPhoto(null);
      navigation.navigate('ResultModal', resultParams);
    } catch (error) {
      if (!isCurrent(pending.generation)) return;
      console.error('Classification request failed:', error);
      Alert.alert(
        'Scan Failed',
        error.message || 'Unable to analyze image. Please ensure your backend server is running.',
        [
          { text: 'Retake', style: 'cancel', onPress: () => {
            if (isCurrent(pending.generation)) handleRetake();
          } },
          { text: 'Try Again', onPress: () => {
            if (isCurrent(pending.generation)) return handleAnalyze();
          } },
        ]
      );
    } finally {
      finishOperation(pending);
    }
  };

  const handleRetake = () => {
    if (operation.current) return;
    setCapturedPhoto(null);
  };

  const handleCycleCity = () => {
    const currentIndex = SUPPORTED_CITIES.indexOf(selectedCity);
    const nextCity = SUPPORTED_CITIES[(currentIndex + 1) % SUPPORTED_CITIES.length];
    setSelectedCity(nextCity);
  };

  const formattedCity = selectedCity.replace('-', ' ').toUpperCase();
  const showCamera = isFocused && isActive && !capturedPhoto;

  return (
    <View style={styles.container}>
      {capturedPhoto ? (
        <View style={styles.previewContainer}>
          <Image source={{ uri: capturedPhoto.uri }} style={styles.previewImage} />

          {isAnalyzing ? (
            <View style={styles.analyzingOverlay}>
              <ActivityIndicator size="large" color="#FFFFFF" />
              <Text style={styles.analyzingText}>Analyzing waste item with AI...</Text>
              <Text style={styles.analyzingSubtext}>Checking {formattedCity} sorting rules</Text>
            </View>
          ) : (
            <SafeAreaView edges={['left', 'right']} style={styles.previewControls}>
              <View style={styles.previewButtons}>
                <TouchableOpacity
                  style={styles.retakeButton}
                  onPress={handleRetake}
                  disabled={isBusy}
                  accessibilityRole="button"
                  activeOpacity={0.8}
                >
                  <Text style={styles.retakeButtonText}>Retake</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  style={styles.analyzeButton}
                  onPress={handleAnalyze}
                  disabled={isBusy}
                  accessibilityRole="button"
                  activeOpacity={0.8}
                >
                  <Text style={styles.analyzeButtonText}>Identify Bin</Text>
                </TouchableOpacity>
              </View>
            </SafeAreaView>
          )}
        </View>
      ) : showCamera ? (
        <CameraPreview
          formattedCity={formattedCity}
          onCycleCity={handleCycleCity}
          onCapture={handleCapture}
          onPreviewReady={handlePreviewReady}
          isBusy={isBusy}
        />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
  centered: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.lg,
    backgroundColor: COLORS.background.primary,
  },
  permissionArea: {
    flex: 1,
    backgroundColor: COLORS.background.primary,
  },
  statusText: {
    marginTop: 12,
    color: COLORS.text.secondary,
    fontSize: 14,
  },
  permissionTitle: {
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 8,
    color: COLORS.text.primary,
  },
  permissionBody: {
    fontSize: 14,
    color: COLORS.text.secondary,
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 20,
  },
  primaryButton: {
    backgroundColor: COLORS.accent.berkeleyBlue,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 10,
  },
  buttonText: {
    color: '#FFFFFF',
    fontWeight: '700',
    fontSize: 15,
  },
  camera: {
    flex: 1,
  },
  cameraOverlay: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
  },
  topBar: {
    flexDirection: 'row',
    justifyContent: 'center',
  },
  cityPill: {
    flexShrink: 1,
    minHeight: 48,
    justifyContent: 'center',
    backgroundColor: 'rgba(15, 23, 42, 0.72)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.25)',
  },
  cityPillText: {
    color: '#F8FAFC',
    fontWeight: '600',
    fontSize: 13,
    letterSpacing: 0.5,
    textAlign: 'center',
  },
  reticleContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  reticleBox: {
    flexShrink: 1,
    width: '80%',
    maxWidth: 250,
    height: 250,
    borderWidth: 2,
    borderColor: 'rgba(255, 255, 255, 0.75)',
    borderRadius: 18,
    borderStyle: 'dashed',
  },
  reticleHint: {
    color: 'rgba(255, 255, 255, 0.85)',
    marginTop: 14,
    fontSize: 13,
    fontWeight: '500',
    letterSpacing: 0.2,
    textAlign: 'center',
  },
  bottomControls: {
    alignItems: 'center',
  },
  shutterButton: {
    width: 76,
    height: 76,
    borderRadius: 38,
    borderWidth: 4,
    borderColor: '#FFFFFF',
    backgroundColor: 'transparent',
    justifyContent: 'center',
    alignItems: 'center',
  },
  shutterInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#FFFFFF',
  },
  previewContainer: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
  previewImage: {
    flex: 1,
    resizeMode: 'cover',
  },
  analyzingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(15, 23, 42, 0.82)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  analyzingText: {
    color: '#FFFFFF',
    fontSize: 17,
    fontWeight: '700',
    marginTop: 16,
    textAlign: 'center',
  },
  analyzingSubtext: {
    color: '#CBD5E1',
    fontSize: 13,
    marginTop: 6,
    textAlign: 'center',
  },
  previewControls: {
    position: 'absolute',
    bottom: SPACING.md,
    left: 0,
    right: 0,
    paddingHorizontal: SPACING.md,
  },
  previewButtons: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    gap: SPACING.sm,
  },
  retakeButton: {
    flexGrow: 1,
    flexBasis: 110,
    minHeight: 48,
    backgroundColor: 'rgba(15, 23, 42, 0.75)',
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  retakeButtonText: {
    color: '#FFFFFF',
    fontWeight: '600',
    fontSize: 15,
    textAlign: 'center',
  },
  analyzeButton: {
    flexGrow: 1,
    flexBasis: 130,
    minHeight: 48,
    backgroundColor: COLORS.accent.berkeleyBlue,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  analyzeButtonText: {
    color: '#FFFFFF',
    fontWeight: '700',
    fontSize: 15,
    textAlign: 'center',
  },
});
