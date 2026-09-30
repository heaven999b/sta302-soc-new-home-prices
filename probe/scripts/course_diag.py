"""STA302-style assumption checks and influence diagnostics (training set), figures laid out as grids.
Condition 1: Y vs fitted.  Condition 2: pairwise scatterplots of numeric predictors.
Residuals vs fitted / vs each numeric predictor / boxplots by each categorical predictor / QQ.
Influence: leverage (hat), standardized residuals, Cook's D, DFFITS, DFBETAS.
"""
import numpy as np, pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE = "#33658a"; RED = "#d1495b"


def _lowess(ax, x, y):
    try:
        lw = sm.nonparametric.lowess(y, x, frac=0.3)
        ax.plot(lw[:, 0], lw[:, 1], color=RED, lw=2)
    except Exception:
        pass


def course_checks(m, data, yname, numeric_preds, cat_preds, label, figdir, ylab=None, focal_terms=()):
    d = data.loc[m.resid.index]
    y = d[yname]; f = m.fittedvalues; r = m.resid
    infl = m.get_influence()
    sr = infl.resid_studentized_internal
    n = int(m.nobs); p = int(m.df_model + 1)
    out = {}
    # ---- Figure A: Condition 1 + Condition 2 ----
    k = len(numeric_preds)
    npan = 1 + max(1, k * (k - 1) // 2)
    ncol_a = min(3, npan); nrow_a = int(np.ceil(npan / ncol_a))
    fig, ax = plt.subplots(nrow_a, ncol_a, figsize=(4.8 * ncol_a, 4.0 * nrow_a))
    ax = np.atleast_1d(ax).ravel()
    for a_ in ax[npan:]:
        a_.axis("off")
    ax[0].scatter(f, y, s=4, alpha=0.25, color=BLUE, edgecolor="none")
    lo, hi = np.nanmin([f.min(), y.min()]), np.nanmax([f.max(), y.max()])
    ax[0].plot([lo, hi], [lo, hi], color="k", lw=0.8, ls="--"); _lowess(ax[0], f.values, y.values)
    ax[0].set_xlabel("Fitted value"); ax[0].set_ylabel(ylab or yname); ax[0].set_title("Condition 1: Y vs fitted")
    j = 1
    pairs = [(numeric_preds[a], numeric_preds[b]) for a in range(k) for b in range(a + 1, k)]
    for (a, b) in pairs:
        ax[j].scatter(d[a], d[b], s=4, alpha=0.25, color=BLUE, edgecolor="none"); _lowess(ax[j], d[a].values, d[b].values)
        ax[j].set_xlabel(a); ax[j].set_ylabel(b); ax[j].set_title(f"Condition 2: {b} vs {a}"); j += 1
    fig.tight_layout(); fig.savefig(f"{figdir}/{label}_conditions.png", dpi=110); plt.close(fig)
    # simple numeric summaries for conditions
    lwc = sm.nonparametric.lowess(y.values, f.values, frac=0.3)
    out["cond1_corr_y_fitted"] = float(np.corrcoef(y, f)[0, 1])
    out["cond1_lowess_max_dev_from_identity"] = float(np.max(np.abs(lwc[:, 1] - lwc[:, 0])) / y.std())
    pr = {}
    for (a, b) in pairs:
        pr[f"{a}~{b}"] = {"pearson": float(np.corrcoef(d[a], d[b])[0, 1]), "spearman": float(stats.spearmanr(d[a], d[b])[0])}
    out["cond2_pairs"] = pr
    # ---- Figure B: residual vs fitted, QQ, scale-location ----
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
    ax[0].scatter(f, r, s=4, alpha=0.25, color=BLUE, edgecolor="none"); ax[0].axhline(0, color="k", lw=0.8); _lowess(ax[0], f.values, r.values)
    ax[0].set_xlabel("Fitted value"); ax[0].set_ylabel("Residual"); ax[0].set_title("Residuals vs fitted")
    (osm, osr), (sl, ic, _) = stats.probplot(sr, dist="norm")
    ax[1].scatter(osm, osr, s=4, alpha=0.35, color=BLUE, edgecolor="none"); ax[1].plot(osm, sl * osm + ic, color=RED)
    ax[1].set_xlabel("Theoretical quantile"); ax[1].set_ylabel("Standardized residual"); ax[1].set_title("Normal QQ")
    ax[2].scatter(f, np.sqrt(np.abs(sr)), s=4, alpha=0.25, color=BLUE, edgecolor="none"); _lowess(ax[2], f.values, np.sqrt(np.abs(sr)))
    ax[2].set_xlabel("Fitted value"); ax[2].set_ylabel("sqrt(|standardized residual|)"); ax[2].set_title("Scale-location")
    fig.tight_layout(); fig.savefig(f"{figdir}/{label}_resid_main.png", dpi=110); plt.close(fig)
    # ---- Figure C: residuals vs each numeric predictor ----
    ncol_c = min(3, max(1, k)); nrow_c = int(np.ceil(max(1, k) / ncol_c))
    fig, ax = plt.subplots(nrow_c, ncol_c, figsize=(4.8 * ncol_c, 3.9 * nrow_c)); ax = np.atleast_1d(ax).ravel()
    for a_ in ax[k:]:
        a_.axis("off")
    rv = {}
    for i, v in enumerate(numeric_preds):
        ax[i].scatter(d[v], r, s=4, alpha=0.25, color=BLUE, edgecolor="none"); ax[i].axhline(0, color="k", lw=0.8); _lowess(ax[i], d[v].values, r.values)
        ax[i].set_xlabel(v); ax[i].set_ylabel("Residual"); ax[i].set_title(f"Residuals vs {v}")
        lw = sm.nonparametric.lowess(r.values, d[v].values, frac=0.3)
        rv[v] = {"lowess_max_abs_over_resid_sd": float(np.max(np.abs(lw[:, 1])) / r.std())}
    fig.tight_layout(); fig.savefig(f"{figdir}/{label}_resid_vs_numeric.png", dpi=110); plt.close(fig)
    out["resid_vs_numeric"] = rv
    # ---- Figure D: residual boxplots by categorical predictor (3 per row) ----
    kc = len(cat_preds); ncol = 3; nrow = int(np.ceil(kc / ncol))
    fig, ax = plt.subplots(nrow, ncol, figsize=(15, 3.6 * nrow)); ax = np.atleast_1d(ax).ravel()
    cb = {}
    for i, v in enumerate(cat_preds):
        g = d[v].astype(str)
        levs = list(pd.Series(g).value_counts().index)
        data_ = [r[g == L].values for L in levs]
        ax[i].boxplot(data_, labels=[str(L)[:10] for L in levs], showfliers=False)
        ax[i].axhline(0, color=RED, lw=0.8); ax[i].set_title(f"Residuals by {v}"); ax[i].tick_params(axis="x", labelrotation=45, labelsize=7)
        sds = [np.std(x) for x in data_ if len(x) > 5]
        lev_p = stats.levene(*[x for x in data_ if len(x) > 5]).pvalue if len(sds) > 1 else np.nan
        cb[v] = {"max_sd_ratio": float(max(sds) / min(sds)) if len(sds) > 1 else np.nan, "levene_p": float(lev_p)}
    for i in range(kc, len(ax)):
        ax[i].axis("off")
    fig.tight_layout(); fig.savefig(f"{figdir}/{label}_resid_by_categorical.png", dpi=105); plt.close(fig)
    out["resid_by_categorical"] = cb
    # ---- influence ----
    h = infl.hat_matrix_diag
    cd = infl.cooks_distance[0]
    # DFFITS / DFBETAS computed analytically (no leave-one-out refits)
    X = m.model.exog; e = m.resid.values
    XtX_inv = np.linalg.pinv(X.T @ X)
    s2 = m.ssr / (n - p)
    s2_i = ((n - p) * s2 - e ** 2 / (1 - h)) / (n - p - 1)
    t_ext = e / np.sqrt(s2_i * (1 - h))
    dff = t_ext * np.sqrt(h / (1 - h))
    names = list(m.params.index)
    dfb_cols = {}
    for t in focal_terms:
        if t in names:
            j = names.index(t)
            c = XtX_inv[j] @ X.T          # row j of (X'X)^-1 X'
            dfb_cols[t] = c * e / (1 - h) / (np.sqrt(s2_i) * np.sqrt(XtX_inv[j, j]))
    out["n"] = n; out["p"] = p
    out["leverage"] = {"cut_2p_over_n": 2 * p / n, "n_above": int((h > 2 * p / n).sum()), "max": float(h.max())}
    thr = 4 if n > 1000 else 3
    out["std_resid"] = {"cut": thr, "n_outliers": int((np.abs(sr) > thr).sum()), "max_abs": float(np.max(np.abs(sr)))}
    out["cooks"] = {"cut_4_over_n": 4 / n, "n_above_4n": int((cd > 4 / n).sum()),
                    "cut_F50": float(stats.f.ppf(0.5, p, n - p)), "n_above_F50": int((cd > stats.f.ppf(0.5, p, n - p)).sum()),
                    "max": float(cd.max())}
    out["dffits"] = {"cut_2sqrt_p_over_n": float(2 * np.sqrt(p / n)), "n_above": int((np.abs(dff) > 2 * np.sqrt(p / n)).sum()),
                     "max_abs": float(np.max(np.abs(dff)))}
    cut_b = 2 / np.sqrt(n)
    fb = {}
    for t, col in dfb_cols.items():
        fb[t] = {"n_above_2_over_sqrt_n": int((np.abs(col) > cut_b).sum()), "max_abs": float(np.max(np.abs(col)))}
    out["dfbetas"] = {"cut": float(cut_b), "focal": fb}
    # ---- Figure E: influence panel ----
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.1))
    ax[0].scatter(h, sr, s=5, alpha=0.3, color=BLUE, edgecolor="none"); ax[0].axvline(2 * p / n, color=RED, ls="--"); ax[0].axhline(thr, color=RED, ls="--"); ax[0].axhline(-thr, color=RED, ls="--")
    ax[0].set_xlabel("Leverage (hat)"); ax[0].set_ylabel("Standardized residual"); ax[0].set_title("Leverage vs standardized residual")
    ax[1].stem(np.arange(n), cd, markerfmt=" ", basefmt=" "); ax[1].axhline(4 / n, color=RED, ls="--"); ax[1].set_title("Cook's distance"); ax[1].set_xlabel("Observation")
    ax[2].stem(np.arange(n), dff, markerfmt=" ", basefmt=" "); ax[2].axhline(2 * np.sqrt(p / n), color=RED, ls="--"); ax[2].axhline(-2 * np.sqrt(p / n), color=RED, ls="--"); ax[2].set_title("DFFITS"); ax[2].set_xlabel("Observation")
    fig.tight_layout(); fig.savefig(f"{figdir}/{label}_influence.png", dpi=110); plt.close(fig)
    return out
