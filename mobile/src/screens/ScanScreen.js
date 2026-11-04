// src/screens/ScanScreen.js
import React, { useState, useRef } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Image,
  SafeAreaView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { COLORS, SPACING } from '../styles/theme';
import { classifyImage } from '../services/api';

const SUPPORTED_CITIES = ['berkeley', 'san-francisco', 'oakland', 'san-jose', 'sunnyvale'];

export default function ScanScreen({ navigation }) {
  const [permission, requestPermission] = useCameraPermissions();
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedCity, setSelectedCity] = useState('berkeley');
  const cameraRef = useRef(null);

  if (!permission) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={COLORS.accent.berkeleyBlue} />
        <Text style={styles.statusText}>Requesting camera permission...</Text>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <SafeAreaView style={styles.centered}>
        <Text style={styles.permissionTitle}>Camera Access Required</Text>
        <Text style={styles.permissionBody}>
          Sortify requires camera access to scan and classify waste items in real time.
        </Text>
        <TouchableOpacity style={styles.primaryButton} onPress={requestPermission} activeOpacity={0.8}>
          <Text style={styles.buttonText}>Grant Permission</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  const handleCapture = async () => {
    if (!cameraRef.current || isAnalyzing) return;
    try {
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.8,
        skipProcessing: false,
      });
      if (photo?.uri) {
        setCapturedPhoto(photo);
      }
    } catch (error) {
      console.error('Failed to capture photo:', error);
      Alert.alert('Camera Error', 'Could not capture photo. Please try again.');
    }
  };

  const handleAnalyze = async () => {
    if (!capturedPhoto?.uri || isAnalyzing) return;

    setIsAnalyzing(true);
    try {
      const result = await classifyImage(capturedPhoto.uri, selectedCity);

      if (!result || typeof result !== 'object') {
        throw new Error('Classification server returned an invalid response.');
      }

      const photoUri = capturedPhoto.uri;

      // Clear captured photo so camera preview resets cleanly when returning from result modal
      setCapturedPhoto(null);

      // Navigate to ResultModal with live prediction fields
      navigation.navigate('ResultModal', {
        itemName: result.item_name || result.itemName || 'Detected Waste Item',
        category: (result.category || 'landfill').toLowerCase(),
        confidence: typeof result.confidence === 'number' ? result.confidence : 0.0,
        bin: result.bin || result.bin_color || 'Landfill Bin',
        binColor: result.bin_color || null,
        disposalTip: result.disposal_tip || result.tip || 'Place in designated waste receptacle.',
        tip: result.disposal_tip || result.tip || 'Place in designated waste receptacle.',
        location: result.location || selectedCity,
        alternatives: result.alternatives || [],
        photoUri,
      });
    } catch (error) {
      console.error('Classification request failed:', error);
      Alert.alert(
        'Scan Failed',
        error.message || 'Unable to analyze image. Please ensure your backend server is running.',
        [
          { text: 'Retake', style: 'cancel', onPress: handleRetake },
          { text: 'Try Again', onPress: handleAnalyze },
        ]
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleRetake = () => {
    if (isAnalyzing) return;
    setCapturedPhoto(null);
  };

  const handleCycleCity = () => {
    const currentIndex = SUPPORTED_CITIES.indexOf(selectedCity);
    const nextCity = SUPPORTED_CITIES[(currentIndex + 1) % SUPPORTED_CITIES.length];
    setSelectedCity(nextCity);
  };

  const formattedCity = selectedCity.replace('-', ' ').toUpperCase();

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
            <View style={styles.previewControls}>
              <TouchableOpacity
                style={styles.retakeButton}
                onPress={handleRetake}
                activeOpacity={0.8}
              >
                <Text style={styles.retakeButtonText}>Retake</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.analyzeButton}
                onPress={handleAnalyze}
                activeOpacity={0.8}
              >
                <Text style={styles.analyzeButtonText}>Identify Bin</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      ) : (
        <CameraView style={styles.camera} ref={cameraRef}>
          <SafeAreaView style={styles.cameraOverlay}>
            {/* Top Bar with Municipality Selector */}
            <View style={styles.topBar}>
              <TouchableOpacity
                style={styles.cityPill}
                onPress={handleCycleCity}
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
                activeOpacity={0.7}
              >
                <View style={styles.shutterInner} />
              </TouchableOpacity>
            </View>
          </SafeAreaView>
        </CameraView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: SPACING.lg,
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
    flex: 1,
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
  },
  topBar: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 8,
  },
  cityPill: {
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
  },
  reticleContainer: {
    alignItems: 'center',
  },
  reticleBox: {
    width: 250,
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
  },
  bottomControls: {
    alignItems: 'center',
    marginBottom: 24,
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
    bottom: 36,
    left: 20,
    right: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
  },
  retakeButton: {
    flex: 1,
    backgroundColor: 'rgba(15, 23, 42, 0.75)',
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.3)',
  },
  retakeButtonText: {
    color: '#FFFFFF',
    fontWeight: '600',
    fontSize: 15,
  },
  analyzeButton: {
    flex: 1.5,
    backgroundColor: COLORS.accent.berkeleyBlue,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  analyzeButtonText: {
    color: '#FFFFFF',
    fontWeight: '700',
    fontSize: 15,
  },
});
