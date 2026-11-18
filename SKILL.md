---
name: render-math
description: Make math and graphs render properly in Claude replies (like ChatGPT). Use whenever a reply contains equations, LaTeX, derivations, homework solutions, or anything that should be graphed or plotted.
---

# Render math & graphs properly

Claude's chat renderer (claude.ai web, desktop, mobile) uses KaTeX, but it only reliably
recognises `$$ ... $$`. Single `$...$`, `\( \)` and `\[ \]` often show up as raw text.
Follow these rules every time math appears.

## 1. Math in chat replies

- **Always use `$$ ... $$`** for math — both inline and display.
  - Inline: put it mid-sentence: `The slope is $$m = \frac{\Delta y}{\Delta x}$$ here.`
  - Display: put it on its own line with a blank line above and below.
- **Never** use single `$`, `\( \)`, `\[ \]`, or ```` ```latex ```` code blocks for math the user should *read*.
  (Code blocks only when the user asks for LaTeX source to copy.)
- Write currency as `USD 5` or `5 dollars`, never `$5`, in any reply that also contains math.
- Don't put math inside markdown headings, bold, tables or links — KaTeX can break there. Put it in a normal sentence.
- Multi-line work: use `\begin{aligned} ... \end{aligned}` inside one `$$` block, with `&=` to line up equals signs.
  ```
  $$
  \begin{aligned}
  \int_0^1 x e^{x}\,dx &= \big[x e^{x}\big]_0^1 - \int_0^1 e^{x}\,dx \\
  &= e - (e - 1) = 1
  \end{aligned}
  $$
  ```
- Use proper commands: `\sin`, `\ln`, `\lim_{x\to 0}`, `\frac{}{}`, `\sqrt{}`, `\cdot`, `\,dx`, `\left( \right)`, `\mathbb{R}`, `\vec{v}`.
- Supported environments: `aligned`, `cases`, `pmatrix`, `bmatrix`, `vmatrix`, `array`. Not supported: `align` (use `aligned`), `\label`, `\ref`, `\usepackage`, TikZ.
- Number steps in prose ("**Step 1.** Factor the numerator:") then show the math on the next line.
- Box final answers: `$$\boxed{x = 3}$$`.

## 2. Graphs — pick the lightest tool that works

1. **Simple data chart** (line/bar/scatter from a handful of numbers): use the native chart tool
   (`chart_display_v0`) if available. Renders instantly.
2. **Graph of a function, or an explanatory diagram inline**: use the Visualizer
   (`show_widget`, load `read_me` with the `chart` module first). For functions, sample
   x in JS and draw with Chart.js/SVG; break the line at asymptotes (set `null` where |Δy| is huge).
3. **No visual tools / need a PNG** (homework, docs, slides, image to save): run
   ```
   python3 scripts/plot.py "sin(x)" "x**2/8" --xmin -6 --xmax 6 --ymin -4 --ymax 4 \
       --labels '$\sin x$' '$x^2/8$' --title 'My graph' -o graph.png
   ```
   then send `graph.png` with SendUserFile. Expressions are numpy (`sin, exp, log, sqrt, pi, abs`, `**` for powers).
   Always pass `--ymin/--ymax` when there are asymptotes (`1/x`, `tan x`) so they render cleanly.
4. **Something to keep or share** (worked solution, study guide, interactive graph):
   copy `assets/math-page.html`, fill in the content and `FUNCS`, and publish it as an artifact.
   It has KaTeX + Plotly (zoom/hover) and dark mode.

After making any image, look at it (Read the PNG) before sending — check labels, ranges, and that curves aren't joined across asymptotes.

## 3. Equation images

When math must go somewhere that won't render LaTeX (an image, a slide, a Word doc, a text message):
```
python3 scripts/tex2png.py '\int_0^1 x^2\,dx = \frac{1}{3}' -o eq.png
```
Uses real LaTeX (amsmath) when installed, matplotlib mathtext otherwise.

## Quick self-check before sending a math reply

- [ ] Every formula is wrapped in `$$ ... $$` (no single `$`, no `\(`).
- [ ] No `$` used for money.
- [ ] Multi-step derivations use `aligned`, not several loose lines.
- [ ] If the question involves a function's shape, a graph is included.
