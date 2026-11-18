#!/usr/bin/env python3
"""Graph functions of x to a clean PNG.
  plot.py "sin(x)" "x**2/4" --xmin -6 --xmax 6 --title "$f(x)=\\sin x$" -o graph.png
Expressions use numpy names (sin, exp, log, sqrt, pi, abs...). Labels accept $mathtext$."""
import argparse, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

p = argparse.ArgumentParser()
p.add_argument("exprs", nargs="+")
p.add_argument("--xmin", type=float, default=-10); p.add_argument("--xmax", type=float, default=10)
p.add_argument("--ymin", type=float); p.add_argument("--ymax", type=float)
p.add_argument("--labels", nargs="*"); p.add_argument("--title", default="")
p.add_argument("-o", "--out", default="graph.png")
a = p.parse_args()

ns = {k: getattr(np, k) for k in dir(np) if not k.startswith("_")}
x = np.linspace(a.xmin, a.xmax, 2000)
plt.rcParams.update({"font.size": 12, "mathtext.fontset": "cm", "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(7, 4.5), dpi=200)
for i, e in enumerate(a.exprs):
    with np.errstate(all="ignore"):
        y = np.asarray(eval(e, {"__builtins__": {}}, {**ns, "x": x}), dtype=float) * np.ones_like(x)
    jump = (a.ymax - a.ymin) / 2 if a.ymin is not None and a.ymax is not None else 1e3
    y[np.abs(np.diff(y, prepend=y[0])) > jump] = np.nan  # break lines at asymptotes
    lab = a.labels[i] if a.labels and i < len(a.labels) else f"$y={e.replace('**','^')}$"
    ax.plot(x, y, lw=2, label=lab)
ax.axhline(0, color="0.4", lw=0.8); ax.axvline(0, color="0.4", lw=0.8)
ax.grid(alpha=0.3); ax.set_xlim(a.xmin, a.xmax)
if a.ymin is not None or a.ymax is not None: ax.set_ylim(a.ymin, a.ymax)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_title(a.title); ax.legend(frameon=False)
fig.tight_layout(); fig.savefig(a.out); print(a.out)
