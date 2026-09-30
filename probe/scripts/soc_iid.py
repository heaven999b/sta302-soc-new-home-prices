"""SOC: IID-related checks on the Part 2 final specification (training split only).
1) cluster-robust SE by Census division (only 9 clusters -> unreliable; reported with that caveat)
2) survey-weighted (SOC WEIGHT) estimation of the final specification
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
train["log_price"] = np.log(train.price_k)
train["log_sqft"] = np.log(train.sqft100 * 100)
ctrl = "lot_k + C(stories) + C(bedrooms) + C(fullbath) + C(halfbath) + C(garage) + C(foundation) + C(fireplace) + C(wall) + C(heat_fuel)"
F2 = f"log_price ~ log_sqft * division + {ctrl}"
F2r = f"log_price ~ log_sqft + division + {ctrl}"
out = {}
m = smf.ols(F2, data=train).fit()
g = train.division.cat.codes.values
mc = smf.ols(F2, data=train).fit(cov_type="cluster", cov_kwds={"groups": g})
terms = [t for t in m.params.index if t.startswith("log_sqft:division")]
out["cluster_division_individual"] = {t: {"est": float(mc.params[t]), "se_cluster": float(mc.bse[t]), "p_cluster": float(mc.pvalues[t]),
                                          "se_ols": float(m.bse[t]), "p_ols": float(m.pvalues[t])} for t in terms}
R = np.zeros((len(terms), len(m.params)))
for i, t in enumerate(terms):
    R[i, list(m.params.index).index(t)] = 1
try:
    w = mc.wald_test(R, scalar=True)
    out["cluster_division_joint"] = {"stat": float(w.statistic), "p": float(w.pvalue), "note": "8 restrictions with only 9 clusters: covariance rank <= 8, test unreliable"}
except Exception as e:
    out["cluster_division_joint"] = {"error": repr(e)}
# a 1-df contrast that is robust to the cluster problem: Midwest (ENC+WNC) vs rest of divisions, cluster by division
train["midwest"] = train.division.isin(["ENCentral", "WNCentral"]).map({True: "Midwest", False: "Other"})
Fm = f"log_price ~ log_sqft * C(midwest, Treatment('Other')) + division + {ctrl}"
mm = smf.ols(Fm, data=train).fit(); mmc = smf.ols(Fm, data=train).fit(cov_type="cluster", cov_kwds={"groups": g})
mm3 = mm.get_robustcov_results(cov_type="HC3")
t = [x for x in mm.params.index if x.startswith("log_sqft:C(midwest")][0]
j = list(mm.params.index).index(t)
out["midwest_contrast"] = {"term": t, "est": float(mm.params[t]), "p_ols": float(mm.pvalues[t]), "p_hc3": float(mm3.pvalues[j]),
                           "p_cluster_division": float(mmc.pvalues[t]), "se_cluster": float(mmc.bse[t])}
# survey weights
wts = pd.read_csv(f"{BASE}/data/soc/soc25.csv", usecols=["ID", "WEIGHT"]).set_index("ID").WEIGHT
train["w"] = train.id.map(wts).values
mw = smf.wls(F2, data=train, weights=train.w).fit(); mwr = smf.wls(F2r, data=train, weights=train.w).fit()
f_, p_, _ = mw.compare_f_test(mwr)
mw3 = mw.get_robustcov_results(cov_type="HC3")
names = list(mw.params.index)
Rw = np.zeros((len(terms), len(names)))
for i, tt in enumerate(terms):
    Rw[i, names.index(tt)] = 1
ww = mw3.wald_test(Rw, scalar=True, use_f=True)
out["weighted_final"] = {"F": float(f_), "p": float(p_), "HC3_p": float(ww.pvalue),
                         "ENC_minus_SA": float(mw.params["log_sqft:division[T.ENCentral]"]),
                         "WNC_minus_SA": float(mw.params["log_sqft:division[T.WNCentral]"]),
                         "Pacific_minus_SA": float(mw.params["log_sqft:division[T.Pacific]"])}
save_json(out, f"{BASE}/results/soc_iid.json")
for k, v in out["cluster_division_individual"].items():
    print(f"{k:34s} est={v['est']:.3f} p_ols={v['p_ols']:.1e} p_cluster={v['p_cluster']:.1e}")
print("joint", out["cluster_division_joint"])
print("midwest contrast", out["midwest_contrast"])
print("weighted", out["weighted_final"])
