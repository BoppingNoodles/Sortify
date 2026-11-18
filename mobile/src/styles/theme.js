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
    primary: '#F4F8FA',
    card: '#FFFFFF',
    surface: '#F2F6F7',
  },
  text: {
    primary: '#202E39',
    secondary: '#566D7B',
    muted: '#627988',
    inverse: '#FFFFFF',
  },
  design: {
    border: '#DDE6EA',
    progress: '#E3EAED',
    green: '#51C900',
    greenText: '#2D7800',
    greenTint: '#E6F7DC',
    blueTint: '#E2F5FC',
  },
  accent: {
    berkeleyBlue: '#006B91',
    californiaGold: '#FDB515',
  },
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
