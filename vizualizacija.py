import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

barve = {
    "Slovenija": "#e63946",
    "Avstrija":  "#457b9d",
    "Hrvaška":   "#2a9d8f",
    "Madžarska": "#e9c46a",
    "Italija":   "#f4a261",
    "Češka":     "#6d6875",
    "Slovaška":  "#a8c5da",
    "Nemčija":   "#3d405b",
}

naslovi = {
    "gdp_per_capita":     "BDP na prebivalca",
    "life_expectancy":    "Pričakovana življenjska doba",
    "unemployment":       "Stopnja brezposelnosti",
    "youth_unemployment": "Brezposelnost mladih (15–24 let)",
    "internet_users":     "Delež internetnih uporabnikov",
    "fertility_rate":     "Stopnja rodnosti",
    "inflation":          "Stopnja inflacije",
    "infant_mortality":   "Umrljivost dojenčkov",
}

enote = {
    "gdp_per_capita":     "USD",
    "life_expectancy":    "let",
    "unemployment":       "%",
    "youth_unemployment": "%",
    "internet_users":     "%",
    "fertility_rate":     "otr./žen.",
    "inflation":          "%",
    "infant_mortality":   "na 1000 rojstev",
}


def nalozi():
    try:
        return pd.read_csv("world_bank_data.csv", encoding="utf-8-sig")
    except FileNotFoundError:
        print("Napaka: world_bank_data.csv ne obstaja.")
        print("Najprej zaženi pridobi_podatke.py")
        exit()


def barva(drzava):
    return barve.get(drzava, "#888888")


def graf_kazalnik_vse_drzave(df, kazalnik):
    d = df[df["indicator"] == kazalnik].sort_values("year")
    if d.empty:
        print(f"  Ni podatkov za '{kazalnik}'.")
        return

    fig, ax = plt.subplots(figsize=(11, 6))

    for drzava in sorted(d["country"].unique()):
        pod = d[d["country"] == drzava]
        ax.plot(
            pod["year"], pod["value"],
            label=drzava,
            color=barve.get(drzava, "#888888"),
            linewidth=3.0 if drzava == "Slovenija" else 1.8,
        )

    ax.set_title(f"{naslovi.get(kazalnik, kazalnik)} (2000–2023)", fontsize=13, fontweight="bold")
    ax.set_xlabel("Leto")
    ax.set_ylabel(enote.get(kazalnik, ""))
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3, linestyle="--")
    ax.set_xlim(2000, 2023)

    if kazalnik == "gdp_per_capita":
        ax.yaxis.set_major_formatter(
            ticker.FuncFormatter(lambda x, _: f"{x:,.0f}")
        )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    plt.close()


def graf_kazalnik_ena_drzava(df, kazalnik, drzava):
    d = df[
        (df["indicator"] == kazalnik) &
        (df["country"]   == drzava)
    ].sort_values("year")

    if d.empty:
        print("  Ni podatkov.")
        return

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(d["year"], d["value"], color=barva(drzava), linewidth=2.5, marker="o", markersize=4)
    ax.fill_between(d["year"], d["value"], alpha=0.12, color=barva(drzava))
    ax.set_title(f"{drzava} — {naslovi.get(kazalnik, kazalnik)}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Leto")
    ax.set_ylabel(enote.get(kazalnik, ""))
    ax.grid(alpha=0.3, linestyle="--")
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
    plt.close()


def graf_vsi_kazalniki(df, drzava):
    kazalniki = sorted(df["indicator"].unique())
    cols = 3
    rows = (len(kazalniki) + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(16, rows * 4.5))
    axes = axes.flatten()
    fig.suptitle(f"Vsi kazalniki — {drzava}", fontsize=14, fontweight="bold", y=1.0)
    fig.subplots_adjust(hspace=0.55, wspace=0.35)

    d_drzava = df[df["country"] == drzava]

    for i, kaz in enumerate(kazalniki):
        ax  = axes[i]
        pod = d_drzava[d_drzava["indicator"] == kaz].sort_values("year")
        if pod.empty:
            ax.set_visible(False)
            continue

        ax.plot(pod["year"], pod["value"], color=barva(drzava), linewidth=2)
        ax.fill_between(pod["year"], pod["value"], alpha=0.1, color=barva(drzava))
        ax.set_title(naslovi.get(kaz, kaz), fontsize=9, fontweight="bold", pad=8)
        ax.set_ylabel(enote.get(kaz, ""), fontsize=8)
        ax.grid(alpha=0.3, linestyle="--")
        ax.tick_params(labelsize=7)
        ax.set_xticks([pod["year"].min(), pod["year"].max()])

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()
    plt.close()