"""Shared helpers for the 2026-09-30 STA302 econ probes (written fresh for this folder).

Conventions
-----------
* split70(): 70/30 split with numpy default_rng(302); every model/diagnostic is fit on TRAIN only.
* All models use statsmodels formula OLS; HC3 robust SEs are computed alongside classical SEs.
"""
import json
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 302


def split70(df, seed=SEED):
    """Return (train, test) with a 70/30 random split (row order independent: sort by key first)."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(df))
    ntr = int(round(0.7 * len(df)))
    tr = df.iloc[np.sort(idx[:ntr])].copy()
    te = df.iloc[np.sort(idx[ntr:])].copy()
    return tr, te


def fit(formula, data):
    m = smf.ols(formula, data=data).fit()
    m_hc3 = m.get_robustcov_results(cov_type="HC3")
    return m, m_hc3


def coef_table(m, m_hc3, terms):
    names = list(m.params.index)
    ci = m.conf_int()
    out = []
    for t in terms:
        if t not in names:
            continue
        j = names.index(t)
        out.append({"term": t, "est": float(m.params[t]), "se": float(m.bse[t]),
                    "p": float(m.pvalues[t]), "ci_low": float(ci.loc[t, 0]), "ci_high": float(ci.loc[t, 1]),
                    "se_hc3": float(m_hc3.bse[j]), "p_hc3": float(m_hc3.pvalues[j])})
    return out


def lincomb(m, m_hc3, weights):
    """weights: dict term->weight. Returns estimate, SE, CI, p (classical) and HC3 SE/p."""
    names = list(m.params.index)
    L = np.zeros(len(names))
    for k, w in weights.items():
        L[names.index(k)] = w
    est = float(L @ m.params.values)
    se = float(np.sqrt(L @ m.cov_params().values @ L))
    se3 = float(np.sqrt(L @ np.asarray(m_hc3.cov_params()) @ L))
    df = m.df_resid
    tcrit = stats.t.ppf(0.975, df)
    return {"est": est, "se": se, "ci_low": est - tcrit * se, "ci_high": est + tcrit * se,
            "p": float(2 * stats.t.sf(abs(est / se), df)), "se_hc3": se3,
            "ci_low_hc3": est - tcrit * se3, "ci_high_hc3": est + tcrit * se3,
            "p_hc3": float(2 * stats.t.sf(abs(est / se3), df))}


def partial_f(m_full, m_red):
    """Classical nested F test (same data)."""
    f, p, ddf = m_full.compare_f_test(m_red)
    return {"F": float(f), "p": float(p), "df_num": int(ddf),
            "delta_R2": float(m_full.rsquared - m_red.rsquared)}


def wald_hc3(m, m_hc3, term_prefixes):
    """HC3 Wald test that all coefficients whose names contain any of term_prefixes are 0."""
    names = list(m.params.index)
    idx = [i for i, n in enumerate(names) if any(tp in n for tp in term_prefixes)]
    R = np.zeros((len(idx), len(names)))
    for r, i in enumerate(idx):
        R[r, i] = 1
    res = m_hc3.wald_test(R, scalar=True, use_f=True)
    return {"F": float(res.statistic), "p": float(res.pvalue), "df_num": len(idx),
            "terms": [names[i] for i in idx]}


def icc_oneway(resid, groups):
    d = pd.DataFrame({"r": np.asarray(resid, float), "g": np.asarray(groups)}).dropna()
    k = d["g"].nunique(); N = len(d)
    grp = d.groupby("g")["r"]
    ni = grp.size().values
    ssb = np.sum(ni * (grp.mean().values - d["r"].mean()) ** 2)
    ssw = np.sum((d["r"] - grp.transform("mean")) ** 2)
    msb = ssb / (k - 1); msw = ssw / (N - k)
    n0 = (N - np.sum(ni ** 2) / N) / (k - 1)
    icc = (msb - msw) / (msb + (n0 - 1) * msw)
    return {"icc": float(icc), "n_groups": int(k), "mean_size": float(N / k),
            "F": float(msb / msw), "p": float(stats.f.sf(msb / msw, k - 1, N - k))}


def gvif(m):
    """Fox & Monette GVIF^(1/(2df)) per formula term."""
    X = pd.DataFrame(m.model.exog, columns=m.model.exog_names).drop(columns=["Intercept"], errors="ignore")
    R = np.corrcoef(X.values, rowvar=False)
    ld = np.linalg.slogdet(R)[1]
    cols = list(X.columns)
    out = []
    for term, sl in m.model.data.design_info.term_name_slices.items():
        if term == "Intercept":
            continue
        tc = m.model.exog_names[sl]
        idx = [cols.index(c) for c in tc]
        rest = [i for i in range(len(cols)) if i not in idx]
        g = np.exp(np.linalg.slogdet(R[np.ix_(idx, idx)])[1] + np.linalg.slogdet(R[np.ix_(rest, rest)])[1] - ld)
        out.append({"term": term, "df": len(idx), "GVIF": float(g), "GVIF_adj": float(g ** (1 / (2 * len(idx))))})
    return sorted(out, key=lambda r: -r["GVIF_adj"])


def boxcox_lambda(m, y):
    """Profile log-likelihood for Box-Cox lambda using the model's design matrix."""
    y = np.asarray(y, float)
    if np.any(y <= 0):
        return None
    X = m.model.exog
    Q, _ = np.linalg.qr(X)  # projection onto column space, computed once
    n = len(y)
    lgm = np.mean(np.log(y))
    def ll(lam):
        if abs(lam) < 1e-9:
            z = np.exp(lgm) * np.log(y)
        else:
            z = (y ** lam - 1) / (lam * np.exp(lgm * (lam - 1)))
        rss = np.sum((z - Q @ (Q.T @ z)) ** 2)
        return -n / 2 * np.log(rss / n)
    grid = np.arange(-2, 2.0001, 0.05)
    lls = np.array([ll(l) for l in grid])
    b = grid[np.argmax(lls)]
    fine = np.arange(b - 0.06, b + 0.0601, 0.005)
    llf = np.array([ll(l) for l in fine])
    lam = fine[np.argmax(llf)]
    cut = llf.max() - stats.chi2.ppf(0.95, 1) / 2
    # widen CI search
    wide = np.arange(lam - 0.5, lam + 0.5001, 0.005)
    llw = np.array([ll(l) for l in wide])
    ci = wide[llw >= cut]
    return {"lambda": float(lam), "ci95": [float(ci.min()), float(ci.max())]}


def diagnostics(m, clusters=None):
    r = m.resid
    infl = m.get_influence()
    cd = infl.cooks_distance[0]
    h = infl.hat_matrix_diag
    bp = het_breuschpagan(r, m.model.exog)  # Koenker (studentized) version
    out = {"n": int(m.nobs), "k_params": int(m.df_model) + 1,
           "R2": float(m.rsquared), "adjR2": float(m.rsquared_adj),
           "resid_se": float(np.sqrt(m.scale)), "F": float(m.fvalue), "F_p": float(m.f_pvalue),
           "resid_skew": float(stats.skew(r)), "resid_exkurt": float(stats.kurtosis(r)),
           "BP_LM": float(bp[0]), "BP_p": float(bp[1]),
           "max_cooks": float(cd.max()), "n_cooks_gt_4n": int((cd > 4 / len(cd)).sum()),
           "n_cooks_gt_0.5": int((cd > 0.5).sum()),
           "max_leverage": float(h.max()), "n_lev_gt_2pn": int((h > 2 * (m.df_model + 1) / len(h)).sum())}
    if clusters:
        out["icc"] = {k: icc_oneway(r, v) for k, v in clusters.items()}
    return out


def pct_effect(slope, x, ysd):
    p10, p90 = np.percentile(x, [10, 90])
    d = slope * (p90 - p10)
    return {"x_p10": float(p10), "x_p90": float(p90), "delta_y": float(d), "delta_y_in_sd": float(d / ysd)}


def resid_plots(m, path, title, ylab="Residual"):
    f = m.fittedvalues; r = m.resid
    sr = m.get_influence().resid_studentized_internal
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
    ax[0].scatter(f, r, s=4, alpha=0.25, color="#33658a", edgecolor="none")
    ax[0].axhline(0, color="k", lw=0.8)
    lw = sm.nonparametric.lowess(r, f, frac=0.3)
    ax[0].plot(lw[:, 0], lw[:, 1], color="#d1495b", lw=2)
    ax[0].set_xlabel("Fitted value"); ax[0].set_ylabel(ylab); ax[0].set_title("Residuals vs fitted")
    (osm, osr), (sl, ic, _) = stats.probplot(sr, dist="norm")
    ax[1].scatter(osm, osr, s=4, alpha=0.35, color="#33658a", edgecolor="none")
    ax[1].plot(osm, sl * osm + ic, color="#d1495b", lw=1.5)
    ax[1].set_xlabel("Theoretical quantile"); ax[1].set_ylabel("Standardized residual"); ax[1].set_title("Normal QQ")
    ax[2].scatter(f, np.sqrt(np.abs(sr)), s=4, alpha=0.25, color="#33658a", edgecolor="none")
    lw2 = sm.nonparametric.lowess(np.sqrt(np.abs(sr)), f, frac=0.3)
    ax[2].plot(lw2[:, 0], lw2[:, 1], color="#d1495b", lw=2)
    ax[2].set_xlabel("Fitted value"); ax[2].set_ylabel("sqrt(|std. residual|)"); ax[2].set_title("Scale-location")
    fig.suptitle(title, fontsize=11); fig.tight_layout(); fig.savefig(path, dpi=120); plt.close(fig)


def save_json(obj, path):
    def conv(o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2, default=conv, ensure_ascii=False)


def run_probe(train, y, x, g, controls, label, figdir, alts=None, clusters=None, log_y=None,
              extra_terms=(), subsamples=None, ylab=None):
    """Generic numeric-X x categorical-G probe on the TRAINING set.
    y: response column; x: numeric focal predictor; g: categorical column (pd.Categorical, first level = baseline).
    controls: string of RHS control terms. alts: dict name -> extra RHS terms (alternative interactions).
    log_y: name of a log-response column to also fit (Part 2 preview), or None.
    """
    alts = alts or {}; clusters = clusters or {}; subsamples = subsamples or {}
    F_FULL = f"{y} ~ {x} * {g} + {controls}"
    F_NOINT = f"{y} ~ {x} + {g} + {controls}"
    F_NOX = f"{y} ~ {g} + {controls}"
    res = {"formula": F_FULL}
    yy = train[y]
    ysd = float(yy.std())
    res["Y_train"] = {"mean": float(yy.mean()), "sd": ysd, "median": float(yy.median()), "min": float(yy.min()),
                      "max": float(yy.max()), "skew": float(stats.skew(yy)), "exkurt": float(stats.kurtosis(yy))}
    res["X_train_pct"] = dict(zip(["p10", "p25", "p50", "p75", "p90"], np.percentile(train[x], [10, 25, 50, 75, 90]).tolist()))
    res["G_counts"] = train[g].value_counts().to_dict()
    m, m3 = fit(F_FULL, train); m0, _ = fit(F_NOINT, train); mx, _ = fit(F_NOX, train)
    res["diag"] = diagnostics(m, clusters=clusters)
    res["gvif_main"] = gvif(m0)[:5]
    res["gvif_full"] = gvif(m)[:5]
    res["boxcox"] = boxcox_lambda(m, yy) if (yy > 0).all() else "response has non-positive values"
    res["interaction_partialF"] = partial_f(m, m0)
    res["interaction_wald_hc3"] = wald_hc3(m, m3, [f"{x}:{g}"])
    res["dR2_X_and_XxG"] = partial_f(m, mx)
    res["coefs"] = coef_table(m, m3, [t for t in m.params.index if t.startswith(x)] + list(extra_terms))
    levels = list(train[g].cat.categories)
    slopes = {}
    for lev in levels:
        w = {x: 1.0}
        if lev != levels[0]:
            w[f"{x}:{g}[T.{lev}]"] = 1.0
        lc = lincomb(m, m3, w)
        xs = train.loc[train[g] == lev, x]
        lc["n_train"] = int(len(xs))
        lc["p10_p90_within_group"] = pct_effect(lc["est"], xs, ysd)
        lc["p10_p90_overall_x"] = pct_effect(lc["est"], train[x], ysd)
        slopes[str(lev)] = lc
    res["slopes"] = slopes
    resid_plots(m, f"{figdir}/{label}_raw_resid.png", f"{label} (train): Part 1 model on raw {y}")
    # interaction plot: fitted lines at group means
    fig, ax = plt.subplots(figsize=(7.5, 5))
    grid = np.linspace(np.percentile(train[x], 5), np.percentile(train[x], 95), 50)
    for i, lev in enumerate(levels):
        gd = train[train[g] == lev]
        sl = slopes[str(lev)]["est"]
        icpt = gd[y].mean() - sl * gd[x].mean()
        ax.plot(grid, icpt + sl * grid, lw=2, label=f"{lev}: slope {sl:.3g}")
    ax.set_xlabel(x); ax.set_ylabel(ylab or y); ax.legend(frameon=False, fontsize=8)
    ax.set_title(f"{label} (train): adjusted slope of {y} on {x} by {g}")
    fig.tight_layout(); fig.savefig(f"{figdir}/{label}_interaction.png", dpi=120); plt.close(fig)
    if log_y:
        ml, ml3 = fit(F_FULL.replace(f"{y} ~", f"{log_y} ~", 1), train)
        ml0, _ = fit(F_NOINT.replace(f"{y} ~", f"{log_y} ~", 1), train)
        mlx, _ = fit(F_NOX.replace(f"{y} ~", f"{log_y} ~", 1), train)
        res["log_diag"] = diagnostics(ml, clusters=clusters)
        res["log_interaction_partialF"] = partial_f(ml, ml0)
        res["log_interaction_wald_hc3"] = wald_hc3(ml, ml3, [f"{x}:{g}"])
        res["log_dR2_X_and_XxG"] = partial_f(ml, mlx)
        ls = {}
        for lev in levels:
            w = {x: 1.0}
            if lev != levels[0]:
                w[f"{x}:{g}[T.{lev}]"] = 1.0
            ls[str(lev)] = lincomb(ml, ml3, w)
        res["log_slopes"] = ls
        resid_plots(ml, f"{figdir}/{label}_log_resid.png", f"{label} (train): model on {log_y}", "Residual (log)")
    rob = {}
    for k, extra in alts.items():
        ma, ma3 = fit(F_FULL + " + " + extra, train); mr, _ = fit(F_NOINT + " + " + extra, train)
        rob[k] = {"partialF": partial_f(ma, mr), "wald_hc3": wald_hc3(ma, ma3, [f"{x}:{g}"]),
                  "coefs": coef_table(ma, ma3, [t for t in ma.params.index if t.startswith(f"{x}:{g}")])}
    for k, mask in subsamples.items():
        sb = train[mask]
        try:
            ma, ma3 = fit(F_FULL, sb); mr, _ = fit(F_NOINT, sb)
            rob[f"sub_{k}"] = {"n": int(len(sb)), "R2": float(ma.rsquared), "partialF": partial_f(ma, mr),
                               "wald_hc3": wald_hc3(ma, ma3, [f"{x}:{g}"]),
                               "coefs": coef_table(ma, ma3, [t for t in ma.params.index if t.startswith(f"{x}:{g}")])}
        except Exception as e:
            rob[f"sub_{k}"] = repr(e)
    res["robustness"] = rob
    return res, m


def summarize(res):
    d = res["diag"]
    lines = [f"R2={d['R2']:.3f} adjR2={d['adjR2']:.3f} n={d['n']} k={d['k_params']} sigma={d['resid_se']:.3g}",
             f"skew={d['resid_skew']:.2f} exkurt={d['resid_exkurt']:.1f} BP_p={d['BP_p']:.1e} maxCook={d['max_cooks']:.3f} maxLev={d['max_leverage']:.3f}",
             f"ICC={ {k: round(v['icc'], 4) for k, v in d.get('icc', {}).items()} }",
             f"boxcox={res['boxcox']}",
             f"GVIF main top={res['gvif_main'][0]}",
             f"interaction partialF={res['interaction_partialF']} HC3={ {k: v for k, v in res['interaction_wald_hc3'].items() if k != 'terms'} }",
             f"dR2(X + XxG)={res['dR2_X_and_XxG']['delta_R2']:.4f}"]
    for lev, v in res["slopes"].items():
        lines.append(f"  slope[{lev}] n={v['n_train']} est={v['est']:.4g} CI=({v['ci_low']:.4g},{v['ci_high']:.4g}) p={v['p']:.1e} pHC3={v['p_hc3']:.1e} "
                     f"P10->P90(within)={v['p10_p90_within_group']['delta_y']:.4g} ({v['p10_p90_within_group']['delta_y_in_sd']:.2f} SD)")
    if "log_diag" in res:
        ld = res["log_diag"]
        lines.append(f"LOG: R2={ld['R2']:.3f} skew={ld['resid_skew']:.2f} exkurt={ld['resid_exkurt']:.1f} ICC={ {k: round(v['icc'], 4) for k, v in ld.get('icc', {}).items()} } "
                     f"intF p={res['log_interaction_partialF']['p']:.1e} HC3 p={res['log_interaction_wald_hc3']['p']:.1e} dR2int={res['log_interaction_partialF']['delta_R2']:.4f} dR2X={res['log_dR2_X_and_XxG']['delta_R2']:.4f}")
        for lev, v in res["log_slopes"].items():
            lines.append(f"  logslope[{lev}] est={v['est']:.4g} CI=({v['ci_low']:.4g},{v['ci_high']:.4g}) pHC3={v['p_hc3']:.1e}")
    for k, v in res["robustness"].items():
        if isinstance(v, str):
            lines.append(f"ROB {k}: {v}"); continue
        cs = "; ".join(f"{c['term']}={c['est']:.4g}(p={c['p']:.1e},pHC3={c['p_hc3']:.1e})" for c in v["coefs"])
        lines.append(f"ROB {k}: n={v.get('n','')} F p={v['partialF']['p']:.1e} HC3 p={v['wald_hc3']['p']:.1e} | {cs}")
    return "\n".join(lines)


def backward_select(data, y, forced, candidates, criterion="BIC"):
    """Backward elimination over formula TERMS (a categorical counts as one term).
    forced: list of RHS terms always kept; candidates: removable RHS terms.
    At each step drop the candidate whose removal gives the lowest criterion, if it improves on the current model.
    Returns (kept_candidates, history) where history rows record the partial-F p-value of each dropped term."""
    cur = list(candidates)
    def f_of(terms):
        return f"{y} ~ " + " + ".join(forced + terms)
    m_cur = smf.ols(f_of(cur), data=data).fit()
    crit = lambda m: m.bic if criterion == "BIC" else m.aic
    hist = [{"step": 0, "dropped": None, criterion: float(crit(m_cur)), "R2": float(m_cur.rsquared), "adjR2": float(m_cur.rsquared_adj)}]
    step = 0
    while cur:
        best = None
        for t in cur:
            trial = [u for u in cur if u != t]
            m_t = smf.ols(f_of(trial), data=data).fit()
            if best is None or crit(m_t) < best[1]:
                best = (t, crit(m_t), m_t)
        if best[1] < crit(m_cur):
            f_, p_, dfd = m_cur.compare_f_test(best[2])
            step += 1
            cur = [u for u in cur if u != best[0]]
            hist.append({"step": step, "dropped": best[0], criterion: float(best[1]), "partialF_p_of_dropped": float(p_),
                         "df": int(dfd), "R2": float(best[2].rsquared), "adjR2": float(best[2].rsquared_adj)})
            m_cur = best[2]
        else:
            break
    return cur, hist


def describe_train(train, numeric, categorical):
    rows = []
    for v in numeric:
        x = train[v]
        rows.append({"var": v, "type": "numeric", "mean": float(x.mean()), "sd": float(x.std()), "min": float(x.min()),
                     "median": float(x.median()), "max": float(x.max()), "skew": float(stats.skew(x)), "n_missing": int(x.isna().sum())})
    for v in categorical:
        vc = train[v].astype(str).value_counts()
        rows.append({"var": v, "type": f"categorical ({len(vc)} levels)", "levels": "; ".join(f"{k}: {n}" for k, n in vc.items())})
    return rows


def grid_plots(m, path, title, xvar=None, data=None):
    """2x2 grid: residuals vs fitted, QQ, scale-location, residuals vs focal X (or Cook's D)."""
    f = m.fittedvalues; r = m.resid
    infl = m.get_influence()
    sr = infl.resid_studentized_internal
    fig, ax = plt.subplots(2, 2, figsize=(11, 8.5))
    a = ax[0, 0]; a.scatter(f, r, s=4, alpha=0.25, color="#33658a", edgecolor="none"); a.axhline(0, color="k", lw=0.8)
    lw = sm.nonparametric.lowess(r, f, frac=0.3); a.plot(lw[:, 0], lw[:, 1], color="#d1495b", lw=2)
    a.set_xlabel("Fitted value"); a.set_ylabel("Residual"); a.set_title("Residuals vs fitted")
    a = ax[0, 1]; (osm, osr), (sl, ic, _) = stats.probplot(sr, dist="norm")
    a.scatter(osm, osr, s=4, alpha=0.35, color="#33658a", edgecolor="none"); a.plot(osm, sl * osm + ic, color="#d1495b")
    a.set_xlabel("Theoretical quantile"); a.set_ylabel("Standardized residual"); a.set_title("Normal QQ")
    a = ax[1, 0]; a.scatter(f, np.sqrt(np.abs(sr)), s=4, alpha=0.25, color="#33658a", edgecolor="none")
    lw2 = sm.nonparametric.lowess(np.sqrt(np.abs(sr)), f, frac=0.3); a.plot(lw2[:, 0], lw2[:, 1], color="#d1495b", lw=2)
    a.set_xlabel("Fitted value"); a.set_ylabel("sqrt(|std. residual|)"); a.set_title("Scale-location")
    a = ax[1, 1]
    if xvar is not None and data is not None:
        xv = data.loc[r.index, xvar]
        a.scatter(xv, r, s=4, alpha=0.25, color="#33658a", edgecolor="none"); a.axhline(0, color="k", lw=0.8)
        lw3 = sm.nonparametric.lowess(r, xv, frac=0.3); a.plot(lw3[:, 0], lw3[:, 1], color="#d1495b", lw=2)
        a.set_xlabel(xvar); a.set_ylabel("Residual"); a.set_title(f"Residuals vs {xvar}")
    else:
        cd = infl.cooks_distance[0]; a.stem(np.arange(len(cd)), cd, markerfmt=" ", basefmt=" ")
        a.set_title("Cook's distance"); a.set_xlabel("Observation")
    fig.suptitle(title, fontsize=12); fig.tight_layout(); fig.savefig(path, dpi=115); plt.close(fig)
