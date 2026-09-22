# Sortify — Frontend Subteam Starter Code & Technical Guidance (Weeks 1–12)

> **Subteam:** Frontend (Mobile / UI/UX)  
> **Members:** Mong, Caden  
> **Tech Stack:** React Native, Expo, React Navigation, Expo Camera, Expo SecureStore, Expo Haptics  
> **Purpose:** Structural scaffolds, function signatures, and step-by-step implementation guidance for each weekly deliverable.

---

# Week 1 — Setup, Onboarding & Learning Exercises

---

### Mong (Week 1)
* **Task:** Figma Wireframing & User Journey Mapping (Primary) + Optional React Native Sandbox
* **Target File / Output:** Shared Figma Canvas (`Sortify Mobile`) / `sandbox/App.js`
* **Starter Guidance & Structure:**

```javascript
// sandbox/App.js (Optional React Native Sandbox)
import React, { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, SafeAreaView } from 'react-native';

export default function App() {
  const [activeScreen, setActiveScreen] = useState('Home');

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>Sortify UI Sandbox</Text>
      {/* TODO: Add mock navigation between Home, Scan, and Result view placeholders */}
      <View style={styles.placeholderBox}>
        <Text>Current Screen: {activeScreen}</Text>
      </View>
      <TouchableOpacity 
        style={styles.button}
        onPress={() => setActiveScreen(activeScreen === 'Home' ? 'Scan' : 'Home')}
      >
        <Text style={styles.buttonText}>Toggle Test Screen</Text>
      </TouchableOpacity>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', backgroundColor: '#F8FAFC' },
  title: { fontSize: 22, fontWeight: 'bold', marginBottom: 16 },
  placeholderBox: { width: '80%', height: 160, borderWidth: 1, borderColor: '#CBD5E1', borderRadius: 12, justifyContent: 'center', alignItems: 'center', marginBottom: 20 },
  button: { backgroundColor: '#16A34A', paddingVertical: 12, paddingHorizontal: 24, borderRadius: 8 },
  buttonText: { color: '#FFFFFF', fontWeight: '600' }
});
```

* **Figma Canvas Architecture Checklist:**
  1. `01_Design_Tokens`: Waste bin colors (`Blue #2563EB`, `Green #16A34A`, `Brown #D97706`, `Teal #0D9488`, `Gray #4B5563`).
  2. `02_User_Flow`: Onboarding → Dashboard → Camera Reticle → Result Modal → History.
  3. `03_Wireframes`: 375×812pt frames with 16pt margin gutters and 44×44pt minimum touch targets.

---

### Caden (Week 1)
* **Task:** Mobile Workspace Setup & Camera Permission Sandbox
* **Target File / Output:** `sortify-app/App.js`
* **Starter Guidance & Structure:**

```javascript
// sortify-app/App.js (Expo Camera Sandbox)
import React, { useState, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image, SafeAreaView } from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';

export default function App() {
  const [permission, requestPermission] = useCameraPermissions();
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const cameraRef = useRef(null);

  // TODO: Handle loading / permission pending state
  if (!permission) {
    return <View style={styles.centered}><Text>Requesting camera permission...</Text></View>;
  }

  // TODO: Handle permission denied state with request button
  if (!permission.granted) {
    return (
      <SafeAreaView style={styles.centered}>
        <Text style={styles.permissionText}>Camera permission is required to scan waste items.</Text>
        <TouchableOpacity style={styles.button} onPress={requestPermission}>
          <Text style={styles.buttonText}>Grant Permission</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  const handleCapture = async () => {
    // TODO: Use cameraRef.current.takePictureAsync() with quality: 0.7
    // TODO: Store photo URI in capturedPhoto state
  };

  return (
    <View style={styles.container}>
      {capturedPhoto ? (
        <View style={styles.previewContainer}>
          <Image source={{ uri: capturedPhoto.uri }} style={styles.previewImage} />
          {/* TODO: Add 'Retake' and 'Use Photo' buttons */}
        </View>
      ) : (
        <CameraView style={styles.camera} ref={cameraRef}>
          <View style={styles.shutterContainer}>
            <TouchableOpacity style={styles.shutterButton} onPress={handleCapture} />
          </View>
        </CameraView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  camera: { flex: 1 },
  permissionText: { textAlign: 'center', marginBottom: 16, fontSize: 16 },
  button: { backgroundColor: '#16A34A', padding: 12, borderRadius: 8 },
  buttonText: { color: '#FFF', fontWeight: 'bold' },
  shutterContainer: { position: 'absolute', bottom: 40, width: '100%', alignItems: 'center' },
  shutterButton: { width: 72, height: 72, borderRadius: 36, borderWidth: 4, borderColor: '#FFF', backgroundColor: 'rgba(255,255,255,0.3)' },
  previewContainer: { flex: 1 },
  previewImage: { flex: 1 }
});
```

---

# Week 2 — Design, Architecture & Data Preparation

---

### Mong (Week 2)
* **Task:** Design Token System & High-Fidelity Figma Components
* **Target File / Output:** `src/styles/theme.js`
* **Starter Guidance & Structure:**

```javascript
// src/styles/theme.js
export const COLORS = {
  // Waste Bin Color System
  bins: {
    plastic: '#2563EB',    // Blue
    compost: '#16A34A',    // Green
    paper: '#D97706',      // Brown / Amber
    glass: '#0D9488',      // Teal
    landfill: '#4B5563',   // Charcoal Gray
  },
  background: {
    primary: '#F8FAFC',
    card: '#FFFFFF',
    surface: '#F1F5F9',
  },
  text: {
    primary: '#0F172A',
    secondary: '#64748B',
    muted: '#94A3B8',
    inverse: '#FFFFFF',
  },
  accent: {
    berkeleyBlue: '#003262',
    californiaGold: '#FDB515',
  }
};

export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const TYPOGRAPHY = {
  header: { fontSize: 24, fontWeight: '700' },
  subtitle: { fontSize: 18, fontWeight: '600' },
  body: { fontSize: 14, fontWeight: '400' },
  caption: { fontSize: 12, fontWeight: '400' },
};
```

---

### Caden (Week 2)
* **Task:** React Navigation Scaffolding & Directory Setup
* **Target File / Output:** `src/navigation/AppNavigator.js`
* **Starter Guidance & Structure:**

```javascript
// src/navigation/AppNavigator.js
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

// Placeholder screen imports
import HomeScreen from '../screens/HomeScreen';
import ScanScreen from '../screens/ScanScreen';
import HistoryScreen from '../screens/HistoryScreen';
import ProfileScreen from '../screens/ProfileScreen';
import ResultScreen from '../screens/ResultScreen';

const Tab = createBottomTabNavigator();
const Stack = createNativeStackNavigator();

function MainTabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      {/* TODO: Configure tab icons (Ionicons) and active tint colors */}
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Scan" component={ScanScreen} />
      <Tab.Screen name="History" component={HistoryScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        {/* Main tab navigator */}
        <Stack.Screen name="MainTabs" component={MainTabs} options={{ headerShown: false }} />
        {/* Modal transitions */}
        <Stack.Screen 
          name="ResultModal" 
          component={ResultScreen} 
          options={{ presentation: 'modal', title: 'Item Analysis' }} 
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

---

# Week 3 — Foundation Building & Scaffolding

---

### Mong (Week 3)
* **Task:** Result Screen Component with Mock Data
* **Target File / Output:** `src/screens/ResultScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/ResultScreen.js
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function ResultScreen({ route, navigation }) {
  // Extract params or fallback to mock prediction
  const { 
    itemName = 'Paper Coffee Cup', 
    category = 'compost', 
    confidence = 0.92,
    tip = 'Compostable in Berkeley if certified BPI or lining is plant-based.'
  } = route?.params || {};

  const binColor = COLORS.bins[category.toLowerCase()] || COLORS.bins.landfill;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {/* Category Header Badge */}
      <View style={[styles.badge, { backgroundColor: binColor }]}>
        <Text style={styles.badgeText}>{category.toUpperCase()}</Text>
      </View>

      <Text style={styles.itemName}>{itemName}</Text>

      {/* Confidence Bar */}
      <View style={styles.confidenceContainer}>
        <Text style={styles.confidenceLabel}>Confidence: {Math.round(confidence * 100)}%</Text>
        <View style={styles.progressBarBackground}>
          <View style={[styles.progressBarFill, { width: `${Math.round(confidence * 100)}%`, backgroundColor: binColor }]} />
        </View>
      </View>

      {/* Disposal Recommendation Card */}
      <View style={styles.tipCard}>
        <Text style={styles.tipTitle}>Disposal Guideline</Text>
        <Text style={styles.tipBody}>{tip}</Text>
      </View>

      {/* Action Buttons */}
      <TouchableOpacity 
        style={[styles.primaryButton, { backgroundColor: binColor }]}
        onPress={() => navigation.goBack()}
      >
        <Text style={styles.buttonText}>Scan Another Item</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: SPACING.lg, alignItems: 'center' },
  badge: { paddingHorizontal: 20, paddingVertical: 8, borderRadius: 20, marginBottom: 12 },
  badgeText: { color: '#FFF', fontWeight: 'bold', fontSize: 16 },
  itemName: { ...TYPOGRAPHY.header, textAlign: 'center', marginBottom: 16 },
  confidenceContainer: { width: '100%', marginBottom: 24 },
  confidenceLabel: { ...TYPOGRAPHY.caption, marginBottom: 6 },
  progressBarBackground: { height: 10, backgroundColor: '#E2E8F0', borderRadius: 5, overflow: 'hidden' },
  progressBarFill: { height: '100%' },
  tipCard: { backgroundColor: '#F8FAFC', padding: 16, borderRadius: 12, width: '100%', marginBottom: 24, borderWidth: 1, borderColor: '#E2E8F0' },
  tipTitle: { ...TYPOGRAPHY.subtitle, fontSize: 16, marginBottom: 8 },
  tipBody: { ...TYPOGRAPHY.body, color: '#475569' },
  primaryButton: { width: '100%', padding: 16, borderRadius: 12, alignItems: 'center' },
  buttonText: { color: '#FFF', fontWeight: '700' }
});
```

---

### Caden (Week 3)
* **Task:** Camera Viewfinder with Overlay & Scaffolding `services/api.js`
* **Target File / Output:** `src/screens/ScanScreen.js` & `src/services/api.js`
* **Starter Guidance & Structure:**

```javascript
// src/services/api.js
const API_BASE_URL = 'http://192.168.1.50:8000'; // TODO: Update to local backend IP or tunnel

export async function classifyImage(imageUri, location = 'berkeley') {
  const formData = new FormData();
  
  // Create file entry from local URI
  const filename = imageUri.split('/').pop();
  const match = /\.(\w+)$/.exec(filename);
  const type = match ? `image/${match[1]}` : 'image/jpeg';

  formData.append('file', {
    uri: imageUri,
    name: filename,
    type,
  });

  // TODO: Add location query or form parameter
  // TODO: Add AbortController for 10s request timeout
  const response = await fetch(`${API_BASE_URL}/api/classify?location=${encodeURIComponent(location)}`, {
    method: 'POST',
    body: formData,
    headers: {
      'Accept': 'application/json',
      // Note: Do NOT set Content-Type header manually when using FormData in React Native
    },
  });

  if (!response.ok) {
    throw new Error(`Server returned ${response.status}`);
  }

  return await response.json();
}
```

---

# Week 4 — Core MVP Build (Part 1: Live Scanning & Dashboard)

---

### Mong (Week 4)
* **Task:** Build Home Screen UI with Streak and Action Cards
* **Target File / Output:** `src/screens/HomeScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/HomeScreen.js
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { COLORS, SPACING, TYPOGRAPHY } from '../styles/theme';

export default function HomeScreen({ navigation }) {
  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Bear Mascot & Campus Greeting */}
      <View style={styles.header}>
        <Text style={styles.welcomeText}>Welcome back, Cal Bear! 🐻</Text>
        <Text style={styles.subText}>UC Berkeley Sustainable Campus</Text>
      </View>

      {/* Daily Streak Card */}
      <View style={styles.streakCard}>
        <Text style={styles.streakEmoji}>🔥</Text>
        <View>
          <Text style={styles.streakNumber}>3 Day Streak</Text>
          <Text style={styles.streakSubtext}>Scan an item today to keep it active!</Text>
        </View>
      </View>

      {/* Main Scan Button CTA */}
      <TouchableOpacity 
        style={styles.scanCta}
        onPress={() => navigation.navigate('Scan')}
      >
        <Text style={styles.scanCtaText}>📸 Scan Waste Item</Text>
      </TouchableOpacity>

      {/* Did You Know? Tip Card */}
      <View style={styles.infoCard}>
        <Text style={styles.infoTitle}>Did you know?</Text>
        <Text style={styles.infoBody}>
          Pizza boxes with grease belong in the green Compost bin at Berkeley, not paper recycling!
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC' },
  content: { padding: SPACING.lg },
  header: { marginBottom: SPACING.lg },
  welcomeText: { ...TYPOGRAPHY.header, color: COLORS.accent.berkeleyBlue },
  subText: { ...TYPOGRAPHY.caption, color: COLORS.text.secondary },
  streakCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFFBEB', padding: 16, borderRadius: 12, borderWidth: 1, borderColor: '#FDE68A', marginBottom: SPACING.lg },
  streakEmoji: { fontSize: 32, marginRight: 12 },
  streakNumber: { fontWeight: '700', fontSize: 16, color: '#B45309' },
  streakSubtext: { fontSize: 12, color: '#92400E' },
  scanCta: { backgroundColor: COLORS.bins.compost, padding: 20, borderRadius: 16, alignItems: 'center', marginBottom: SPACING.lg, elevation: 4 },
  scanCtaText: { color: '#FFF', fontSize: 18, fontWeight: '700' },
  infoCard: { backgroundColor: '#FFFFFF', padding: 16, borderRadius: 12, borderWidth: 1, borderColor: '#E2E8F0' },
  infoTitle: { fontWeight: '600', marginBottom: 4 },
  infoBody: { color: '#64748B', lineHeight: 20 }
});
```

---

### Caden (Week 4)
* **Task:** Integrate Camera Shutter with Live Classification API
* **Target File / Output:** `src/screens/ScanScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/ScanScreen.js (Integration snippet)
import React, { useState, useRef } from 'react';
import { View, Text, TouchableOpacity, ActivityIndicator, Alert, StyleSheet } from 'react-native';
import { CameraView } from 'expo-camera';
import { classifyImage } from '../services/api';

export default function ScanScreen({ navigation }) {
  const cameraRef = useRef(null);
  const [isClassifying, setIsClassifying] = useState(false);

  const handleCaptureAndAnalyze = async () => {
    if (!cameraRef.current || isClassifying) return;
    
    try {
      setIsClassifying(true);
      // 1. Take compressed photo
      const photo = await cameraRef.current.takePictureAsync({ quality: 0.7 });
      
      // 2. Call backend API
      const result = await classifyImage(photo.uri, 'berkeley');
      
      // 3. Navigate to result modal with payload
      navigation.navigate('ResultModal', {
        itemName: result.label || result.detected_item,
        category: result.category,
        confidence: result.confidence,
        tip: result.disposal_tip || result.rules?.guideline
      });
    } catch (error) {
      Alert.alert(
        'Scan Failed',
        'Could not classify item. Please check network connection and try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsClassifying(false);
    }
  };

  return (
    <View style={styles.container}>
      <CameraView style={styles.camera} ref={cameraRef}>
        {/* Reticle guide */}
        <View style={styles.reticle} />

        {isClassifying ? (
          <View style={styles.loadingOverlay}>
            <ActivityIndicator size="large" color="#FFFFFF" />
            <Text style={styles.loadingText}>Analyzing item with Sortify AI...</Text>
          </View>
        ) : (
          <View style={styles.bottomBar}>
            <TouchableOpacity style={styles.shutter} onPress={handleCaptureAndAnalyze} />
          </View>
        )}
      </CameraView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  camera: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  reticle: { width: 240, height: 240, borderWidth: 2, borderColor: 'rgba(255,255,255,0.7)', borderRadius: 16 },
  loadingOverlay: { ...StyleSheet.absoluteFillObject, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'center', alignItems: 'center' },
  loadingText: { color: '#FFF', marginTop: 12, fontWeight: '600' },
  bottomBar: { position: 'absolute', bottom: 40, width: '100%', alignItems: 'center' },
  shutter: { width: 72, height: 72, borderRadius: 36, backgroundColor: '#FFF' }
});
```

---

# Week 5 — Core MVP Build (Part 2: Rules Engine & Demo Hardening)

---

### Mong (Week 5)
* **Task:** Location Selector Modal Component
* **Target File / Output:** `src/components/LocationSelector.js`
* **Starter Guidance & Structure:**

```javascript
// src/components/LocationSelector.js
import React from 'react';
import { View, Text, StyleSheet, Modal, TouchableOpacity, FlatList } from 'react-native';

const CITIES = [
  { id: 'berkeley', name: 'UC Berkeley / City of Berkeley 🐻', tag: 'Local Campus Rules' },
  { id: 'san_francisco', name: 'San Francisco (SF Environment) 🌁', tag: 'Strict Zero-Waste' },
  { id: 'oakland', name: 'Oakland (Alameda County) 🌳', tag: 'StopWaste' },
];

export default function LocationSelector({ visible, selectedCity, onSelectCity, onClose }) {
  return (
    <Modal visible={visible} animationType="slide" transparent>
      <View style={styles.overlay}>
        <View style={styles.sheet}>
          <Text style={styles.title}>Select Sorting Municipality</Text>
          <FlatList
            data={CITIES}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <TouchableOpacity 
                style={[styles.cityItem, selectedCity === item.id && styles.activeItem]}
                onPress={() => { onSelectCity(item.id); onClose(); }}
              >
                <Text style={styles.cityName}>{item.name}</Text>
                <Text style={styles.cityTag}>{item.tag}</Text>
              </TouchableOpacity>
            )}
          />
          <TouchableOpacity style={styles.closeBtn} onPress={onClose}>
            <Text style={styles.closeBtnText}>Cancel</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'flex-end' },
  sheet: { backgroundColor: '#FFF', borderTopLeftRadius: 20, borderTopRightRadius: 20, padding: 20 },
  title: { fontSize: 18, fontWeight: '700', marginBottom: 16 },
  cityItem: { padding: 14, borderRadius: 10, marginBottom: 8, backgroundColor: '#F8FAFC' },
  activeItem: { borderColor: '#16A34A', borderWidth: 1.5, backgroundColor: '#F0FDF4' },
  cityName: { fontWeight: '600', fontSize: 15 },
  cityTag: { fontSize: 12, color: '#64748B', marginTop: 2 },
  closeBtn: { marginTop: 12, padding: 14, alignItems: 'center' },
  closeBtnText: { color: '#64748B', fontWeight: '600' }
});
```

---

### Caden (Week 5)
* **Task:** Location State Integration & Error Boundary Hardening
* **Target File / Output:** `src/context/LocationContext.js`
* **Starter Guidance & Structure:**

```javascript
// src/context/LocationContext.js
import React, { createContext, useState, useContext } from 'react';

const LocationContext = createContext();

export function LocationProvider({ children }) {
  const [selectedLocation, setSelectedLocation] = useState('berkeley');

  return (
    <LocationContext.Provider value={{ selectedLocation, setSelectedLocation }}>
      {children}
    </LocationContext.Provider>
  );
}

export function useLocation() {
  return useContext(LocationContext);
}
```

---

# Week 6 — Mid-Semester Presentation (Demo Video & Retro)

---

### Mong (Week 6)
* **Task:** UI Responsiveness Audit & Demo Flow Styling
* **Target File / Output:** `src/styles/responsive.js` & visual inspection check
* **Starter Guidance & Structure:**

```javascript
// src/styles/responsive.js
import { Dimensions, PixelRatio } from 'react-native';

const { width, height } = Dimensions.get('window');

// Guideline sizes based on standard iPhone 14 / 390x844
const guidelineBaseWidth = 390;
const guidelineBaseHeight = 844;

export const scale = (size) => (width / guidelineBaseWidth) * size;
export const verticalScale = (size) => (height / guidelineBaseHeight) * size;
export const moderateScale = (size, factor = 0.5) => size + (scale(size) - size) * factor;

// Verify activeOpacity consistency across buttons
export const BUTTON_TOUCH_OPACITY = 0.7;
```

---

### Caden (Week 6)
* **Task:** App Demo Video Recording Walkthrough Script
* **Target File / Output:** `docs/midsem_demo_script.md`
* **Starter Guidance & Structure:**

```markdown
<!-- docs/midsem_demo_script.md -->
# 90-Second Demo Video Recording Script

- **0:00 - 0:15:** App launch into Home Screen showing campus streak & Cal Bear banner.
- **0:15 - 0:35:** Camera Scan 1: Paper cup placed on desk. Show instant classification, confidence bar (94%), and compost recommendation.
- **0:35 - 0:55:** Camera Scan 2: Plastic water bottle. Show Blue Plastic bin designation and cap removal tip.
- **0:55 - 1:15:** Location Switch: Open Location Selector, switch to San Francisco. Re-scan compostable container showing SF Recology specifics.
- **1:15 - 1:30:** Closing summary of technical architecture & upcoming Week 7-12 roadmap.
```

---

# Week 7 — Authentication & User Accounts

---

### Mong (Week 7)
* **Task:** Login, Register & Password Recovery Screens
* **Target File / Output:** `src/screens/LoginScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/LoginScreen.js
import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { useAuth } from '../context/AuthContext';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSignIn = async () => {
    setErrorMsg('');
    // Validate Berkeley email domain
    if (!email.toLowerCase().endsWith('@berkeley.edu')) {
      setErrorMsg('Please use your @berkeley.edu student email.');
      return;
    }

    try {
      setIsLoading(true);
      await login(email, password);
      // Navigation is handled automatically via AuthContext state
    } catch (err) {
      setErrorMsg(err.message || 'Invalid email or password.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Sign in to Sortify</Text>
      {errorMsg ? <Text style={styles.errorBanner}>{errorMsg}</Text> : null}

      <TextInput
        style={styles.input}
        placeholder="student@berkeley.edu"
        autoCapitalize="none"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
      />

      <TouchableOpacity style={styles.button} onPress={handleSignIn} disabled={isLoading}>
        {isLoading ? <ActivityIndicator color="#FFF" /> : <Text style={styles.buttonText}>Sign In</Text>}
      </TouchableOpacity>

      <TouchableOpacity onPress={() => navigation.navigate('Register')}>
        <Text style={styles.linkText}>Don't have an account? Sign Up</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: 'center', backgroundColor: '#FFF' },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20 },
  input: { borderWidth: 1, borderColor: '#CBD5E1', borderRadius: 8, padding: 12, marginBottom: 12 },
  button: { backgroundColor: '#16A34A', padding: 14, borderRadius: 8, alignItems: 'center', marginTop: 8 },
  buttonText: { color: '#FFF', fontWeight: 'bold' },
  errorBanner: { color: '#DC2626', backgroundColor: '#FEE2E2', padding: 10, borderRadius: 6, marginBottom: 12 },
  linkText: { color: '#2563EB', textAlign: 'center', marginTop: 16 }
});
```

---

### Caden (Week 7)
* **Task:** Firebase Auth Integration & React AuthContext
* **Target File / Output:** `src/context/AuthContext.js`
* **Starter Guidance & Structure:**

```javascript
// src/context/AuthContext.js
import React, { createContext, useState, useEffect, useContext } from 'react';
import * as SecureStore from 'expo-secure-store';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check SecureStore on launch for existing auth token
    const loadSession = async () => {
      try {
        const storedToken = await SecureStore.getItemAsync('user_token');
        if (storedToken) {
          setToken(storedToken);
          // TODO: Verify token validity against /api/user/profile
        }
      } catch (e) {
        console.error('Failed to load session:', e);
      } finally {
        setLoading(false);
      }
    };
    loadSession();
  }, []);

  const login = async (email, password) => {
    // TODO: Call backend /api/auth/login or Firebase Client SDK
    // TODO: Store returned JWT token in SecureStore.setItemAsync('user_token', idToken)
  };

  const logout = async () => {
    await SecureStore.deleteItemAsync('user_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
```

---

# Week 8 — Engagement Tracker, Streaks & Gamification

---

### Mong (Week 8)
* **Task:** Stats & Gamification Dashboard UI
* **Target File / Output:** `src/screens/StatsScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/StatsScreen.js
import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { TYPOGRAPHY, COLORS } from '../styles/theme';

export default function StatsScreen() {
  const [refreshing, setRefreshing] = useState(false);
  const [stats, setStats] = useState({
    streak_days: 5,
    eco_points: 120,
    items_sorted: 24,
    categories: { compost: 10, plastic: 8, paper: 4, glass: 2 }
  });

  const onRefresh = async () => {
    setRefreshing(true);
    // TODO: Fetch latest stats from GET /api/stats
    setRefreshing(false);
  };

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <Text style={styles.title}>Your Eco Impact</Text>
      
      {/* Streak Badge */}
      <View style={styles.streakBox}>
        <Text style={styles.streakEmoji}>🔥</Text>
        <Text style={styles.streakDays}>{stats.streak_days} Day Streak</Text>
      </View>

      {/* Metric Counters */}
      <View style={styles.counterRow}>
        <View style={styles.counterCard}>
          <Text style={styles.counterNumber}>{stats.eco_points}</Text>
          <Text style={styles.counterLabel}>Eco Points</Text>
        </View>
        <View style={styles.counterCard}>
          <Text style={styles.counterNumber}>{stats.items_sorted}</Text>
          <Text style={styles.counterLabel}>Items Sorted</Text>
        </View>
      </View>

      {/* TODO: Add Pie Chart or Breakdown Bar using stats.categories */}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#F8FAFC' },
  title: { ...TYPOGRAPHY.header, marginBottom: 16 },
  streakBox: { backgroundColor: '#FFFBEB', padding: 20, borderRadius: 12, alignItems: 'center', marginBottom: 16 },
  streakEmoji: { fontSize: 36 },
  streakDays: { fontSize: 20, fontWeight: 'bold', color: '#B45309' },
  counterRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 16 },
  counterCard: { width: '48%', backgroundColor: '#FFF', padding: 16, borderRadius: 12, alignItems: 'center', borderWidth: 1, borderColor: '#E2E8F0' },
  counterNumber: { fontSize: 24, fontWeight: 'bold', color: COLORS.accent.berkeleyBlue },
  counterLabel: { fontSize: 12, color: '#64748B', marginTop: 4 }
});
```

---

### Caden (Week 8)
* **Task:** History Screen with FlatList & Auto-Logging
* **Target File / Output:** `src/screens/HistoryScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/HistoryScreen.js
import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, RefreshControl } from 'react-native';
import { COLORS } from '../styles/theme';

export default function HistoryScreen() {
  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchHistory = async () => {
    // TODO: Execute GET /api/history with user bearer token
    // Sample mock item structure:
    // { id: '1', item_name: 'Almond Milk Carton', category: 'compost', timestamp: '2026-09-20T14:30:00Z' }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const renderItem = ({ item }) => (
    <View style={styles.itemCard}>
      <View style={[styles.badge, { backgroundColor: COLORS.bins[item.category] || '#999' }]}>
        <Text style={styles.badgeText}>{item.category?.toUpperCase()}</Text>
      </View>
      <View style={styles.itemDetails}>
        <Text style={styles.itemName}>{item.item_name}</Text>
        <Text style={styles.itemDate}>{new Date(item.timestamp).toLocaleDateString()}</Text>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={historyItems}
        keyExtractor={(item) => item.id}
        renderItem={renderItem}
        refreshControl={<RefreshControl refreshing={loading} onRefresh={fetchHistory} />}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>No scans yet! Snap an item to begin.</Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8FAFC', padding: 16 },
  itemCard: { flexDirection: 'row', backgroundColor: '#FFF', padding: 14, borderRadius: 10, marginBottom: 10, alignItems: 'center' },
  badge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 6, marginRight: 12 },
  badgeText: { color: '#FFF', fontSize: 11, fontWeight: '700' },
  itemDetails: { flex: 1 },
  itemName: { fontWeight: '600', fontSize: 15 },
  itemDate: { fontSize: 12, color: '#94A3B8', marginTop: 2 },
  emptyContainer: { padding: 40, alignItems: 'center' },
  emptyText: { color: '#64748B' }
});
```

---

# Week 9 — System Integration Testing & Robustness

---

### Mong (Week 9)
* **Task:** Loading Skeletons & Accessibility Attributes
* **Target File / Output:** `src/components/SkeletonCard.js`
* **Starter Guidance & Structure:**

```javascript
// src/components/SkeletonCard.js
import React, { useEffect, useRef } from 'react';
import { View, Animated, StyleSheet } from 'react-native';

export default function SkeletonCard() {
  const opacityAnim = useRef(new Animated.Value(0.3)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(opacityAnim, { toValue: 1, duration: 800, useNativeDriver: true }),
        Animated.timing(opacityAnim, { toValue: 0.3, duration: 800, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  return (
    <Animated.View style={[styles.skeleton, { opacity: opacityAnim }]} 
      accessible={true} 
      accessibilityLabel="Loading content"
    />
  );
}

const styles = StyleSheet.create({
  skeleton: { height: 72, backgroundColor: '#E2E8F0', borderRadius: 10, marginBottom: 12, width: '100%' }
});
```

---

### Caden (Week 9)
* **Task:** Camera Lifecycle Memory Optimization & Unmounting
* **Target File / Output:** `src/screens/ScanScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/ScanScreen.js (Navigation focus listener snippet)
import React, { useState } from 'react';
import { useIsFocused } from '@react-navigation/native';
import { CameraView } from 'expo-camera';

export default function ScanScreen() {
  const isFocused = useIsFocused();

  // Explicitly unmount CameraView hardware stream when screen loses focus
  if (!isFocused) {
    return null;
  }

  return (
    <CameraView style={{ flex: 1 }}>
      {/* Viewfinder UI */}
    </CameraView>
  );
}
```

---

# Week 10 — Production Hardening & UX Polish

---

### Mong (Week 10)
* **Task:** First-Time Onboarding Walkthrough & Dark Mode Support
* **Target File / Output:** `src/screens/OnboardingScreen.js`
* **Starter Guidance & Structure:**

```javascript
// src/screens/OnboardingScreen.js
import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function OnboardingScreen({ navigation }) {
  const handleFinishOnboarding = async () => {
    await AsyncStorage.setItem('has_completed_onboarding', 'true');
    navigation.replace('MainTabs');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.stepTitle}>Snap Your Trash 📸</Text>
      <Text style={styles.stepBody}>Point your phone at any waste item on campus to instantly find the correct bin.</Text>
      
      <TouchableOpacity style={styles.getStartedBtn} onPress={handleFinishOnboarding}>
        <Text style={styles.getStartedText}>Get Started</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 32, justifyContent: 'center', alignItems: 'center', backgroundColor: '#FFF' },
  stepTitle: { fontSize: 24, fontWeight: '700', marginBottom: 12 },
  stepBody: { fontSize: 16, color: '#64748B', textAlign: 'center', marginBottom: 32 },
  getStartedBtn: { backgroundColor: '#16A34A', paddingVertical: 14, paddingHorizontal: 32, borderRadius: 12 },
  getStartedText: { color: '#FFF', fontWeight: 'bold', fontSize: 16 }
});
```

---

### Caden (Week 10)
* **Task:** Haptic Feedback & Safe Area Padding Audit
* **Target File / Output:** `src/utils/haptics.js`
* **Starter Guidance & Structure:**

```javascript
// src/utils/haptics.js
import * as Haptics from 'expo-haptics';
import { Platform } from 'react-native';

export function triggerShutterHaptic() {
  if (Platform.OS === 'web') return;
  Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
}

export function triggerSuccessHaptic() {
  if (Platform.OS === 'web') return;
  Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
}

export function triggerErrorHaptic() {
  if (Platform.OS === 'web') return;
  Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
}
```

---

# Week 11 — Stretch Goals & Deployment

---

### Mong (Week 11)
* **Task:** App Store Mockups & Visual Portfolio Assets
* **Target File / Output:** `docs/portfolio_assets/README.md`
* **Starter Guidance & Structure:**

```markdown
<!-- docs/portfolio_assets/README.md -->
# Sortify Portfolio Asset Manifest

Export high-resolution iPhone 14 frame mockups into this directory:
- `01_home_streak_hero.png` (390x844 @ 2x)
- `02_camera_reticle_live.png`
- `03_result_modal_compost.png`
- `04_municipal_selector_rules.png`
```

---

### Caden (Week 11)
* **Task:** EAS Build Configuration & Standalone Preview APK
* **Target File / Output:** `eas.json`
* **Starter Guidance & Structure:**

```json
{
  "cli": {
    "version": ">= 7.0.0"
  },
  "build": {
    "preview": {
      "android": {
        "buildType": "apk"
      },
      "distribution": "internal"
    },
    "production": {}
  }
}
```

---

# Week 12 — Final Presentation & Portfolio Release

---

### Mong (Week 12)
* **Task:** Mobile Architecture Documentation & Code Polish
* **Target File / Output:** `mobile/README.md`
* **Starter Guidance & Structure:**

```markdown
<!-- mobile/README.md -->
# Sortify Mobile Client (`sortify-app`)

## Architecture & Directory Structure
- `src/screens/`: Screen views (Home, Scan, Result, History, Stats, Profile).
- `src/components/`: Reusable design system elements (LocationSelector, SkeletonCard).
- `src/context/`: AuthContext and LocationContext global state.
- `src/services/`: API client (`api.js`) and Firebase integration.
- `src/styles/`: Theme tokens (`COLORS`, `SPACING`, `TYPOGRAPHY`).

## Quickstart
```bash
npm install
npx expo start
```
```

---

### Caden (Week 12)
* **Task:** Final 2-Minute Presentation Demo Video Script
* **Target File / Output:** `docs/final_demo_script.md`
* **Starter Guidance & Structure:**

```markdown
<!-- docs/final_demo_script.md -->
# Final 2-Minute Presentation Walkthrough

- **0:00 - 0:20:** User Registration & Firebase Auth login session.
- **0:20 - 0:50:** Scanning 3 diverse waste items (food container, bottle, greasy box) with live AI inference.
- **0:50 - 1:15:** Municipal rules shift: Berkeley to SF Recology guidelines update.
- **1:15 - 1:35:** Real-time streak increment, points awarded, and updated History list.
- **1:35 - 2:00:** Impact summary & open-source repository overview.
```
