# Expanded Training Data Summaries

Numerical outlier counts use the 1.5 IQR rule and do not by themselves justify removing observations. These tables supplement the revised proposal; model interpretations and limitations are in the English analysis supplement.

| Variable | Type (reference level) | Training-set summary |
|:--------------------|:----------------|:----------------------------------------|
| Sale price, $1000s (response) | Numerical | Mean 527, SD 307, min 210, median 433, max 3,300; skewness 3.04 |
| Floor area, 100 sq ft | Numerical | Mean 25.4, SD 9.9, min 7.1, median 23.0, max 85.1; skewness 1.67 |
| Lot size, 1000 sq ft | Numerical | Mean 14.1, SD 16.6, min 2.0, median 8.7, max 87.1; skewness 3.10 |
| Month of sale (1–12) | Numerical | Mean 6.3, SD 3.4, min 1, median 6, max 12; skewness 0.09 |
| Census division | 9 levels (South Atlantic) | South Atlantic 1,308; New England 39; Middle Atlantic 119; East North Central 510; West North Central 313; East South Central 344; West South Central 850; Mountain 473; Pacific 374 |
| Stories | 3 (one) | 1: 2,120; 2: 2,116; 3+: 94 |
| Bedrooms | 4 (two or fewer) | ≤2: 154; 3: 1,780; 4: 1,777; 5+: 619 |
| Full bathrooms | 4 (one or fewer) | ≤1: 46; 2: 2,664; 3: 1,203; 4+: 417 |
| Half bathrooms | 3 (none) | 0: 2,373; 1: 1,897; 2+: 60 |
| Garage | 4 (one-car) | 1-car: 158; 2-car: 3,124; 3+-car: 919; other: 129 |
| Foundation | 4 (basement) | Basement: 992; crawl space: 403; slab: 2,926; other: 9 |
| Fireplaces | 3 (none) | 0: 2,781; 1: 1,383; 2+: 166 |
| Homeowners' association | 2 (no) | No: 1,109; yes: 3,221 |
| Age-restricted community | 2 (no) | No: 4,216; yes: 114 |
| Exterior wall material | 7 (brick) | Brick 897; wood 169; stucco 906; vinyl 1,362; stone 56; fiber cement 926; other 14 |
| Heating fuel | 4 (electricity) | Electricity 2,147; natural gas 2,083; propane 52; other 48 |
| Sewer | 2 (public) | Public 3,893; septic or other 437 |
| Construction stage at sale | 3 (completed) | Completed 2,452; under construction 1,344; not started 534 |
