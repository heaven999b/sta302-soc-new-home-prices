"""Extra checks for SOC probe (training split of 2025 only + an independent 2024 replication sample).
1) log-scale and Box-Cox(-0.5) versions with the same alternative interactions
2) survey-weighted (WLS with WEIGHT) sensitivity
3) replication on houses sold in 2024 (soc24 file; different houses, never touches the 2025 test set)
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from utils import *
import statsmodels.formula.api as smf

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(f"{BASE}/data/soc/soc_analysis.csv")
divs = ["SouthAtlantic", "NewEngland", "MidAtlantic", "ENCentral", "WNCentral", "ESCentral", "WSCentral", "Mountain", "Pacific"]
df["division"] = pd.Categorical(df.division, categories=divs)
train, test = split70(df)
controls = ("lot_k + C(stories) + C(bedrooms) + C(fullbath) + C(halfbath) + C(garage) + C(foundation)"
            " + C(fireplace) + C(hoa) + C(age_restricted) + C(wall) + C(heat_fuel) + C(sewer) + C(stage) + sale_month")
train["log_price"] = np.log(train.price_k)
train["bc_m05"] = -2 * (train.price_k ** -0.5 - 1)     # Box-Cox lambda = -0.5 (monotone increasing)
alts = {"none": "", "division_x_lot": " + division:lot_k", "sqft_x_stories": " + sqft100:C(stories)",
        "sqft_x_garage": " + sqft100:C(garage)", "sqft_x_fullbath": " + sqft100:C(fullbath)", "sqft_x_stage": " + sqft100:C(stage)",
        "division_x_fullbath": " + division:C(fullbath)",
        "all": " + division:lot_k + sqft100:C(stories) + sqft100:C(garage) + sqft100:C(fullbath) + sqft100:C(stage)"}
out = {}
for yv in ["log_price", "bc_m05"]:
    out[yv] = {}
    for k, extra in alts.items():
        mf, mf3 = fit(f"{yv} ~ sqft100 * division + {controls}{extra}", train)
        mr, _ = fit(f"{yv} ~ sqft100 + division + {controls}{extra}", train)
        pf = partial_f(mf, mr); w = wald_hc3(mf, mf3, ["sqft100:division"])
        out[yv][k] = {"R2": mf.rsquared, "F_p": pf["p"], "HC3_p": w["p"], "dR2_int": pf["delta_R2"],
                      "pacific_minus_SA": coef_table(mf, mf3, ["sqft100:division[T.Pacific]"])[0],
                      "ENC_minus_SA": coef_table(mf, mf3, ["sqft100:division[T.ENCentral]"])[0]}
        if k == "none":
            d = diagnostics(mf)
            out[yv]["diag"] = {a: d[a] for a in ["R2", "adjR2", "resid_skew", "resid_exkurt", "BP_p", "max_cooks"]}
# survey-weighted sensitivity (raw scale)
w = pd.read_csv(f"{BASE}/data/soc/soc25.csv", usecols=["ID", "WEIGHT"]).set_index("ID").WEIGHT
train["w"] = train.id.map(w).values
mw = smf.wls(f"price_k ~ sqft100 * division + {controls}", data=train, weights=train.w).fit()
mwr = smf.wls(f"price_k ~ sqft100 + division + {controls}", data=train, weights=train.w).fit()
f_, p_, _ = mw.compare_f_test(mwr)
out["weighted_raw"] = {"F": f_, "p": p_, "pacific_minus_SA": float(mw.params["sqft100:division[T.Pacific]"]),
                       "ENC_minus_SA": float(mw.params["sqft100:division[T.ENCentral]"])}

# ---------- 2024 replication (independent houses: contract signed in 2024) ----------
D = pd.read_csv(f"{BASE}/data/soc/soc24.csv")
s = D[(D.CAT == 1) & (D.SALE >= 202401) & (D.SALE <= 202412) & (D.SLPR > 0) & (D.DET == 1) & (D.CON == 2) & (D.SQFS > 0) & (D.AREA > 0)]
need = {"STOR": [1, 2, 3], "BEDR": [2, 3, 4, 5], "FULB": [1, 2, 3, 4], "HAFB": [0, 1, 2], "GAR": [1, 2, 3, 4],
        "BASE": [1, 2, 3, 4], "FPLS": [0, 1, 2], "ASSOC": [1, 2], "AGER": [1, 2], "WAL1": [1, 2, 4, 5, 6, 7, 8, 9],
        "FUEL": [1, 2, 3, 4, 5], "SEWER": [1, 2, 3]}
for c, ok in need.items():
    s = s[s[c].isin(ok)]
divn = {1: "NewEngland", 2: "MidAtlantic", 3: "ENCentral", 4: "WNCentral", 5: "SouthAtlantic", 6: "ESCentral", 7: "WSCentral", 8: "Mountain", 9: "Pacific"}
sale_m = s.SALE.values // 100 * 12 + s.SALE.values % 100
strt_m = np.where(s.STRT.values > 0, s.STRT.values // 100 * 12 + s.STRT.values % 100, 10 ** 9)
comp_m = np.where(s.COMP.values > 0, s.COMP.values // 100 * 12 + s.COMP.values % 100, 10 ** 9)
r = pd.DataFrame({
    "price_k": s.SLPR.values / 1000, "sqft100": s.SQFS.values / 100, "lot_k": s.AREA.values / 1000,
    "division": pd.Categorical(s.DIV.map(divn).values, categories=divs),
    "stories": s.STOR.astype(str).values, "bedrooms": s.BEDR.astype(str).values, "fullbath": s.FULB.astype(str).values,
    "halfbath": s.HAFB.astype(str).values, "garage": s.GAR.astype(str).values, "foundation": s.BASE.astype(str).values,
    "fireplace": s.FPLS.astype(str).values, "hoa": s.ASSOC.astype(str).values, "age_restricted": s.AGER.astype(str).values,
    "wall": s.WAL1.replace({6: 9}).astype(str).values, "heat_fuel": s.FUEL.replace({5: 4}).astype(str).values,
    "sewer": s.SEWER.replace({3: 2}).astype(str).values, "sale_month": (s.SALE % 100).values,
    "stage": np.where(sale_m < strt_m, "not_started", np.where(sale_m < comp_m, "under_constr", "completed")),
})
mf, mf3 = fit(f"price_k ~ sqft100 * division + {controls}", r)
mr, _ = fit(f"price_k ~ sqft100 + division + {controls}", r)
mx, _ = fit(f"price_k ~ division + {controls}", r)
sl = {}
for lev in divs:
    wts = {"sqft100": 1.0}
    if lev != "SouthAtlantic":
        wts[f"sqft100:division[T.{lev}]"] = 1.0
    sl[lev] = lincomb(mf, mf3, wts)
r["log_price"] = np.log(r.price_k)
ml, ml3 = fit(f"log_price ~ sqft100 * division + {controls}", r)
mlr, _ = fit(f"log_price ~ sqft100 + division + {controls}", r)
out["replication_2024"] = {"n": len(r), "R2": mf.rsquared, "adjR2": mf.rsquared_adj,
                           "interaction": partial_f(mf, mr), "interaction_hc3": wald_hc3(mf, mf3, ["sqft100:division"]),
                           "dR2_X_and_XxG": partial_f(mf, mx)["delta_R2"], "slopes": sl,
                           "log_R2": ml.rsquared, "log_interaction": partial_f(ml, mlr),
                           "log_interaction_hc3": wald_hc3(ml, ml3, ["sqft100:division"])}
save_json(out, f"{BASE}/results/soc_extra.json")
for yv in ["log_price", "bc_m05"]:
    print(yv, out[yv]["diag"])
    for k, v in out[yv].items():
        if k == "diag":
            continue
        print(f"  {k:20s} R2={v['R2']:.3f} F_p={v['F_p']:.1e} HC3_p={v['HC3_p']:.1e} dR2int={v['dR2_int']:.4f} Pac-SA={v['pacific_minus_SA']['est']:.4f}(pHC3={v['pacific_minus_SA']['p_hc3']:.1e}) ENC-SA={v['ENC_minus_SA']['est']:.4f}(pHC3={v['ENC_minus_SA']['p_hc3']:.1e})")
print("weighted", out["weighted_raw"])
rp = out["replication_2024"]
print("REPL 2024 n", rp["n"], "R2", round(rp["R2"], 3), "int", rp["interaction"], "hc3 p", rp["interaction_hc3"]["p"], "dR2X", rp["dR2_X_and_XxG"])
print("  log R2", rp["log_R2"], "log int p", rp["log_interaction"]["p"], "hc3", rp["log_interaction_hc3"]["p"])
for lev, v in sl.items():
    print(f"  {lev:14s} slope={v['est']:.2f} CI=({v['ci_low']:.2f},{v['ci_high']:.2f}) pHC3={v['p_hc3']:.1e}")
