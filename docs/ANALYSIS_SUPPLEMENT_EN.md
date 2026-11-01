# English Analysis Supplement


These sections describe exploratory training-set work already present in the project repositories. They are separate from the uncorrected preliminary results in the Part 1 proposals. The numbers below are training fit and sensitivity results unless a different sample is explicitly identified. They are not held-out predictive performance.


## New home prices

### Data construction and specification

The source file contains 25,246 SOC records. Filtering leaves 16,849 homes built for sale, 8,901 with a 2025 sales contract, 8,532 with reported price, 7,062 detached homes outside condominium projects, 6,315 with reported floor and lot area, and 6,185 with valid categorical codes. The fixed split contains 4,330 training and 1,855 test homes.

The preliminary response is price in thousands of dollars. Its 17 predictors are floor area, division, lot size, sale month, stories, bedrooms, full bathrooms, half bathrooms, garage, foundation, fireplaces, homeowners' association, age restriction, wall material, heating fuel, sewer and sale stage. Floor area interacts with division. Category indicators count as levels of a predictor, not separate predictors for the course minimum. Sale stage is constructed from dates; lot value, permit valuation and final-price fields are excluded to avoid mechanically explaining price with its components or proxies.

### Transformations and selection

The Box–Cox profile for the preliminary response peaks at approximately −0.421, with a 95% profile interval of −0.470 to −0.372. Both logarithmic and approximately inverse-square-root responses were explored. A log response was retained for interpretation, with log floor area addressing curvature; this choice is a trade-off, not a claim that every assumption is satisfied. Log floor area was centred to reduce structural collinearity.

Grouped backward BIC selection retained the focal interaction and lot size, while removing homeowners' association, age restriction, sewer, sale month and sale stage. AIC retained more controls. The final training specification has log price as response and log floor area by division, lot size, stories, bedrooms, both bathroom counts, garage, foundation, fireplaces, wall material and heating fuel as predictors. It contains 46 coefficients.

| Measure | Preliminary | Selected log model |
|---|---|---|
| R² / adjusted R² | 0.713 / 0.710 | 0.756 / 0.753 |
| Residual skewness / excess kurtosis | 2.04 / 18.0 | 0.48 / 2.52 |
| Largest Cook distance | 0.18 | 0.022 |
| Interaction HC3 p | 7.5e-24 | 1.6e-10 |

R² changes across response scales should not be read as a direct improvement in original-dollar predictive accuracy. The final residuals remain imperfect; neither the transformation nor a small interaction p-value establishes independent errors.

### Regional estimates and sensitivity

| Division | Log-model elasticity | 95% interval | Associated price difference for 10% more area |
|---|---|---|---|
| South Atlantic | 0.679 | 0.630–0.727 | 6.7% |
| New England | 0.632 | 0.448–0.815 | 6.2% |
| Middle Atlantic | 0.735 | 0.633–0.837 | 7.3% |
| East North Central | 0.525 | 0.462–0.589 | 5.1% |
| West North Central | 0.535 | 0.462–0.608 | 5.2% |
| East South Central | 0.702 | 0.628–0.775 | 6.9% |
| West South Central | 0.734 | 0.677–0.791 | 7.2% |
| Mountain | 0.584 | 0.523–0.645 | 5.7% |
| Pacific | 0.727 | 0.650–0.804 | 7.2% |

The interaction persists under alternative interactions, survey weighting, exclusion of disclosure-coded prices and AIC selection. Adding all seven rival interactions gives HC3 p=1.3e-7 for the focal interaction block. However, the East-North-Central-versus-South-Atlantic contrast becomes inconclusive in that demanding specification (p≈0.076). The broader Midwest contrast is more stable: the elasticity difference is approximately −0.152; division-clustered inference using t with eight degrees of freedom gives p≈0.00059. With only nine divisions, an eight-parameter cluster-robust joint test is not a reliable substitute for this limited contrast.

Applying the selected specification to 6,118 homes sold in 2024 gives R²=0.752 and interaction HC3 p=1.2e-17. The repository treats this as a different-house replication sample. It does not establish transportability to every future housing market. The final interaction alone adds only about 0.003 to R², even though it is statistically detectable.

### Remaining limitations and disclosure

New England has only 39 training homes. Price and other variables have disclosure coding; complete-case filtering changes the analysed population. Geography is too coarse to identify builder or subdivision clustering. A near-zero residual division ICC after including division effects is partly an algebraic consequence and is not proof of independence. Full-sample division-level descriptive statistics were viewed before the fixed split; the current test set therefore is not completely untouched. Estimates describe associations, not the value caused by enlarging a particular house.

