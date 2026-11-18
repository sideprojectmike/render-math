#!/usr/bin/env python3
"""Render LaTeX to a crisp PNG for surfaces that can't show math (images, docs, slides).
  tex2png.py "\\int_0^1 x^2\\,dx = \\tfrac13" -o eq.png
Uses real LaTeX (amsmath) when installed, else matplotlib mathtext."""
import argparse, shutil, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

p = argparse.ArgumentParser(); p.add_argument("tex"); p.add_argument("-o", "--out", default="eq.png")
p.add_argument("--size", type=int, default=22); a = p.parse_args()
if shutil.which("latex") and shutil.which("dvipng"):
    plt.rcParams.update({"text.usetex": True, "text.latex.preamble": r"\usepackage{amsmath,amssymb}"})
    s = r"$\displaystyle " + a.tex + "$"
else:
    plt.rcParams["mathtext.fontset"] = "cm"; s = "$" + a.tex + "$"
fig = plt.figure(figsize=(0.01, 0.01))
fig.text(0, 0, s, fontsize=a.size)
fig.savefig(a.out, dpi=300, bbox_inches="tight", pad_inches=0.1, transparent=False, facecolor="white")
print(a.out)
