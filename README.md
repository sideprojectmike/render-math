# render-math

A Claude skill that makes math and graphs render properly in Claude chats, the way ChatGPT does.

- Forces KaTeX-safe `$$ ... $$` math (single `$` and `\( \)` often show as raw text in Claude)
- Picks the right graph tool: native charts, inline Visualizer, PNG plots, or an interactive KaTeX + Plotly page
- `scripts/plot.py` graphs functions to clean PNGs (handles asymptotes)
- `scripts/tex2png.py` turns LaTeX into equation images

## Install

Tell Claude to:
```
Install this skill for me: https://github.com/sideprojectmike/render-math
```

#OR

Zip this folder and upload it in Claude under **Settings → Capabilities → Skills**, or copy it to `~/.claude/skills/render-math` for Claude Code.

```
python3 scripts/plot.py "sin(x)" "1/x" --xmin -6 --xmax 6 --ymin -4 --ymax 4 -o graph.png
python3 scripts/tex2png.py '\frac{d}{dx} e^{x^2} = 2x e^{x^2}' -o eq.png
```
