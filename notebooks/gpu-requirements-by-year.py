# Median minimum / recommended GPU in Steam system requirements by release year.
# Reads ../data/games.csv, writes gpu-requirements-by-year.png next to this script.
# Requires matplotlib.
import csv, statistics as st, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

S = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(S, "..", "data", "games.csv"), encoding="utf-8")))
by = {}
for r in rows:
    try:
        y = int(r["release_year"]); m = float(r["min_gpu_g3d"] or 0); rc = float(r["rec_gpu_g3d"] or 0)
    except ValueError:
        continue
    if 2010 <= y <= 2026 and m > 0:
        by.setdefault(y, []).append((m, rc))
years = sorted(by)
med_min = [st.median([m for m, _ in by[y]]) for y in years]
med_rec = [st.median([r for _, r in by[y] if r > 0]) for y in years]
n_min = sum(len(by[y]) for y in years)
n_rec = sum(sum(1 for _, r in by[y] if r > 0) for y in years)

SURF, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
S1, S2 = "#2a78d6", "#eb6834"   # validated categorical slots 1-2 (light)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13})
fig, ax = plt.subplots(figsize=(14, 8.4), dpi=120)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)

ax.plot(years, med_rec, color=S2, lw=2.4, marker="o", ms=8, mec=SURF, mew=2, zorder=3, label="Recommended GPU (median)")
ax.plot(years, med_min, color=S1, lw=2.4, marker="o", ms=8, mec=SURF, mew=2, zorder=3, label="Minimum GPU (median)")

# What the recommended median equals, in cards people know (G3D scores from the same dataset)
notes = {2014: ("≈ GTX 550 Ti", (-12, 6), "right"), 2019: ("= GTX 960", (0, 14), "center"),
         2022: ("= RX 580", (0, 14), "center"), 2025: ("= GTX 1660 Super", (-12, 4), "right"),
         2026: ("= RTX 2060", (0, 14), "center")}
for y, (label, off, ha) in notes.items():
    ax.annotate(label, (y, med_rec[years.index(y)]), xytext=off, textcoords="offset points", ha=ha,
                fontsize=12, color=INK2, fontweight="bold")

# direct labels at the line ends
ax.text(2026.3, med_rec[-1], "Recommended", color=INK, va="center", fontsize=12.5, fontweight="bold")
ax.text(2026.3, med_min[-1], "Minimum", color=INK, va="center", fontsize=12.5, fontweight="bold")

ax.set_xlim(2009.5, 2027.9)
ax.set_ylim(0, 16000)
ax.set_xticks(range(2010, 2027, 2))
ax.set_yticks(range(0, 16001, 4000))
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}"))
ax.grid(axis="y", color=GRID, lw=1); ax.set_axisbelow(True)
for s in ("top", "right", "left"): ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#bdbcb7")
ax.tick_params(colors=INK2, length=0, pad=8)
ax.set_ylabel("GPU benchmark score (PassMark G3D Mark)", color=INK2, labelpad=12)
ax.legend(loc="upper left", frameon=False, labelcolor=INK, fontsize=12.5, bbox_to_anchor=(0.0, 0.98))

fig.text(0.06, 0.955, "The GPU PC games ask for has grown about 10x since 2014", fontsize=21, fontweight="bold", color=INK)
fig.text(0.06, 0.915, "Median minimum and recommended graphics card in the Steam system requirements of PC games, by release year",
         fontsize=13.5, color=INK2)
fig.text(0.06, 0.03,
         f"Data: Steam store requirements of {n_min:,} games ({n_rec:,} with a recommended GPU); GPUs scored with PassMark G3D Mark. "
         "2026 = games released so far.\nOpen dataset (CC BY 4.0): github.com/emilioagustin83/pc-game-fps-dataset · pcgamebenchmarks.com",
         fontsize=11, color=MUTED, linespacing=1.5)
fig.subplots_adjust(left=0.09, right=0.93, top=0.86, bottom=0.14)
out = os.path.join(S, "gpu-requirements-by-year.png")
fig.savefig(out, facecolor=SURF)
print(out)
for y, a, b in zip(years, med_min, med_rec): print(y, int(a), int(b))
