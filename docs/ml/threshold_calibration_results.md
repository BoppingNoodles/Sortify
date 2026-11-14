# Confidence Threshold Calibration Results

Checkpoint: `ml/models/sortify_v2.pth`

| Cutoff | Precision | Rejection Rate | Accepted |
|--------|-----------|----------------|----------|
| 0.40 | 90.08% | 2.27% | 474/485 |
| 0.50 | 90.56% | 3.92% | 466/485 |
| 0.60 | 93.35% | 10.10% | 436/485 |

## Confidence score distribution

| Group | Count | Mean | Median | Min | Max |
|-------|-------|------|--------|-----|-----|
| correct | 428 | 0.934 | 0.983 | 0.369 | 1.000 |
| incorrect | 57 | 0.636 | 0.601 | 0.276 | 0.970 |

**Selected threshold:** `0.40` (lowest cutoff with precision >= 90%, else highest precision).

## Verification

- Clear images passing: 90.0% of 10
- Blurry/ambiguous images flagged uncertain: 9.1% of 11

## Backend handoff

`CONFIDENCE_THRESHOLD = 0.40`

In `POST /api/classify`, if the top softmax probability is below the threshold, return `"uncertain": true` with advice to check physical bin signs.
