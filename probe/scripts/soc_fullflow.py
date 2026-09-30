"""SOC full workflow tables (raw data profile -> variables -> Part 1 model -> Part 2 remedies & selection -> final model).
TRAINING split (70%, seed 302) only. Writes results/soc_fullflow.json, tables/*.csv and figures/soc_part1_grid.png, soc_final_grid.png
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from utils import *
import statsmodels.formula.api as smf

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(f"{BASE}/results/tables", exist_ok=True)
out = {}
# ---------------- 1. raw data profile ----------------
raw = pd.read_csv(f"{BASE}/data/soc/soc25.csv")
out["raw_shape"] = list(raw.shape)
sold = raw[(raw.CAT == 1) & (raw.SALE >= 202501) & (raw.SALE <= 202512)]
prof = {"n_sold_2025": len(sold), "SLPR_not_reported(0)": int((sold.SLPR == 0).sum()),
        "SLPR_top_or_bottom_coded(SLPR_F=1)": int((sold.SLPR_F == 1).sum()),
        "SLPR_min": float(sold.SLPR[sold.SLPR > 0].min()), "SLPR_max": float(sold.SLPR.max()),
        "SQFS_not_reported(0)": int((sold.SQFS == 0).sum()), "SQFS_coded(SQFS_F=1)": int((sold.SQFS_F == 1).sum()),
        "AREA_not_reported(0)": int((sold.AREA == 0).sum()), "AREA_coded(AREA_F=1)": int((sold.AREA_F == 1).sum()),
        "AREA_at_topcode_87120": int((sold.AREA == 87120).sum()), "AREA_at_bottomcode_2000": int((sold.AREA == 2000).sum()),
        "attached_or_condo": int(((sold.DET == 2) | (sold.CON == 1)).sum())}
for c, codes in {"STOR": [0], "BEDR": [0], "FULB": [9], "HAFB": [9], "GAR": [0], "BASE": [0], "FPLS": [9], "ASSOC": [0],
                 "AGER": [0], "WAL1": [0], "FUEL": [0], "SEWER": [0], "FINC": [0], "ACS": [0]}.items():
    prof[f"{c}_not_reported"] = int(sold[c].isin(codes).sum())
out["raw_profile_sold2025"] = prof

# ---------------- 2/3. analysis data & variable table ----------------
df = pd.read_csv(f"{BASE}/data/soc/soc_analysis.csv")
divs = ["SouthAtlantic", "NewEngland", "MidAtlantic", "ENCentral", "WNCentral", "ESCentral", "WSCentral", "Mountain", "Pacific"]
df["division"] = pd.Categorical(df.division, categories=divs)
train, test = split70(df)
num = ["price_k", "sqft100", "lot_k", "sale_month"]
cat = ["division", "stories", "bedrooms", "fullbath", "halfbath", "garage", "foundation", "fireplace", "hoa", "age_restricted",
       "wall", "heat_fuel", "sewer", "stage"]
vt = pd.DataFrame(describe_train(train, num, cat))
vt.to_csv(f"{BASE}/results/tables/soc_variable_table_train.csv", index=False)
out["variable_table"] = vt.to_dict(orient="records")

# ---------------- 5. Part 1 model ----------------
controls = ("lot_k + C(stories) + C(bedrooms) + C(fullbath) + C(halfbath) + C(garage) + C(foundation)"
            " + C(fireplace) + C(hoa) + C(age_restricted) + C(wall) + C(heat_fuel) + C(sewer) + C(stage) + sale_month")
F1 = "price_k ~ sqft100 * division + " + controls
m1, m13 = fit(F1, train)
ct = pd.DataFrame(coef_table(m1, m13, list(m1.params.index)))
ct.to_csv(f"{BASE}/results/tables/soc_part1_coefficients.csv", index=False)
grid_plots(m1, f"{BASE}/figures/soc_part1_grid.png", "SOC Part 1 model (raw price, $1000s) - training set", xvar="sqft100", data=train)
d1 = diagnostics(m1)
out["part1"] = {"formula": F1, "k_params": int(m1.df_model + 1), "diag": d1,
                "boxcox": boxcox_lambda(m1, train.price_k),
                "resid_vs_sqft_lowess_note": "see soc_part1_grid.png panel 4"}

# ---------------- 6. Part 2 remedies ----------------
train["log_price"] = np.log(train.price_k)
train["log_sqft"] = np.log(train.sqft100 * 100)
# (a) response transformation candidates
cands = {}
for name, f in {"log_price ~ sqft100": "log_price ~ sqft100 * division + " + controls,
                "log_price ~ log_sqft": "log_price ~ log_sqft * division + " + controls}.items():
    mm = smf.ols(f, data=train).fit()
    dd = diagnostics(mm)
    cands[name] = {"R2": mm.rsquared, "adjR2": mm.rsquared_adj, "BIC": mm.bic, "skew": dd["resid_skew"], "exkurt": dd["resid_exkurt"], "BP_p": dd["BP_p"]}
out["part2_transform_candidates"] = cands
# (b) curvature in sqft on log scale
mq = smf.ols("log_price ~ sqft100 * division + I(sqft100**2) + " + controls, data=train).fit()
ml_ = smf.ols("log_price ~ sqft100 * division + " + controls, data=train).fit()
fq, pq, _ = mq.compare_f_test(ml_)
out["part2_sqft_squared_test"] = {"F": fq, "p": pq, "coef": float(mq.params["I(sqft100 ** 2)"])}
# (c) backward selection (BIC and AIC) on the log model; research-question terms forced
forced = ["log_sqft", "division", "log_sqft:division", "lot_k"]
candidates = ["C(stories)", "C(bedrooms)", "C(fullbath)", "C(halfbath)", "C(garage)", "C(foundation)", "C(fireplace)",
              "C(hoa)", "C(age_restricted)", "C(wall)", "C(heat_fuel)", "C(sewer)", "C(stage)", "sale_month"]
kept_bic, hist_bic = backward_select(train, "log_price", forced, candidates, "BIC")
kept_aic, hist_aic = backward_select(train, "log_price", forced, candidates, "AIC")
out["part2_backward_BIC"] = {"kept": kept_bic, "history": hist_bic}
out["part2_backward_AIC"] = {"kept": kept_aic, "history": hist_aic}
# (d) final candidate model = BIC-selected log model
F2 = "log_price ~ " + " + ".join(["log_sqft * division", "lot_k"] + kept_bic)
m2, m23 = fit(F2, train)
m2r, _ = fit(F2.replace("log_sqft * division", "log_sqft + division"), train)
m2x, _ = fit(F2.replace("log_sqft * division", "division"), train)
d2 = diagnostics(m2, clusters={"division": train.division.astype(str)})
grid_plots(m2, f"{BASE}/figures/soc_final_grid.png", "SOC Part 2 candidate final model (log price, BIC-selected) - training set", xvar="sqft100", data=train)
sl2 = {}
for lev in divs:
    w = {"log_sqft": 1.0}
    if lev != "SouthAtlantic":
        w[f"log_sqft:division[T.{lev}]"] = 1.0
    lc = lincomb(m2, m23, w)
    lc["pct_per_10pct_more_sqft"] = 100 * (1.1 ** lc["est"] - 1)
    xs = train.log_sqft[train.division == lev]
    lc["n_train"] = int(len(xs))
    lc["p10_p90_within_group"] = pct_effect(lc["est"], xs, float(train.log_price.std()))
    sl2[lev] = lc
out["final"] = {"formula": F2, "k_params": int(m2.df_model + 1), "diag": d2, "gvif_top": gvif(m2)[:4],
                "gvif_main_effects_top": gvif(smf.ols(F2.replace("log_sqft * division", "log_sqft + division"), data=train).fit())[:4],
                "interaction_partialF": partial_f(m2, m2r), "interaction_wald_hc3": wald_hc3(m2, m23, ["log_sqft:division"]),
                "dR2_X_and_XxG": partial_f(m2, m2x)["delta_R2"], "slopes": sl2}
pd.DataFrame(coef_table(m2, m23, list(m2.params.index))).to_csv(f"{BASE}/results/tables/soc_final_coefficients.csv", index=False)
# (e) WLS for remaining heteroscedasticity: weights from regressing |resid| on fitted values (two-step FGLS)
aux = smf.ols("absr ~ fitted", data=pd.DataFrame({"absr": np.abs(m2.resid), "fitted": m2.fittedvalues})).fit()
sig = np.clip(aux.fittedvalues, 1e-3, None)
mw = smf.wls(F2, data=train, weights=1 / sig ** 2).fit()
mwr = smf.wls(F2.replace("log_sqft * division", "log_sqft + division"), data=train, weights=1 / sig ** 2).fit()
fw, pw, _ = mw.compare_f_test(mwr)
from statsmodels.stats.diagnostic import het_breuschpagan
bpw = het_breuschpagan(mw.wresid, mw.model.exog)
out["final_wls"] = {"interaction_F": fw, "interaction_p": pw, "BP_p_weighted_resid": float(bpw[1]),
                    "pacific_minus_SA": float(mw.params["log_sqft:division[T.Pacific]"]),
                    "ENC_minus_SA": float(mw.params["log_sqft:division[T.ENCentral]"])}
# (f) influential points in final model
cd = m2.get_influence().cooks_distance[0]
out["final_influence"] = {"max_cook": float(cd.max()), "n_cook_gt_4n": int((cd > 4 / len(cd)).sum()), "n_cook_gt_0.5": int((cd > 0.5).sum())}
save_json(out, f"{BASE}/results/soc_fullflow.json")

print("RAW", out["raw_shape"], prof)
print("P1", {k: round(v, 4) if isinstance(v, float) else v for k, v in d1.items()})
print("BC", out["part1"]["boxcox"])
print("transform cands", cands)
print("sqft^2 test", out["part2_sqft_squared_test"])
print("BIC hist", hist_bic); print("AIC kept", kept_aic)
print("FINAL", F2); print({k: v for k, v in d2.items() if k != "icc"}, d2["icc"])
print("GVIF", out["final"]["gvif_top"][:2], out["final"]["gvif_main_effects_top"][:2])
print("int", out["final"]["interaction_partialF"], out["final"]["interaction_wald_hc3"]["p"], "dR2X", out["final"]["dR2_X_and_XxG"])
for lev, v in sl2.items():
    print(f"  {lev:14s} n={v['n_train']} elasticity={v['est']:.3f} CI=({v['ci_low']:.3f},{v['ci_high']:.3f}) pHC3={v['p_hc3']:.1e} +10% sqft -> {v['pct_per_10pct_more_sqft']:.2f}% price; P10-90={v['p10_p90_within_group']['delta_y']:.3f} ({v['p10_p90_within_group']['delta_y_in_sd']:.2f} SD)")
print("WLS", out["final_wls"]); print("infl", out["final_influence"])

# ---------------- course-style checks (Part 1 and final) ----------------
from course_diag import course_checks
focal = ["sqft100"] + [t for t in m1.params.index if t.startswith("sqft100:division")]
out["part1_course_checks"] = course_checks(m1, train, "price_k", ["sqft100", "lot_k", "sale_month"], cat, "soc_part1", f"{BASE}/figures",
                                           ylab="Sale price ($1000s)", focal_terms=focal)
cat_final = ["division"] + [c.replace("C(", "").replace(")", "") for c in kept_bic if c.startswith("C(")]
focal2 = ["log_sqft"] + [t for t in m2.params.index if t.startswith("log_sqft:division")]
out["final_course_checks"] = course_checks(m2, train, "log_price", ["log_sqft", "lot_k"], cat_final, "soc_final", f"{BASE}/figures",
                                           ylab="log sale price", focal_terms=focal2)
save_json(out, f"{BASE}/results/soc_fullflow.json")
for k in ["part1_course_checks", "final_course_checks"]:
    cc = out[k]
    print(k, "cond1 r=", round(cc["cond1_corr_y_fitted"], 3), "lowess dev/sd=", round(cc["cond1_lowess_max_dev_from_identity"], 3), "cond2", cc["cond2_pairs"])
    print("   resid vs numeric", cc["resid_vs_numeric"])
    print("   resid by cat (sd ratio, levene p)", {a: (round(b["max_sd_ratio"], 2), float("%.1e" % b["levene_p"])) for a, b in cc["resid_by_categorical"].items()})
    print("   lev", cc["leverage"], "std", cc["std_resid"], "cook", cc["cooks"], "dffits", cc["dffits"])
    print("   dfbetas", cc["dfbetas"])

# ---------------- confounding checks on the FINAL (log-log) specification ----------------
alts = {"division_x_lot": " + division:lot_k", "logsqft_x_stories": " + log_sqft:C(stories)", "logsqft_x_garage": " + log_sqft:C(garage)",
        "logsqft_x_fullbath": " + log_sqft:C(fullbath)", "logsqft_x_stage": " + log_sqft:C(stage) + C(stage)",
        "division_x_fullbath": " + division:C(fullbath)", "logsqft_x_lot": " + log_sqft:lot_k",
        "all": " + division:lot_k + log_sqft:C(stories) + log_sqft:C(garage) + log_sqft:C(fullbath) + log_sqft:C(stage) + C(stage) + log_sqft:lot_k"}
rob = {}
for k, extra in alts.items():
    ma, ma3 = fit(F2 + extra, train); mr, _ = fit((F2 + extra).replace("log_sqft * division", "log_sqft + division"), train)
    rob[k] = {"F_p": partial_f(ma, mr)["p"], "HC3_p": wald_hc3(ma, ma3, ["log_sqft:division"])["p"],
              "pacific_minus_SA": coef_table(ma, ma3, ["log_sqft:division[T.Pacific]"])[0],
              "ENC_minus_SA": coef_table(ma, ma3, ["log_sqft:division[T.ENCentral]"])[0]}
sub = train[train.slpr_flag == 0]
ma, ma3 = fit(F2, sub); mr, _ = fit(F2.replace("log_sqft * division", "log_sqft + division"), sub)
rob["excl_top_bottom_coded"] = {"n": len(sub), "F_p": partial_f(ma, mr)["p"], "HC3_p": wald_hc3(ma, ma3, ["log_sqft:division"])["p"]}
out["final_confounding"] = rob
# ---------------- 2024 replication of the FINAL specification ----------------
D = pd.read_csv(f"{BASE}/data/soc/soc24.csv")
s24 = D[(D.CAT == 1) & (D.SALE >= 202401) & (D.SALE <= 202412) & (D.SLPR > 0) & (D.DET == 1) & (D.CON == 2) & (D.SQFS > 0) & (D.AREA > 0)]
need = {"STOR": [1, 2, 3], "BEDR": [2, 3, 4, 5], "FULB": [1, 2, 3, 4], "HAFB": [0, 1, 2], "GAR": [1, 2, 3, 4], "BASE": [1, 2, 3, 4],
        "FPLS": [0, 1, 2], "ASSOC": [1, 2], "AGER": [1, 2], "WAL1": [1, 2, 4, 5, 6, 7, 8, 9], "FUEL": [1, 2, 3, 4, 5], "SEWER": [1, 2, 3]}
for c_, ok in need.items():
    s24 = s24[s24[c_].isin(ok)]
divn = {1: "NewEngland", 2: "MidAtlantic", 3: "ENCentral", 4: "WNCentral", 5: "SouthAtlantic", 6: "ESCentral", 7: "WSCentral", 8: "Mountain", 9: "Pacific"}
r24 = pd.DataFrame({"log_price": np.log(s24.SLPR.values / 1000), "log_sqft": np.log(s24.SQFS.values), "lot_k": s24.AREA.values / 1000,
    "division": pd.Categorical(s24.DIV.map(divn).values, categories=divs),
    "stories": s24.STOR.map({1: "1", 2: "2", 3: "3plus"}).values, "bedrooms": s24.BEDR.map({2: "2orless", 3: "3", 4: "4", 5: "5plus"}).values,
    "fullbath": s24.FULB.map({1: "1orless", 2: "2", 3: "3", 4: "4plus"}).values, "halfbath": s24.HAFB.map({0: "0", 1: "1", 2: "2plus"}).values,
    "garage": s24.GAR.map({1: "1car", 2: "2car", 3: "3plus", 4: "other"}).values, "foundation": s24.BASE.map({1: "basement", 2: "crawl", 3: "slab", 4: "other"}).values,
    "fireplace": s24.FPLS.map({0: "0", 1: "1", 2: "2plus"}).values, "hoa": s24.ASSOC.map({1: "yes", 2: "no"}).values,
    "age_restricted": s24.AGER.map({1: "yes", 2: "no"}).values,
    "wall": s24.WAL1.map({1: "wood", 2: "brick", 4: "stucco", 5: "vinyl", 6: "other", 7: "stone", 8: "fibercement", 9: "other"}).values,
    "heat_fuel": s24.FUEL.map({1: "electric", 2: "gas", 3: "propane", 4: "other", 5: "other"}).values,
    "sewer": s24.SEWER.map({1: "public", 2: "septic", 3: "septic"}).values, "sale_month": (s24.SALE % 100).values})
ma, ma3 = fit(F2, r24); mr, _ = fit(F2.replace("log_sqft * division", "log_sqft + division"), r24)
sl24 = {}
for lev in divs:
    w = {"log_sqft": 1.0}
    if lev != "SouthAtlantic":
        w[f"log_sqft:division[T.{lev}]"] = 1.0
    sl24[lev] = lincomb(ma, ma3, w)
out["replication_2024_final_spec"] = {"n": len(r24), "R2": ma.rsquared, "F_p": partial_f(ma, mr)["p"],
                                      "HC3_p": wald_hc3(ma, ma3, ["log_sqft:division"])["p"], "slopes": sl24}
save_json(out, f"{BASE}/results/soc_fullflow.json")
for k, v in rob.items():
    if "pacific_minus_SA" in v:
        print(f"ROB {k:20s} F_p={v['F_p']:.1e} HC3_p={v['HC3_p']:.1e} Pac-SA={v['pacific_minus_SA']['est']:.3f}({v['pacific_minus_SA']['p_hc3']:.1e}) ENC-SA={v['ENC_minus_SA']['est']:.3f}({v['ENC_minus_SA']['p_hc3']:.1e})")
    else:
        print("ROB", k, v)
rr = out["replication_2024_final_spec"]
print("REPL2024 final spec n", rr["n"], "R2", round(rr["R2"], 3), "F_p", rr["F_p"], "HC3_p", rr["HC3_p"])
for lev, v in sl24.items():
    print(f"  {lev:14s} elasticity={v['est']:.3f} CI=({v['ci_low']:.3f},{v['ci_high']:.3f}) pHC3={v['p_hc3']:.1e}")
