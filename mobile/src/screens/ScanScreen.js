// src/screens/ScanScreen.js
import React, { useState, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image, SafeAreaView, ActivityIndicator } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import { COLORS, SPACING } from '../styles/theme';

export default function ScanScreen({ navigation }) {
  const [permission, requestPermission] = useCameraPermissions();
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
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
        <Text style={styles.permissionBody}>Sortify requires camera access to scan and classify waste items in real time.</Text>
        <TouchableOpacity style={styles.primaryButton} onPress={requestPermission}>
          <Text style={styles.buttonText}>Grant Permission</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  const handleCapture = async () => {
    if (!cameraRef.current || isAnalyzing) return;
    try {
      const photo = await cameraRef.current.takePictureAsync({ quality: 0.7 });
      setCapturedPhoto(photo);
    } catch (error) {
      console.error('Failed to capture photo:', error);
    }
  };

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    // TODO: In Week 4, call classifyImage(capturedPhoto.uri)
    setTimeout(() => {
      setIsAnalyzing(false);
      const photoUri = capturedPhoto.uri;
      setCapturedPhoto(null);
      navigation.navigate('ResultModal', {
        itemName: 'Paper Coffee Cup',
        category: 'compost',
        confidence: 0.94,
        tip: 'Accepted in Berkeley green compost bins. Please empty liquids first.',
        photoUri,
      });
    }, 1000);
  };

  const handleRetake = () => {
    setCapturedPhoto(null);
  };

  return (
    <View style={styles.container}>
      {capturedPhoto ? (
        <View style={styles.previewContainer}>
          <Image source={{ uri: capturedPhoto.uri }} style={styles.previewImage} />
          {isAnalyzing ? (
            <View style={styles.analyzingOverlay}>
              <ActivityIndicator size="large" color="#FFFFFF" />
              <Text style={styles.analyzingText}>Analyzing item with Sortify AI...</Text>
            </View>
          ) : (
            <View style={styles.actionRow}>
              <TouchableOpacity style={styles.retakeButton} onPress={handleRetake}>
                <Text style={styles.retakeText}>Retake</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.analyzeButton} onPress={handleAnalyze}>
                <Text style={styles.buttonText}>Analyze Item</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      ) : (
        <CameraView style={styles.camera} ref={cameraRef}>
          {/* Target Reticle Overlay */}
          <View style={styles.reticle} />
          <Text style={styles.reticleHint}>Center item inside frame</Text>

          {/* Shutter Bar */}
          <View style={styles.bottomBar}>
            <TouchableOpacity style={styles.shutterButton} onPress={handleCapture} activeOpacity={0.7} />
          </View>
        </CameraView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: SPACING.lg, backgroundColor: COLORS.background.primary },
  statusText: { marginTop: 12, color: COLORS.text.secondary },
  permissionTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 8, color: COLORS.text.primary },
  permissionBody: { fontSize: 14, color: COLORS.text.secondary, textAlign: 'center', marginBottom: 20 },
  primaryButton: { backgroundColor: COLORS.bins.compost, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 10 },
  buttonText: { color: '#FFF', fontWeight: 'bold', fontSize: 15 },
  camera: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  reticle: { width: 260, height: 260, borderWidth: 2, borderColor: 'rgba(255,255,255,0.7)', borderRadius: 20 },
  reticleHint: { color: 'rgba(255,255,255,0.8)', marginTop: 16, fontSize: 13, fontWeight: '600' },
  bottomBar: { position: 'absolute', bottom: 44, width: '100%', alignItems: 'center' },
  shutterButton: { width: 74, height: 74, borderRadius: 37, borderWidth: 4, borderColor: '#FFF', backgroundColor: 'rgba(255,255,255,0.3)' },
  previewContainer: { flex: 1 },
  previewImage: { flex: 1 },
  actionRow: { position: 'absolute', bottom: 44, flexDirection: 'row', width: '100%', justifyContent: 'space-evenly', paddingHorizontal: 20 },
  retakeButton: { backgroundColor: 'rgba(0,0,0,0.6)', paddingVertical: 14, paddingHorizontal: 28, borderRadius: 12, borderWidth: 1, borderColor: '#FFF' },
  retakeText: { color: '#FFF', fontWeight: '600', fontSize: 15 },
  analyzeButton: { backgroundColor: COLORS.bins.compost, paddingVertical: 14, paddingHorizontal: 28, borderRadius: 12 },
  analyzingOverlay: { ...StyleSheet.absoluteFillObject, backgroundColor: 'rgba(0,0,0,0.7)', justifyContent: 'center', alignItems: 'center' },
  analyzingText: { color: '#FFF', marginTop: 16, fontSize: 16, fontWeight: '600' },
});
