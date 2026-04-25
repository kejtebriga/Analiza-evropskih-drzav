import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# preberemo csv
try:
    df = pd.read_csv("world_bank_data.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("Napaka: world_bank_data.csv ne obstaja.")
    print("Najprej zaženi pridobi_podatke.py")
    exit()


pivot = df.pivot_table(
    index=["country", "year"],
    columns="indicator",
    values="value",
    aggfunc="first"
).reset_index()

# povprečje čez vsa leta za vsako državo 
povprecje = pivot.groupby("country").mean(numeric_only=True)

# zadnje leto za vsako državo
zadnje = pivot.sort_values("year").groupby("country").last()

# slovensko ime, enota in smer za vsak kazalnik
kazalniki_slo = {
    "gdp_per_capita":     ("BDP na prebivalca",                "USD",       True),
    "life_expectancy":    ("Pričakovana življenjska doba",     "let",       True),
    "unemployment":       ("Stopnja brezposelnosti",           "%",         False),
    "youth_unemployment": ("Brezposelnost mladih (15–24 let)", "%",         False),
    "internet_users":     ("Delež internetnih uporabnikov",    "%",         True),
    "fertility_rate":     ("Stopnja rodnosti",                 "otr./žen.", True),
    "inflation":          ("Stopnja inflacije",                "%",         False),
    "infant_mortality":   ("Umrljivost dojenčkov",             "na 1000",   False),
}

# ocena kazalnika: (pozitivna ocena, negativna ocena)
ocene_kazalnikov = {
    "gdp_per_capita":     ("visok",  "nizek"),
    "life_expectancy":    ("visoka", "nizka"),
    "unemployment":       ("nizka",  "visoka"),
    "youth_unemployment": ("nizka",  "visoka"),
    "internet_users":     ("visok",  "nizek"),
    "inflation":          ("nizka",  "visoka"),
    "infant_mortality":   ("nizka",  "visoka"),
}

# scenariji: kazalnik (True = višje boljše, False = nižje boljše, utež)
scenariji = {
    "druzina": {
        "naziv": "Iskalnik najboljše države za družino",
        "opis":  "Iščemo državo ki ponuja najboljše razmere za življenje družine.",
        "kazalniki": {
            "life_expectancy":    (True,  0.30),
            "infant_mortality":   (False, 0.30),
            "youth_unemployment": (False, 0.20),
            "gdp_per_capita":     (True,  0.20),
        },
    },
    "mladi": {
        "naziv": "Iskalnik najboljše države za mlade",
        "opis":  "Iščemo državo, ki ponuja najboljše priložnosti za mlade.",
        "kazalniki": {
            "youth_unemployment": (False, 0.40),
            "gdp_per_capita":     (True,  0.35),
            "internet_users":     (True,  0.25),
        },
    },
    "pokoj": {
        "naziv": "Iskalnik najboljše države za upokojence",
        "opis":  "Iščemo državo, ki ponuja najboljše razmere za življenje upokojencev.",
        "kazalniki": {
            "life_expectancy":  (True,  0.30),
            "inflation":        (False, 0.30),
            "gdp_per_capita":   (True,  0.25),
            "infant_mortality": (False, 0.15),
        },
    },
}


def izracunaj_scenarij(kljuc):
    scenarij  = scenariji[kljuc]
    kazalniki = scenarij["kazalniki"]
    data      = povprecje.copy()

    
    dostopni = [k for k in kazalniki if k in data.columns]
    if not dostopni:
        return None

    data = data[dostopni].copy()

    # negiramo kazalnike kjer je nižje = boljše
    for kaz in dostopni:
        if not kazalniki[kaz][0]:
            data[kaz] = -data[kaz]

    # odstranimo države kjer manjka preveč vrednosti
    data = data.dropna(thresh=max(1, len(dostopni) - 1))
    if data.empty:
        return None

    # normalizacija na 0-1
    scaler = MinMaxScaler()
    norm   = pd.DataFrame(
        scaler.fit_transform(data),
        index=data.index,
        columns=data.columns,
    )

    # uteženo povprečje
    score      = pd.Series(0.0, index=norm.index)
    vsota_utez = 0.0
    for kaz in dostopni:
        utez        = kazalniki[kaz][1]
        score      += norm[kaz] * utez
        vsota_utez += utez

    norm["score"] = score / vsota_utez
    return norm.sort_values("score", ascending=False)


def generiraj_razlago(drzava, kljuc):
    kazalniki = scenariji[kljuc]["kazalniki"]

    if drzava not in povprecje.index:
        return ""

    vrednosti = povprecje.loc[drzava]
    vrstice   = []

    for kaz, (visje_boljse, _) in kazalniki.items():
        if kaz not in vrednosti or pd.isna(vrednosti[kaz]):
            continue

        vrednost  = vrednosti[kaz]
        naziv_kaz, enota, _ = kazalniki_slo.get(kaz, (kaz, "", True))
        vrednost_str = f"{vrednost:.1f}"
        enota_str    = f" {enota}" if enota else ""

        if kaz in povprecje.columns:
            je_nad = vrednost > povprecje[kaz].mean()
            pozitivna, negativna = ocene_kazalnikov.get(kaz, ("visoka", "nizka"))
            if (visje_boljse and je_nad) or (not visje_boljse and not je_nad):
                ocena = pozitivna
            else:
                ocena = negativna

            vrstica = f"  {naziv_kaz:<42} {vrednost_str + enota_str:<18}  — {ocena}"
            vrstice.append(vrstica)

    if not vrstice:
        return ""

    return "\n".join(vrstice)


def naslov(tekst):
    print(f"\n  {tekst}")
    print("  " + "-" * (len(tekst) + 2))


def analiza_drzava(ime_drzave):
    naslov(f"PODATKI — {ime_drzave.upper()}")
    d = df[df["country"] == ime_drzave]
    if d.empty:
        print(f"  Država '{ime_drzave}' ni najdena.")
        return
    zadnje_d = d.sort_values("year").groupby("indicator").last()
    print()
    for kaz, vrstica in zadnje_d.iterrows():
        naziv_kaz, enota, _ = kazalniki_slo.get(kaz, (kaz, "", True))
        print(f"  {naziv_kaz:<40} {vrstica['value']:>10.2f} {enota}")


def analiza_kazalnik(kazalnik):
    naziv_kaz, enota, _ = kazalniki_slo.get(kazalnik, (kazalnik, "", True))
    naslov(f"PRIMERJAVA — {naziv_kaz.upper()}")

    d = df[df["indicator"] == kazalnik]

    if d.empty:
        print(f"  Kazalnik '{kazalnik}' ni najden.")
        return

    povprecje_k = (
        d.groupby("country")["value"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\n  Povprečje za celotno obdobje:\n")

    for drzava, vrednost in povprecje_k.items():
        print(f"  {drzava:<12} {vrednost:>10.2f} {enota}")
        
def analiza_scenarij(kljuc):
    if kljuc not in scenariji:
        print(f"  Scenarij '{kljuc}' ne obstaja.")
        return

    scenarij  = scenariji[kljuc]
    rezultati = izracunaj_scenarij(kljuc)

    naslov(scenarij["naziv"].upper())
    print()
    print(f"  {scenarij['opis']}")

    print("\n  Kazalniki:\n")
    for kaz, (smer, _) in scenarij["kazalniki"].items():
        naziv_kaz, enota, _ = kazalniki_slo.get(kaz, (kaz, "", True))
        smer_txt = "višje = boljše" if smer else "nižje = boljše"
        print(f"  {naziv_kaz:<42} {smer_txt}   [{enota}]")

    if rezultati is None:
        print("\n  Premalo podatkov.")
        return

    print("\n  Razvrstitev:\n")
    for i, (drzava, _) in enumerate(rezultati.iterrows(), 1):
        print(f"  {i}. {drzava}")

    zmagovalec = rezultati.index[0]
    razlaga    = generiraj_razlago(zmagovalec, kljuc)
    if razlaga:
        naziv = scenarij["naziv"].lower().replace("iskalnik najboljše države za ", "")
        print(f"\n  Zakaj je {zmagovalec} najboljša država za {naziv}?")
        print(razlaga)