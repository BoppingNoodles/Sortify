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
