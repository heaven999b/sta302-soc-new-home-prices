"""Probe 1: Census Survey of Construction (SOC) 2025 microdata.
Question: does the marginal sale price of new-home floor area differ across Census divisions?
All fitting/diagnostics on the 70% training split (seed 302) only.
"""
import sys, os
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from utils import *

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = pd.read_csv(f"{BASE}/data/soc/soc25.csv")
flow = [("raw 2025 SOC records", len(D))]
s = D[D.CAT == 1]; flow.append(("CAT=1 built for sale", len(s)))
s = s[(s.SALE >= 202501) & (s.SALE <= 202512)]; flow.append(("sold (contract signed) in 2025", len(s)))
s = s[s.SLPR > 0]; flow.append(("sales price reported", len(s)))
s = s[(s.DET == 1) & (s.CON == 2)]; flow.append(("detached, not part of condominium project", len(s)))
s = s[(s.SQFS > 0) & (s.AREA > 0)]; flow.append(("floor area and lot size reported", len(s)))
need = {"STOR": [1, 2, 3], "BEDR": [2, 3, 4, 5], "FULB": [1, 2, 3, 4], "HAFB": [0, 1, 2],
        "GAR": [1, 2, 3, 4], "BASE": [1, 2, 3, 4], "FPLS": [0, 1, 2], "ASSOC": [1, 2],
        "AGER": [1, 2], "WAL1": [1, 2, 4, 5, 6, 7, 8, 9], "FUEL": [1, 2, 3, 4, 5], "SEWER": [1, 2, 3]}
for c, ok in need.items():
    s = s[s[c].isin(ok)]
flow.append(("no 'not reported' codes in categorical predictors", len(s)))

divn = {1: "NewEngland", 2: "MidAtlantic", 3: "ENCentral", 4: "WNCentral", 5: "SouthAtlantic",
        6: "ESCentral", 7: "WSCentral", 8: "Mountain", 9: "Pacific"}
df = pd.DataFrame({
    "id": s.ID.values,
    "price_k": s.SLPR.values / 1000,
    "sqft100": s.SQFS.values / 100,
    "lot_k": s.AREA.values / 1000,
    "division": pd.Categorical(s.DIV.map(divn).values, categories=["SouthAtlantic"] + [v for k, v in divn.items() if k != 5]),
    "stories": s.STOR.map({1: "1", 2: "2", 3: "3plus"}).values,
    "bedrooms": s.BEDR.map({2: "2orless", 3: "3", 4: "4", 5: "5plus"}).values,
    "fullbath": s.FULB.map({1: "1orless", 2: "2", 3: "3", 4: "4plus"}).values,
    "halfbath": s.HAFB.map({0: "0", 1: "1", 2: "2plus"}).values,
    "garage": s.GAR.map({1: "1car", 2: "2car", 3: "3plus", 4: "other"}).values,
    "foundation": s.BASE.map({1: "basement", 2: "crawl", 3: "slab", 4: "other"}).values,
    "fireplace": s.FPLS.map({0: "0", 1: "1", 2: "2plus"}).values,
    "hoa": s.ASSOC.map({1: "yes", 2: "no"}).values,
    "age_restricted": s.AGER.map({1: "yes", 2: "no"}).values,
    "wall": s.WAL1.map({1: "wood", 2: "brick", 4: "stucco", 5: "vinyl", 6: "other", 7: "stone", 8: "fibercement", 9: "other"}).values,
    "heat_fuel": s.FUEL.map({1: "electric", 2: "gas", 3: "propane", 4: "other", 5: "other"}).values,
    "sewer": s.SEWER.map({1: "public", 2: "septic", 3: "septic"}).values,
    "sale_month": (s.SALE % 100).values,
    "slpr_flag": s.SLPR_F.values,
})
# stage of construction at contract signing (derived from dates, not from price)
sale_m = s.SALE.values // 100 * 12 + s.SALE.values % 100
strt_m = np.where(s.STRT.values > 0, s.STRT.values // 100 * 12 + s.STRT.values % 100, 10 ** 9)
comp_m = np.where(s.COMP.values > 0, s.COMP.values // 100 * 12 + s.COMP.values % 100, 10 ** 9)
df["stage"] = np.where(sale_m < strt_m, "not_started", np.where(sale_m < comp_m, "under_constr", "completed"))
df["region4"] = s.DIV.map({1: "Northeast", 2: "Northeast", 3: "Midwest", 4: "Midwest", 5: "South", 6: "South",
                           7: "South", 8: "West", 9: "West"}).values
df = df.dropna().reset_index(drop=True)
flow.append(("final analysis sample", len(df)))
df.to_csv(f"{BASE}/data/soc/soc_analysis.csv", index=False)

train, test = split70(df)
test[["id"]].to_csv(f"{BASE}/data/soc/soc_test_ids.csv", index=False)  # ids only; never analysed here
print("flow", flow, "train", len(train), "test", len(test))

controls = ("lot_k + C(stories) + C(bedrooms) + C(fullbath) + C(halfbath) + C(garage) + C(foundation)"
            " + C(fireplace) + C(hoa) + C(age_restricted) + C(wall) + C(heat_fuel) + C(sewer) + C(stage) + sale_month")
F_FULL = "price_k ~ sqft100 * division + " + controls
F_NOINT = "price_k ~ sqft100 + division + " + controls
F_NOX = "price_k ~ division + " + controls

res = {"flow": flow, "n_train": len(train), "n_test": len(test)}
y = train.price_k
res["Y_train"] = {"mean": y.mean(), "sd": y.std(), "median": y.median(), "min": y.min(), "max": y.max(),
                  "skew": float(stats.skew(y)), "exkurt": float(stats.kurtosis(y)),
                  "share_topbottom_coded": float(train.slpr_flag.mean())}
res["X_train"] = {"sqft100_p10_p50_p90": np.percentile(train.sqft100, [10, 50, 90]).tolist(),
                  "division_counts": train.division.value_counts().to_dict()}

m, m3 = fit(F_FULL, train)
m0, _ = fit(F_NOINT, train)
mx, _ = fit(F_NOX, train)
res["model_formula"] = F_FULL
res["diag_raw"] = diagnostics(m, clusters={"division": train.division.astype(str), "region4": train.region4})
# ICC by division in a model WITHOUT division terms (how much clustering division absorbs)
mnd, _ = fit("price_k ~ sqft100 + " + controls, train)
res["icc_division_if_division_omitted"] = icc_oneway(mnd.resid, train.division.astype(str))
res["gvif_full"] = gvif(m)[:6]
res["gvif_main_effects"] = gvif(m0)[:6]
res["boxcox_raw"] = boxcox_lambda(m, train.price_k)
res["interaction_partialF"] = partial_f(m, m0)
res["interaction_wald_hc3"] = wald_hc3(m, m3, ["sqft100:division"])
res["dR2_X_and_XxG"] = partial_f(m, mx)
terms = [t for t in m.params.index if t.startswith("sqft100")]
res["coefs_raw"] = coef_table(m, m3, terms + ["lot_k"])
slopes = {}
ysd = y.std()
for lev in train.division.cat.categories:
    w = {"sqft100": 1.0}
    if lev != "SouthAtlantic":
        w[f"sqft100:division[T.{lev}]"] = 1.0
    lc = lincomb(m, m3, w)
    xs = train.sqft100[train.division == lev]
    lc["n_train"] = int(len(xs))
    lc["p10_p90_within_group"] = pct_effect(lc["est"], xs, ysd)
    lc["p10_p90_overall_x"] = pct_effect(lc["est"], train.sqft100, ysd)
    slopes[lev] = lc
res["slopes_raw_by_division"] = slopes
resid_plots(m, f"{BASE}/figures/soc_raw_resid.png", "SOC 2025 (train): raw price_k model")

# ---------- log version (Part 2 preview) ----------
train["log_price"] = np.log(train.price_k)
ml, ml3 = fit(F_FULL.replace("price_k", "log_price"), train)
ml0, _ = fit(F_NOINT.replace("price_k", "log_price"), train)
mlx, _ = fit(F_NOX.replace("price_k", "log_price"), train)
res["diag_log"] = diagnostics(ml, clusters={"division": train.division.astype(str)})
res["interaction_partialF_log"] = partial_f(ml, ml0)
res["interaction_wald_hc3_log"] = wald_hc3(ml, ml3, ["sqft100:division"])
res["dR2_X_and_XxG_log"] = partial_f(ml, mlx)
sl_log = {}
for lev in train.division.cat.categories:
    w = {"sqft100": 1.0}
    if lev != "SouthAtlantic":
        w[f"sqft100:division[T.{lev}]"] = 1.0
    sl_log[lev] = lincomb(ml, ml3, w)
res["slopes_log_by_division"] = sl_log
resid_plots(ml, f"{BASE}/figures/soc_log_resid.png", "SOC 2025 (train): log price model", "Residual (log)")

# ---------- confounding / robustness (raw scale) ----------
rob = {}
alts = {
    "plus_division_x_lot": F_FULL + " + division:lot_k",
    "plus_sqft_x_stories": F_FULL + " + sqft100:C(stories)",
    "plus_sqft_x_garage": F_FULL + " + sqft100:C(garage)",
    "plus_sqft_x_fullbath": F_FULL + " + sqft100:C(fullbath)",
    "plus_sqft_x_stage": F_FULL + " + sqft100:C(stage)",
    "plus_division_x_fullbath": F_FULL + " + division:C(fullbath)",
    "plus_all_above": F_FULL + " + division:lot_k + sqft100:C(stories) + sqft100:C(garage) + sqft100:C(fullbath) + sqft100:C(stage)",
    "plus_sqft_squared": F_FULL + " + I(sqft100**2)",
}
for k, f in alts.items():
    ma, ma3 = fit(f, train)
    red = f.replace("sqft100 * division", "sqft100 + division")
    mr, _ = fit(red, train)
    rob[k] = {"partialF": partial_f(ma, mr), "wald_hc3": wald_hc3(ma, ma3, ["sqft100:division"]),
              "pacific_minus_SA": coef_table(ma, ma3, ["sqft100:division[T.Pacific]"]),
              "newengland_minus_SA": coef_table(ma, ma3, ["sqft100:division[T.NewEngland]"])}
# exclude top/bottom-coded prices
sub = train[train.slpr_flag == 0]
ma, ma3 = fit(F_FULL, sub); mr, _ = fit(F_NOINT, sub)
rob["exclude_topbottom_coded_prices"] = {"n": len(sub), "partialF": partial_f(ma, mr),
                                         "wald_hc3": wald_hc3(ma, ma3, ["sqft100:division"]), "R2": ma.rsquared}
# 4-region version
f4 = F_FULL.replace("division", "region4"); f4r = F_NOINT.replace("division", "region4")
ma, ma3 = fit(f4, train); mr, _ = fit(f4r, train)
rob["region4_instead_of_division"] = {"partialF": partial_f(ma, mr), "R2": ma.rsquared,
                                      "coefs": coef_table(ma, ma3, [t for t in ma.params.index if t.startswith("sqft100")])}
# subsample: homes without HOA / with HOA; completed vs not
for name, mask in {"hoa_yes": train.hoa == "yes", "hoa_no": train.hoa == "no",
                   "stage_not_completed": train.stage != "completed", "sqft_le_4000": train.sqft100 <= 40}.items():
    sb = train[mask]
    try:
        ma, ma3 = fit(F_FULL, sb); mr, _ = fit(F_NOINT, sb)
        rob[f"subsample_{name}"] = {"n": len(sb), "partialF": partial_f(ma, mr),
                                    "wald_hc3": wald_hc3(ma, ma3, ["sqft100:division"]),
                                    "pacific_minus_SA": coef_table(ma, ma3, ["sqft100:division[T.Pacific]"])}
    except Exception as e:
        rob[f"subsample_{name}"] = str(e)
res["robustness"] = rob

# interaction plot (training data, fitted lines at controls held at training means via partial residual style)
fig, ax = plt.subplots(figsize=(8, 5.2))
cols = plt.cm.tab10(np.arange(9))
grid = np.linspace(np.percentile(train.sqft100, 5), np.percentile(train.sqft100, 95), 50)
for i, lev in enumerate(train.division.cat.categories):
    sl = slopes[lev]["est"]
    g = train[train.division == lev]
    # intercept: group mean of price minus slope*group mean sqft
    icpt = g.price_k.mean() - sl * g.sqft100.mean()
    ax.plot(grid * 100, icpt + sl * grid, color=cols[i], lw=2, label=f"{lev} ({sl:.1f}k$/100sqft)")
ax.set_xlabel("Finished floor area (sq ft)"); ax.set_ylabel("Sale price ($1000s)")
ax.set_title("SOC 2025 train: adjusted slope of price on floor area by Census division")
ax.legend(fontsize=7.5, frameon=False, ncol=2)
fig.tight_layout(); fig.savefig(f"{BASE}/figures/soc_interaction.png", dpi=120); plt.close(fig)

save_json(res, f"{BASE}/results/soc.json")
print(json.dumps({k: res[k] for k in ["Y_train", "interaction_partialF", "interaction_wald_hc3", "dR2_X_and_XxG",
                                       "interaction_partialF_log", "interaction_wald_hc3_log", "dR2_X_and_XxG_log",
                                       "boxcox_raw", "icc_division_if_division_omitted"]}, indent=1, default=float))
for k in ["diag_raw", "diag_log"]:
    print(k, {a: b for a, b in res[k].items() if a != "icc"}, res[k]["icc"])
print("gvif main", res["gvif_main_effects"][:3]); print("gvif full", res["gvif_full"][:3])
for lev, v in slopes.items():
    print(f"RAW {lev:14s} n={v['n_train']:5d} slope={v['est']:7.2f} CI=({v['ci_low']:.2f},{v['ci_high']:.2f}) p={v['p']:.1e} pHC3={v['p_hc3']:.1e} P10-90 within: {v['p10_p90_within_group']['delta_y']:.0f}k = {v['p10_p90_within_group']['delta_y_in_sd']:.2f}SD")
for lev, v in sl_log.items():
    print(f"LOG {lev:14s} slope={v['est']:.4f} CI=({v['ci_low']:.4f},{v['ci_high']:.4f}) pHC3={v['p_hc3']:.1e}")
for k, v in rob.items():
    print("ROB", k, json.dumps(v, default=float)[:600])
