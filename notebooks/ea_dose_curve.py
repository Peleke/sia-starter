# %% [markdown]
# # Did the change help, and how sure are we?
#
# This script compares a **baseline** (arm 0) with one or more **changed** versions of an agent
# (arms 1, 2, … or any numbers) on the same held-out **groups**, and reports the gain with a
# bootstrap interval.
#
# **Bundled example:** `data/ea-cells.csv`, an aggregate copy of one pre-registered experiment ("E-a")
# on the ranking step of a pipeline (overview: `docs/example-pipeline.md`). A model judge orders the
# claims in a short document; we score its order against a gold ranking by **pair agreement**: the
# share of claim pairs ordered the same way as the gold. Arms are the number of labeled demo pairs
# given to the judge (0, 2, 4, 8). 5 groups (one per gold document) × 3 reps. A group never sees
# demos taken from its own document (leave-one-out).
#
# **Your data:** `--cells your.csv` with columns `group,arm,rep,score[,excluded]`. With only arm 0 and two or
# more reps per group, the script runs an A/A check instead: how much the score moves when nothing changed.
# See `data/example-own.csv` and the README for where each column comes from.
#
# **Method:**
# - reps are averaged within each group × arm; groups count equally
# - for each changed arm: the paired difference vs arm 0, per group, over groups that have both
# - one bootstrap over those group differences (10,000 resamples, fixed seed); both interval ends
#   come from the same resamples
#
# The result is an **approximate 95% bootstrap percentile interval**. With few groups it is wide
# and its coverage is unreliable: treat it as illustrative. A group must be an independent unit
# (the same unit you grouped your gold set by). Several changed arms are exploratory comparisons;
# for a claim, write down one primary comparison before you run.

# %%
import argparse
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def find_root() -> Path:
    start = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
    for p in [start, *start.parents]:
        if (p / "pyproject.toml").exists():
            return p
    sys.exit("could not find the kit root (no pyproject.toml above this file)")


ROOT = find_root()
BUNDLED = ROOT / "data/ea-cells.csv"

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--cells", type=Path, default=BUNDLED, help="CSV with group,arm,rep,score[,excluded]")
parser.add_argument("--score-label", default=None, help="axis label for the score")
parser.add_argument("--arm-label", default=None, help="axis label for the arms")
parser.add_argument("--reference", action=argparse.BooleanOptionalAction, default=None,
                    help="check point estimates against data/ea-reference.json (default: on for the bundled data only)")
parser.add_argument("--out", type=Path, default=None, help="figure path (default: out/<input name>.png)")
in_notebook = "ipykernel" in sys.modules
args = parser.parse_args([] if in_notebook else None)
bundled = args.cells.resolve() == BUNDLED.resolve()
reference = bundled if args.reference is None else args.reference
score_label = args.score_label or ("pair agreement with gold" if bundled else "score")
arm_label = args.arm_label or ("labeled demo pairs (k)" if bundled else "arm")
out_path = args.out or ROOT / "out" / ("dose-curve.png" if bundled else f"{args.cells.stem}.png")

# %% Load and validate
def fail(msg: str):
    sys.exit(f"input error ({args.cells}): {msg}")

cells = pd.read_csv(args.cells)
missing = {"group", "arm", "rep", "score"} - set(cells.columns)
if missing:
    fail(f"missing columns {sorted(missing)}; need group,arm,rep,score[,excluded]")
if "excluded" not in cells:
    cells["excluded"] = 0
if not pd.api.types.is_numeric_dtype(cells.score) or cells.score.isna().any():
    fail("score must be numeric with no blanks")
if not cells.excluded.isin([0, 1]).all():
    fail("excluded must be 0 or 1")
dupes = cells[cells.duplicated(["group", "arm", "rep"], keep=False)]
if len(dupes):
    fail(f"duplicate group/arm/rep rows, e.g. {dupes.iloc[0][['group', 'arm', 'rep']].tolist()}")
cells = cells[cells.excluded == 0]
if 0 not in set(cells.arm):
    fail("no baseline rows (arm 0)")

# %% Baseline only? Then measure the noise floor instead (an A/A check)
SEED, N_BOOT = 12345, 10_000
print(f"loaded {len(cells)} rows from {args.cells.name}: {cells.group.nunique()} groups, arms {sorted(int(a) for a in cells.arm.unique())}", flush=True)
if set(cells.arm) == {0}:
    by_rep = cells.pivot_table(index="group", columns="rep", values="score")
    if by_rep.shape[1] < 2:
        fail("only arm 0 and one rep per group: run the baseline at least twice per group to see the noise floor")
    first, second = by_rep.columns[:2]
    pair = by_rep[[first, second]].dropna()
    d = (pair[second] - pair[first]).to_numpy()
    if len(d) < 2:
        fail("fewer than 2 groups have both baseline reps")
    boots = np.random.default_rng(SEED).choice(d, size=(N_BOOT, len(d)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    print(f"\nA/A check (baseline rep {second} vs rep {first}, nothing changed): difference {d.mean():+.3f}, "
          f"approx. 95% interval [{lo:.3f}, {hi:.3f}] over {len(d)} groups.")
    print(f"A real change needs a gain clearly outside about ±{max(abs(lo), abs(hi)):.3f} to stand out from run-to-run noise "
          "with this many groups. More groups shrink it.")
    PARCH, FALUN, INK, MUTED = "#f8f5ef", "#9a2520", "#141414", "#8a8580"
    sns.set_theme(style="white", rc={"axes.facecolor": PARCH, "figure.facecolor": PARCH})
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.axhspan(lo, hi, color=FALUN, alpha=0.15, label="approx. 95% interval of the mean difference")
    ax.axhline(0, color=INK, lw=1, alpha=0.6)
    ax.scatter(range(len(d)), d, color=MUTED, zorder=3, label="per-group difference")
    ax.set(xticks=range(len(d)), xticklabels=list(pair.index), ylabel=f"rep {second} − rep {first}",
           title="A/A check: how much the score moves when nothing changed")
    ax.legend(frameon=False, fontsize=9)
    sns.despine(fig)
    aa_path = args.out or ROOT / "out" / f"{args.cells.stem}.png"
    aa_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(aa_path, dpi=200, bbox_inches="tight")
    print(f"\nfigure: {aa_path}")
    sys.exit(0)

# %% Paired differences per group, one bootstrap per comparison
cell_means = cells.groupby(["group", "arm"], as_index=False).score.mean()
wide = cell_means.pivot(index="group", columns="arm", values="score").sort_index(axis=1)
reps = cells.groupby(["group", "arm"]).size().unstack()
rng = np.random.default_rng(SEED)

rows = [{"arm": 0, "mean": wide[0].mean(), "n_groups": int(wide[0].notna().sum()),
         "gain": 0.0, "ci_low": np.nan, "ci_high": np.nan, "dropped": ""}]
for arm in [a for a in wide.columns if a != 0]:
    pair = wide[[0, arm]].dropna()
    dropped = sorted(set(wide.index) - set(pair.index))
    d = (pair[arm] - pair[0]).to_numpy()
    if len(d) < 2:
        fail(f"arm {arm}: fewer than 2 groups have both this arm and arm 0")
    boots = rng.choice(d, size=(N_BOOT, len(d)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    rows.append({"arm": arm, "mean": pair[arm].mean(), "n_groups": len(d), "gain": d.mean(),
                 "ci_low": lo, "ci_high": hi, "dropped": ",".join(map(str, dropped))})
summary = pd.DataFrame(rows).set_index("arm")

pd.set_option("display.width", 120)
print(summary.round(3).to_string())
print(f"\nreps per group x arm: min {int(reps.min().min())}, max {int(reps.max().max())}")
print("`dropped` = groups left out of that comparison because they have no row for that arm or for arm 0.")
for arm, r in summary.drop(index=0).iterrows():
    verdict = "includes zero: inconclusive" if r.ci_low <= 0 <= r.ci_high else "excludes zero"
    print(f"arm {arm} vs 0: gain {r.gain:+.3f}, approx. 95% interval [{r.ci_low:.3f}, {r.ci_high:.3f}] "
          f"over {r.n_groups} groups ({verdict})")
print(f"\nWith {int(summary.n_groups.min())} groups the interval is wide and its coverage is unreliable; "
      "treat it as illustrative. More independent groups narrow it.")

# %% Check against the original analysis (bundled data only)
if reference:
    ref = json.loads((ROOT / "data/ea-reference.json").read_text())
    for k, v in ref["meanPairAgreementByK"].items():
        assert abs(summary.loc[int(k), "mean"] - v) < 1e-9, f"mean for arm {k} differs from the reference"
    for k, v in ref["diffsVsK0"].items():
        assert abs(summary.loc[int(k), "gain"] - v["meanDiff"]) < 1e-9, f"gain for arm {k} differs from the reference"
        lo, hi = v["ci95"]
        assert abs(summary.loc[int(k), "ci_low"] - lo) < 0.01 and abs(summary.loc[int(k), "ci_high"] - hi) < 0.01, \
            f"interval for arm {k} differs from the reference"
    print("\nchecks passed: point estimates match the original analysis exactly; interval ends match within 0.01.")
    print("(The original used a different random number generator and quantile rule, so the ends can differ slightly.)")

# %% Figure: score per group (faint) and mean; gain per arm with its interval
PARCH, FALUN, INK, MUTED = "#f8f5ef", "#9a2520", "#141414", "#8a8580"
sns.set_theme(style="white", rc={"axes.facecolor": PARCH, "figure.facecolor": PARCH, "font.family": "sans-serif"})
fig, (a, b) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"wspace": 0.28})
arms = list(wide.columns)
pos = {arm: i for i, arm in enumerate(arms)}

for _, g in cell_means.groupby("group"):
    a.plot([pos[x] for x in g.arm], g.score, color=MUTED, alpha=0.45, lw=1, marker=".", ls=":")
a.plot([pos[x] for x in summary.index], summary["mean"], color=FALUN, lw=0, marker="o", ms=9, label="mean over groups")
a.axhline(summary.loc[0, "mean"], color=INK, ls="--", lw=1, alpha=0.6, label="baseline (arm 0)")
a.set(xlabel=arm_label, ylabel=score_label, xticks=range(len(arms)), xticklabels=arms, title="Score per group (faint) and mean")
a.legend(frameon=False)

changed = summary.drop(index=0)
xs = [pos[x] for x in changed.index]
b.axhline(0, color=INK, lw=1, alpha=0.6)
b.errorbar(xs, changed.gain, yerr=[changed.gain - changed.ci_low, changed.ci_high - changed.gain],
           fmt="o", color=FALUN, ecolor=FALUN, elinewidth=2.5, capsize=6, ms=8)
for x, (_, r) in zip(xs, changed.iterrows()):
    note = "includes zero" if r.ci_low <= 0 <= r.ci_high else "excludes zero"
    b.annotate(f"{note} (n={r.n_groups})", (x, r.ci_high), textcoords="offset points", xytext=(0, 10),
               ha="center", va="bottom", color=MUTED, fontsize=9)
b.set(xlabel=arm_label, ylabel="gain vs arm 0", xticks=xs, xticklabels=list(changed.index),
      xlim=(min(xs) - 0.6, max(xs) + 0.6), title="Gain with approx. 95% bootstrap interval")
lo_y, hi_y = min(0, changed.ci_low.min()), max(0, changed.ci_high.max())
b.set_ylim(lo_y - 0.1 * (hi_y - lo_y), hi_y + 0.18 * (hi_y - lo_y))
sns.despine(fig)
out_path.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out_path, dpi=200, bbox_inches="tight")
print(f"\nfigure: {out_path}")
