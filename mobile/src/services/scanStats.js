function localDayOrdinal(date) {
  return Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()) / 86_400_000;
}

export function summarizeScans(scans, now = new Date()) {
  const breakdown = { compost: 0, plastic: 0, paper: 0, glass: 0, landfill: 0 };
  const days = new Set();

  for (const scan of scans) {
    const category = (scan.category || '').toLowerCase();
    breakdown[Object.hasOwn(breakdown, category) ? category : 'landfill'] += 1;
    if (scan.timestamp) {
      const day = localDayOrdinal(new Date(scan.timestamp));
      if (Number.isFinite(day)) days.add(day);
    }
  }

  const today = localDayOrdinal(now);
  let day = days.has(today) ? today : today - 1;
  let currentStreak = 0;
  while (days.has(day)) {
    currentStreak += 1;
    day -= 1;
  }

  return {
    currentStreak,
    totalScans: scans.length,
    ecoPoints: scans.length * 10,
    breakdown,
  };
}
