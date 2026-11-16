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

## Verification

| Cutoff | Precision | Clear accepted | Blurry flagged uncertain |
|--------|-----------|----------------|--------------------------|
| 0.40 | 90.08% | 90.0% | 9.1% |
| 0.50 | 90.56% | 90.0% | 27.3% |
| 0.60 | 93.35% | 90.0% | 45.5% |

## Backend handoff

No cutoff passed the configured verification criteria, or verification was skipped.
