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
    onGreen: '#173208',
    greenText: '#2D7800',
    greenTint: '#E6F7DC',
    blueTint: '#E2F5FC',
    welcome: '#F4FCF6',
    points: '#E8F5E9',
    pointsText: '#2E7D32',
    streak: '#FFF3E0',
    streakBorder: '#FFE0B2',
    streakText: '#BF360C',
    thumbnailBorder: '#CBD5E1',
  },
  accent: {
    berkeleyBlue: '#006B91',
    californiaGold: '#FDB515',
  },
};

const DARK_COLORS = {
  bins: {
    plastic: '#79AFFF',
    compost: '#68D791',
    paper: '#F8B96A',
    glass: '#58D1C6',
    landfill: '#AEBAC8',
  },
  background: {
    primary: '#121A1E',
    card: '#19252A',
    surface: '#25343B',
  },
  text: {
    primary: '#F0F5F7',
    secondary: '#BDCCD2',
    muted: '#A2B6BF',
    inverse: '#121A1E',
  },
  design: {
    border: '#41545D',
    progress: '#354951',
    green: '#8ADD66',
    onGreen: '#173208',
    greenText: '#A1E785',
    greenTint: '#273F2D',
    blueTint: '#203A46',
    welcome: '#121A1E',
    points: '#273F2D',
    pointsText: '#A1E785',
    streak: '#3E3024',
    streakBorder: '#795438',
    streakText: '#FFC698',
    thumbnailBorder: '#546B76',
  },
  accent: {
    berkeleyBlue: '#87D6F4',
    californiaGold: '#FDB515',
  },
};

export function getAppColors(scheme) {
  return scheme === 'dark' ? DARK_COLORS : COLORS;
}

export function createThemedStyles(createStyles) {
  const light = { colors: COLORS, styles: createStyles(COLORS) };
  const dark = { colors: DARK_COLORS, styles: createStyles(DARK_COLORS) };
  return (scheme) => scheme === 'dark' ? dark : light;
}

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
