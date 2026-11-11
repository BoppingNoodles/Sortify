# Sortify — Frontend Subteam Starter Code & Technical Guidance (Weeks 6–12)

> **Subteam:** Frontend (React Native / Expo)  
> **Tech Stack:** React Native, Expo SDK 52+, Expo Camera, Expo Haptics, AsyncStorage, React Navigation, React Native Safe Area Context  
> **Purpose:** Concrete code scaffolds, component templates, navigation helpers, and step-by-step implementation guidance for the 2-week sprint cycle.

---

# Sprints Navigation
- [Sprint 1: Weeks 6–7 — End-to-End Mobile Integration & Result Modal](#sprint-1-weeks-67--end-to-end-mobile-integration--result-modal)
  - [Ticket: Live Camera-to-API Scan Integration (`ScanScreen.js`)](#ticket-live-camera-to-api-scan-integration)
  - [Ticket: Result Modal Component (`ResultModal.js` / `ResultScreen.js`)](#ticket-result-modal-component)
  - [Ticket: API Client & Retry Helper (`src/services/api.js`)](#ticket-api-client--retry-helper)
- [Sprint 2: Weeks 8–9 — History Feed, Stats Dashboard & Local Storage](#sprint-2-weeks-89--history-feed-stats-dashboard--local-storage)
  - [Ticket: History Feed Screen (`HistoryScreen.js`)](#ticket-history-feed-screen)
  - [Ticket: Stats & Streak Dashboard (`StatsScreen.js`)](#ticket-stats--streak-dashboard)
  - [Ticket: Local Storage Abstraction Helper (`src/services/storage.js`)](#ticket-local-storage-abstraction-helper)
- [Sprint 3: Weeks 10–11 — UX Polish, Haptics & Onboarding](#sprint-3-weeks-1011--ux-polish-haptics--onboarding)
  - [Ticket: Swipeable Onboarding Walkthrough (`OnboardingScreen.js`)](#ticket-swipeable-onboarding-walkthrough)
  - [Ticket: Tactile Haptics Integration (`expo-haptics`)](#ticket-tactile-haptics-integration)
  - [Ticket: Cross-Device Safe Area Audit & Performance Helper](#ticket-cross-device-safe-area-audit)
- [Week 12 — Final Milestone & Portfolio Showcase](#week-12--final-milestone--portfolio-showcase)
  - [Ticket: App Showcase Assets & Demo Walkthrough Script](#ticket-showcase-assets--demo-walkthrough)

---

# Sprint 1: Weeks 6–7 — End-to-End Mobile Integration & Result Modal

---

### Ticket: Live Camera-to-API Scan Integration
* **Target File:** `src/screens/ScanScreen.js`
* **Goal:** Replace simulated `setTimeout` mock with a real HTTP `multipart/form-data` upload to `POST /api/classify`.
* **Starter Scaffold:**

```javascript
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
        <TouchableOpacity style={styles.primaryButton} onPress={requestPermission}>
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
      setCapturedPhoto(photo);
    } catch (error) {
      console.error('Failed to capture photo:', error);
      Alert.alert('Camera Error', 'Could not capture photo. Please try again.');
    }
  };

  const handleAnalyze = async () => {
    if (!capturedPhoto || isAnalyzing) return;

    setIsAnalyzing(true);
    try {
      // Dispatch real upload request to the backend
      const result = await classifyImage(capturedPhoto.uri, selectedCity);

      // Navigate to ResultModal with live prediction data
      navigation.navigate('ResultModal', {
        itemName: result.item_name || 'Detected Item',
        category: result.category || 'landfill',
        confidence: result.confidence || 0.0,
        binColor: result.bin_color || 'Gray',
        bin: result.bin || 'Landfill Bin',
        disposalTip: result.disposal_tip || 'Place in appropriate container.',
        alternatives: result.alternatives || [],
        location: result.location || selectedCity,
        photoUri: capturedPhoto.uri,
      });

      // Clear current photo after navigating
      setCapturedPhoto(null);
    } catch (error) {
      console.error('Classification request failed:', error);
      Alert.alert(
        'Scan Failed',
        error.message || 'Unable to analyze image. Ensure your backend server is running.',
        [{ text: 'Retry', onPress: handleAnalyze }, { text: 'Cancel', style: 'cancel' }]
      );
    } finally {
      setIsAnalyzing(false);
    }
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
              <Text style={styles.analyzingText}>Analyzing waste item with AI...</Text>
              <Text style={styles.analyzingSubtext}>Checking {selectedCity.toUpperCase()} rules</Text>
            </View>
          ) : (
            <View style={styles.previewControls}>
              <TouchableOpacity style={styles.retakeButton} onPress={handleRetake}>
                <Text style={styles.controlButtonText}>Retake</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.analyzeButton} onPress={handleAnalyze}>
                <Text style={styles.analyzeButtonText}>Identify Bin</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      ) : (
        <CameraView style={styles.camera} ref={cameraRef}>
          <SafeAreaView style={styles.cameraOverlay}>
            <View style={styles.topBar}>
              <TouchableOpacity
                style={styles.cityPill}
                onPress={() => setSelectedCity(selectedCity === 'berkeley' ? 'san-francisco' : 'berkeley')}
              >
                <Text style={styles.cityPillText}>📍 {selectedCity.toUpperCase()}</Text>
              </TouchableOpacity>
            </View>
            <View style={styles.reticleContainer}>
              <View style={styles.reticleBox} />
              <Text style={styles.reticleHint}>Center item inside frame</Text>
            </View>
            <View style={styles.bottomControls}>
              <TouchableOpacity style={styles.shutterButton} onPress={handleCapture}>
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
  container: { flex: 1, backgroundColor: '#000' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 24 },
  camera: { flex: 1 },
  cameraOverlay: { flex: 1, justifyContent: 'space-between', padding: 16 },
  topBar: { flexDirection: 'row', justifyContent: 'center', marginTop: 10 },
  cityPill: {
    backgroundColor: 'rgba(0,0,0,0.6)',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.3)',
  },
  cityPillText: { color: '#FFF', fontWeight: '700', fontSize: 13 },
  reticleContainer: { alignItems: 'center' },
  reticleBox: {
    width: 250,
    height: 250,
    borderWidth: 2,
    borderColor: 'rgba(255,255,255,0.8)',
    borderRadius: 16,
    borderStyle: 'dashed',
  },
  reticleHint: { color: 'rgba(255,255,255,0.8)', marginTop: 12, fontSize: 14, fontWeight: '500' },
  bottomControls: { alignItems: 'center', marginBottom: 20 },
  shutterButton: {
    width: 76,
    height: 76,
    borderRadius: 38,
    borderWidth: 4,
    borderColor: '#FFF',
    justifyContent: 'center',
    alignItems: 'center',
  },
  shutterInner: { width: 60, height: 60, borderRadius: 30, backgroundColor: '#FFF' },
  previewContainer: { flex: 1, backgroundColor: '#000' },
  previewImage: { flex: 1, resizeMode: 'cover' },
  analyzingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  analyzingText: { color: '#FFF', fontSize: 18, fontWeight: '700', marginTop: 16 },
  analyzingSubtext: { color: 'rgba(255,255,255,0.7)', fontSize: 13, marginTop: 6 },
  previewControls: {
    position: 'absolute',
    bottom: 30,
    left: 20,
    right: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  retakeButton: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.7)',
    paddingVertical: 14,
    borderRadius: 12,
    marginRight: 10,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: 'rgba(255,255,255,0.3)',
  },
  analyzeButton: {
    flex: 2,
    backgroundColor: '#003262', // Berkeley Blue
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  controlButtonText: { color: '#FFF', fontWeight: '600', fontSize: 16 },
  analyzeButtonText: { color: '#FFF', fontWeight: '700', fontSize: 16 },
});
```

---

### Ticket: Result Modal Component
* **Target File:** `src/screens/ResultScreen.js`
* **Goal:** Render detected waste item with category badge, official bin colors, confidence meter, and municipal notes.
* **Starter Scaffold:**

```javascript
// src/screens/ResultScreen.js
import React from 'react';
import { StyleSheet, Text, View, Image, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';

const CATEGORY_COLORS = {
  compost: { bg: '#2E7D32', light: '#E8F5E9', label: 'COMPOST' },
  plastic: { bg: '#1565C0', light: '#E3F2FD', label: 'RECYCLING' },
  paper: { bg: '#6D4C41', light: '#EFEBE9', label: 'PAPER / CARDBOARD' },
  glass: { bg: '#00838F', light: '#E0F7FA', label: 'GLASS RECYCLING' },
  metal: { bg: '#0277BD', light: '#E1F5FE', label: 'METAL RECYCLING' },
  landfill: { bg: '#424242', light: '#EEEEEE', label: 'LANDFILL' },
};

export default function ResultScreen({ route, navigation }) {
  const {
    itemName = 'Sample Waste Item',
    category = 'landfill',
    confidence = 0.85,
    bin = 'Landfill Bin',
    disposalTip = 'Place in black landfill bin.',
    location = 'berkeley',
    photoUri = null,
  } = route.params || {};

  const theme = CATEGORY_COLORS[category.toLowerCase()] || CATEGORY_COLORS.landfill;
  const confidencePercent = Math.round(confidence * 100);

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        {/* Header / Dismiss */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Scan Result</Text>
          <TouchableOpacity style={styles.closeButton} onPress={() => navigation.goBack()}>
            <Text style={styles.closeButtonText}>Done</Text>
          </TouchableOpacity>
        </View>

        {/* Thumbnail Preview */}
        {photoUri && (
          <Image source={{ uri: photoUri }} style={styles.thumbnail} />
        )}

        {/* Primary Classification Banner */}
        <View style={[styles.badge, { backgroundColor: theme.bg }]}>
          <Text style={styles.badgeText}>{theme.label}</Text>
        </View>

        <Text style={styles.itemName}>{itemName}</Text>
        <Text style={styles.binName}>Target: {bin}</Text>

        {/* Confidence Meter */}
        <View style={styles.card}>
          <View style={styles.confidenceRow}>
            <Text style={styles.cardSectionLabel}>AI Confidence</Text>
            <Text style={styles.confidenceText}>{confidencePercent}%</Text>
          </View>
          <View style={styles.progressBarBackground}>
            <View style={[styles.progressBarFill, { width: `${confidencePercent}%`, backgroundColor: theme.bg }]} />
          </View>
        </View>

        {/* Municipal Guidance Card */}
        <View style={styles.card}>
          <Text style={styles.cardSectionLabel}>Municipal Sorting Guidance ({location.toUpperCase()})</Text>
          <Text style={styles.disposalTipText}>{disposalTip}</Text>
        </View>

        {/* Action Buttons */}
        <TouchableOpacity
          style={[styles.primaryAction, { backgroundColor: theme.bg }]}
          onPress={() => navigation.navigate('ScanScreen')}
        >
          <Text style={styles.primaryActionText}>Scan Another Item</Text>
        </TouchableOpacity>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  content: { padding: 20, alignItems: 'center' },
  header: { width: '100%', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 },
  headerTitle: { fontSize: 20, fontWeight: '700', color: '#1A1A1A' },
  closeButton: { padding: 8 },
  closeButtonText: { fontSize: 16, fontWeight: '600', color: '#003262' },
  thumbnail: { width: 140, height: 140, borderRadius: 16, marginBottom: 16 },
  badge: { paddingHorizontal: 16, paddingVertical: 6, borderRadius: 20, marginBottom: 8 },
  badgeText: { color: '#FFF', fontWeight: '800', fontSize: 13, letterSpacing: 1 },
  itemName: { fontSize: 24, fontWeight: '800', color: '#111', textAlign: 'center', marginBottom: 4 },
  binName: { fontSize: 16, fontWeight: '600', color: '#555', marginBottom: 16 },
  card: {
    width: '100%',
    backgroundColor: '#FFF',
    borderRadius: 16,
    padding: 18,
    marginBottom: 14,
    shadowColor: '#000',
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  cardSectionLabel: { fontSize: 12, fontWeight: '700', color: '#777', textTransform: 'uppercase', marginBottom: 8 },
  confidenceRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 },
  confidenceText: { fontSize: 16, fontWeight: '700', color: '#222' },
  progressBarBackground: { height: 8, backgroundColor: '#EEE', borderRadius: 4, overflow: 'hidden' },
  progressBarFill: { height: '100%', borderRadius: 4 },
  disposalTipText: { fontSize: 15, color: '#333', lineHeight: 22 },
  primaryAction: { width: '100%', paddingVertical: 16, borderRadius: 14, alignItems: 'center', marginTop: 10 },
  primaryActionText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
});
```

---

### Ticket: API Client & Retry Helper
* **Target File:** `src/services/api.js`
* **Goal:** Implement robust multipart image dispatch with retry backoff and environment resolution.
* **Starter Scaffold:**

```javascript
// src/services/api.js
import { Platform } from 'react-native';

// Adjust to your host machine's LAN IP when testing on physical devices via Expo Go
const DEV_API_URL = Platform.select({
  android: 'http://10.0.2.2:8000',
  ios: 'http://localhost:8000',
  default: 'http://127.0.0.1:8000',
});

export const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || DEV_API_URL;

/**
 * Dispatches an image file to POST /api/classify with retry capability.
 */
export async function classifyImage(imageUri, location = 'berkeley', maxRetries = 2) {
  const formData = new FormData();

  const filename = imageUri.split('/').pop() || 'photo.jpg';
  const match = /\.(\w+)$/.exec(filename);
  const type = match ? `image/${match[1]}` : 'image/jpeg';

  formData.append('file', {
    uri: Platform.OS === 'android' ? imageUri : imageUri.replace('file://', ''),
    name: filename,
    type,
  });

  let lastError = null;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/classify?location=${encodeURIComponent(location)}`, {
        method: 'POST',
        body: formData,
        headers: {
          Accept: 'application/json',
          'Content-Type': 'multipart/form-data',
        },
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => ({}));
        throw new Error(errorBody.detail || `Server returned HTTP ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      lastError = error;
      if (attempt < maxRetries) {
        // Wait 500ms before retrying
        await new Promise((resolve) => setTimeout(resolve, 500 * (attempt + 1)));
      }
    }
  }

  throw lastError || new Error('Failed to connect to classification service.');
}
```

---

# Sprint 2: Weeks 8–9 — History Feed, Stats Dashboard & Local Storage

---

### Ticket: History Feed Screen
* **Target File:** `src/screens/HistoryScreen.js`
* **Goal:** Render responsive scan feed with thumbnails, category badges, pull-to-refresh, and empty state.
* **Starter Scaffold:**

```javascript
// src/screens/HistoryScreen.js
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, FlatList, Image, TouchableOpacity, RefreshControl, SafeAreaView } from 'react-native';
import { loadSavedScans } from '../services/storage';

export default function HistoryScreen({ navigation }) {
  const [scans, setScans] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const fetchHistory = async () => {
    setRefreshing(true);
    try {
      const data = await loadSavedScans();
      setScans(data);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.scanCard}>
      {item.photoUri ? (
        <Image source={{ uri: item.photoUri }} style={styles.cardImage} />
      ) : (
        <View style={styles.cardPlaceholder}><Text style={styles.placeholderEmoji}>♻️</Text></View>
      )}
      <View style={styles.cardContent}>
        <Text style={styles.cardTitle}>{item.itemName || 'Waste Item'}</Text>
        <Text style={styles.cardSubtitle}>{item.bin || 'Sorted Item'}</Text>
        <Text style={styles.cardDate}>{item.date || 'Today'}</Text>
      </View>
      <View style={styles.pointsBadge}>
        <Text style={styles.pointsText}>+10 pts</Text>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Scan History</Text>
      </View>
      <FlatList
        data={scans}
        keyExtractor={(item, index) => item.id || `scan_${index}`}
        renderItem={renderItem}
        contentContainerStyle={scans.length === 0 ? styles.emptyContainer : styles.listContent}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={fetchHistory} />}
        ListEmptyComponent={
          <View style={styles.emptyView}>
            <Text style={styles.emptyEmoji}>📸</Text>
            <Text style={styles.emptyTitle}>No scans yet</Text>
            <Text style={styles.emptyBody}>Snap a photo of waste on campus to start your sorting streak!</Text>
            <TouchableOpacity style={styles.scanNowButton} onPress={() => navigation.navigate('ScanScreen')}>
              <Text style={styles.scanNowButtonText}>Scan First Item</Text>
            </TouchableOpacity>
          </View>
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  header: { padding: 20, backgroundColor: '#FFF', borderBottomWidth: 1, borderBottomColor: '#EEE' },
  headerTitle: { fontSize: 22, fontWeight: '800', color: '#111' },
  listContent: { padding: 16 },
  emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 24 },
  scanCard: {
    flexDirection: 'row',
    backgroundColor: '#FFF',
    borderRadius: 14,
    padding: 12,
    marginBottom: 10,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
  },
  cardImage: { width: 60, height: 60, borderRadius: 10, marginRight: 14 },
  cardPlaceholder: { width: 60, height: 60, borderRadius: 10, backgroundColor: '#E9ECEF', justifyContent: 'center', alignItems: 'center', marginRight: 14 },
  placeholderEmoji: { fontSize: 24 },
  cardContent: { flex: 1 },
  cardTitle: { fontSize: 16, fontWeight: '700', color: '#222' },
  cardSubtitle: { fontSize: 13, color: '#666', marginTop: 2 },
  cardDate: { fontSize: 12, color: '#999', marginTop: 4 },
  pointsBadge: { backgroundColor: '#E8F5E9', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  pointsText: { color: '#2E7D32', fontSize: 12, fontWeight: '700' },
  emptyView: { alignItems: 'center', paddingHorizontal: 30 },
  emptyEmoji: { fontSize: 50, marginBottom: 12 },
  emptyTitle: { fontSize: 18, fontWeight: '700', color: '#222', marginBottom: 6 },
  emptyBody: { fontSize: 14, color: '#666', textAlign: 'center', lineHeight: 20, marginBottom: 20 },
  scanNowButton: { backgroundColor: '#003262', paddingVertical: 12, paddingHorizontal: 24, borderRadius: 20 },
  scanNowButtonText: { color: '#FFF', fontWeight: '700', fontSize: 15 },
});
```

---

### Ticket: Stats & Streak Dashboard
* **Target File:** `src/screens/StatsScreen.js`
* **Goal:** Motivate student habit formation with streak count, total scans, and category breakdown.
* **Starter Scaffold:**

```javascript
// src/screens/StatsScreen.js
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, SafeAreaView, ActivityIndicator } from 'react-native';

export default function StatsScreen() {
  const [stats, setStats] = useState({
    currentStreak: 4,
    totalScans: 28,
    ecoPoints: 280,
    breakdown: { compost: 12, plastic: 8, paper: 5, glass: 2, landfill: 1 },
  });

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.screenTitle}>Impact Dashboard</Text>

        {/* Streak Flame Card */}
        <View style={styles.streakCard}>
          <Text style={styles.streakEmoji}>🔥</Text>
          <Text style={styles.streakCount}>{stats.currentStreak} Day Streak!</Text>
          <Text style={styles.streakSubtext}>Scan daily to keep the campus green</Text>
        </View>

        {/* Impact Counters Grid */}
        <View style={styles.statsGrid}>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{stats.totalScans}</Text>
            <Text style={styles.statLabel}>Total Scans</Text>
          </View>
          <View style={styles.statBox}>
            <Text style={styles.statNumber}>{stats.ecoPoints}</Text>
            <Text style={styles.statLabel}>Eco Points</Text>
          </View>
        </View>

        {/* Sorting Category Breakdown */}
        <View style={styles.breakdownCard}>
          <Text style={styles.cardHeader}>Category Distribution</Text>
          {Object.entries(stats.breakdown).map(([cat, count]) => (
            <View key={cat} style={styles.categoryRow}>
              <Text style={styles.categoryName}>{cat.toUpperCase()}</Text>
              <Text style={styles.categoryCount}>{count} items</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  content: { padding: 20 },
  screenTitle: { fontSize: 24, fontWeight: '800', color: '#111', marginBottom: 16 },
  streakCard: {
    backgroundColor: '#FFF3E0',
    borderColor: '#FFE0B2',
    borderWidth: 1,
    borderRadius: 18,
    padding: 24,
    alignItems: 'center',
    marginBottom: 16,
  },
  streakEmoji: { fontSize: 44, marginBottom: 8 },
  streakCount: { fontSize: 22, fontWeight: '800', color: '#E65100' },
  streakSubtext: { fontSize: 13, color: '#BF360C', marginTop: 4 },
  statsGrid: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 16 },
  statBox: {
    flex: 1,
    backgroundColor: '#FFF',
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 4,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
  },
  statNumber: { fontSize: 26, fontWeight: '800', color: '#003262' },
  statLabel: { fontSize: 13, color: '#666', marginTop: 4, fontWeight: '600' },
  breakdownCard: {
    backgroundColor: '#FFF',
    borderRadius: 16,
    padding: 20,
    shadowColor: '#000',
    shadowOpacity: 0.04,
    shadowRadius: 6,
    elevation: 2,
  },
  cardHeader: { fontSize: 16, fontWeight: '700', color: '#111', marginBottom: 14 },
  categoryRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: '#F0F0F0' },
  categoryName: { fontSize: 14, fontWeight: '600', color: '#444' },
  categoryCount: { fontSize: 14, fontWeight: '700', color: '#003262' },
});
```

---

### Ticket: Local Storage Abstraction Helper
* **Target File:** `src/services/storage.js`
* **Goal:** Encapsulate `AsyncStorage` methods for saving, retrieving, and clearing scan history and stats.
* **Starter Scaffold:**

```javascript
// src/services/storage.js
import AsyncStorage from '@react-native-async-storage/async-storage';

const SCANS_STORAGE_KEY = '@sortify_saved_scans';
const STREAK_STORAGE_KEY = '@sortify_user_streak';

export async function saveScanRecord(scanData) {
  try {
    const existing = await loadSavedScans();
    const newRecord = {
      id: `scan_${Date.now()}`,
      timestamp: new Date().toISOString(),
      ...scanData,
    };
    const updated = [newRecord, ...existing];
    await AsyncStorage.setItem(SCANS_STORAGE_KEY, JSON.stringify(updated.slice(0, 100))); // keep latest 100
    return newRecord;
  } catch (error) {
    console.error('Error saving scan to local storage:', error);
    return null;
  }
}

export async function loadSavedScans() {
  try {
    const raw = await AsyncStorage.getItem(SCANS_STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (error) {
    console.error('Error loading scans from local storage:', error);
    return [];
  }
}
```

---

# Sprint 3: Weeks 10–11 — UX Polish, Haptics & Onboarding

---

### Ticket: Swipeable Onboarding Walkthrough
* **Target File:** `src/screens/OnboardingScreen.js`
* **Goal:** Present 3 swipeable onboarding slides explaining how Sortify works before entering camera.
* **Starter Scaffold:**

```javascript
// src/screens/OnboardingScreen.js
import React, { useState } from 'react';
import { StyleSheet, Text, View, SafeAreaView, TouchableOpacity, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

const SLIDES = [
  {
    emoji: '📸',
    title: 'Snap Your Waste',
    desc: 'Point your camera at any bottle, container, or wrapper to scan it instantly.',
  },
  {
    emoji: '♻️',
    title: 'Municipal Guidance',
    desc: 'Get exact bin recommendations tailored to UC Berkeley and Bay Area rules.',
  },
  {
    emoji: '🔥',
    title: 'Build Sorting Streaks',
    desc: 'Earn eco-points, build sorting habits, and keep campus landfills empty.',
  },
];

export default function OnboardingScreen({ onFinish }) {
  const [currentSlide, setCurrentSlide] = useState(0);

  const handleNext = () => {
    if (currentSlide < SLIDES.length - 1) {
      setCurrentSlide(currentSlide + 1);
    } else {
      if (onFinish) onFinish();
    }
  };

  const slide = SLIDES[currentSlide];

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.slideContent}>
        <Text style={styles.emoji}>{slide.emoji}</Text>
        <Text style={styles.title}>{slide.title}</Text>
        <Text style={styles.desc}>{slide.desc}</Text>
      </View>
      <View style={styles.footer}>
        <TouchableOpacity style={styles.button} onPress={handleNext}>
          <Text style={styles.buttonText}>{currentSlide === SLIDES.length - 1 ? 'Get Started' : 'Next'}</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#FFF', justifyContent: 'space-between', padding: 24 },
  slideContent: { flex: 1, justifyContent: 'center', alignItems: 'center', paddingHorizontal: 20 },
  emoji: { fontSize: 72, marginBottom: 24 },
  title: { fontSize: 24, fontWeight: '800', color: '#111', textAlign: 'center', marginBottom: 12 },
  desc: { fontSize: 16, color: '#666', textAlign: 'center', lineHeight: 24 },
  footer: { paddingBottom: 20 },
  button: { backgroundColor: '#003262', paddingVertical: 16, borderRadius: 14, alignItems: 'center' },
  buttonText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
});
```

---

### Ticket: Tactile Haptics Integration
* **Target Files:** `ScanScreen.js` and `ResultScreen.js`
* **Goal:** Trigger responsive haptic vibrations on shutter tap and result reveal.
* **Implementation Pattern:**

```javascript
import * as Haptics from 'expo-haptics';

// 1. Shutter press trigger:
const onShutterPress = async () => {
  await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
  // ... capture logic ...
};

// 2. Result modal load trigger:
const onResultReceived = async () => {
  await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
};
```

---

### Ticket: Cross-Device Safe Area Audit
* **Target File:** `src/styles/theme.js` & `AppNavigator.js`
* **Goal:** Verify that bottom gesture bar and top notch do not overlap camera buttons or modal sheets across physical iOS and Android phones.

---

# Week 12 — Final Milestone & Portfolio Showcase

---

### Ticket: Showcase Assets & Demo Walkthrough
* **Goal:** Capture high-resolution iPhone frames running Sortify and record the 2-minute demo walkthrough for the presentation slide deck.
* **Deliverable:** 4 device screenshot cards placed in `docs/portfolio_assets/` and high-res video `.mp4`.
