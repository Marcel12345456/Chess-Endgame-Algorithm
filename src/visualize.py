import glob
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Pro Suchtiefe wird ein eigener Satz PNGs erzeugt.
dateien = sys.argv[1:] or sorted(glob.glob(str(RESULTS_DIR / 'results_depth*.csv')))
print(f"Eingelesen: {', '.join(dateien)}\n")
alle = pd.concat([pd.read_csv(d) for d in dateien], ignore_index=True)

def erzeuge_plots(df, tiefe):
    suffix = f'_depth{tiefe}'
    zusatz = f' (Suchtiefe {tiefe})'

    # Remisstellungen aussortieren: DTM gibt es nur für Gewinnstellungen
    gesamt = len(df)
    df = df[df['tablebase'].notna() & (df['tablebase'] > 0)].copy()
    remis = gesamt - len(df)

    # Vergleich: gespielte Halbzüge vs. optimale Mattdistanz
    df['diff'] = df['heuristic'] - df['tablebase']
    df['ratio'] = df['heuristic'] / df['tablebase']

    # Plot 1: Differenz zur optimalen Mattdistanz
    plt.figure()
    bins = np.arange(df['diff'].min() - 0.5, df['diff'].max() + 1.5, 1)
    plt.hist(df['diff'], bins=bins, rwidth=0.85, color='tab:blue', alpha=0.75)
    plt.axvline(0, color='red', linestyle='--', alpha=0.7, label='optimal (0)')
    plt.xlabel('gespielte - optimale Halbzüge')
    plt.ylabel('Häufigkeit')
    plt.title('Differenz zur optimalen Mattdistanz' + zusatz)
    plt.legend()
    plt.savefig(RESULTS_DIR / f'diff_histogramm{suffix}.png', dpi=200)
    plt.close()

    # Plot 2: Effizienz relativ zum Optimum als kategoriale Balken.
    r = df['ratio']
    kategorien = ['< 1,0', '= 1,0', '1,0-1,1', '1,1-1,25', '1,25-1,5',
                  '1,5-2,0', '> 2,0']
    anzahl = [
        int((r < 1.0).sum()),
        int((r == 1.0).sum()),
        int(((r > 1.0) & (r <= 1.1)).sum()),
        int(((r > 1.1) & (r <= 1.25)).sum()),
        int(((r > 1.25) & (r <= 1.5)).sum()),
        int(((r > 1.5) & (r <= 2.0)).sum()),
        int((r > 2.0).sum()),
    ]
    plt.figure()
    balken = plt.bar(kategorien, anzahl, color='tab:blue', alpha=0.8)
    for rect, n in zip(balken, anzahl):
        plt.text(rect.get_x() + rect.get_width() / 2, n + 0.5, str(n),
                 ha='center', va='bottom')
    plt.xlabel('gespielt / optimal')
    plt.ylabel('Anzahl Stellungen')
    plt.title('Effizienz relativ zum Optimum' + zusatz)
    plt.savefig(RESULTS_DIR / f'ratio_kategorien{suffix}.png', dpi=200)
    plt.close()

    # Plot 3: gespielt vs. optimal pro Stellung, Dichte über Transparenz.
    maximum = max(df['tablebase'].max(), df['heuristic'].max())
    alpha = 0.2
    plt.figure()
    plt.plot([0, maximum], [0, maximum], color='red', linestyle='--',
             alpha=0.7, zorder=1)
    plt.scatter(df['tablebase'], df['heuristic'], s=70, alpha=alpha,
                color='tab:blue', edgecolors='none', zorder=2)
    plt.xlabel('optimale DTM (Halbzüge)')
    plt.ylabel('gespielte Halbzüge')
    plt.title('Gespielt vs. optimal pro Stellung' + zusatz)
    stufen = [1, 3, 6, 12]
    handles = [Line2D([], [], linestyle='--', color='red', alpha=0.7)]
    handles += [Line2D([], [], marker='o', linestyle='', markersize=9,
                       color='tab:blue', alpha=1 - (1 - alpha) ** n,
                       markeredgecolor='none')
                for n in stufen]
    plt.legend(handles, ['optimal (y=x)'] + [str(n) for n in stufen],
               title='Stellungen')
    plt.savefig(RESULTS_DIR / f'scatter_alpha{suffix}.png', dpi=200)
    plt.close()

    print(f"--- Suchtiefe {tiefe} ---")
    print(f"Stellungen gesamt:       {gesamt}")
    print(f"davon Remis (entfernt):  {remis}")
    print(f"ausgewertet:             {len(df)}")
    print(f"Differenz: Median={df['diff'].median():.1f}  Mittelwert={df['diff'].mean():.1f}")
    print(f"Ratio:     Median={df['ratio'].median():.2f}  Mittelwert={df['ratio'].mean():.2f}")
    print()

# pro Suchtiefe ein eigener Satz PNGs (Suffix _depth4, _depth6, ...)
for tiefe, gruppe in alle.groupby('depth'):
    erzeuge_plots(gruppe, int(tiefe))