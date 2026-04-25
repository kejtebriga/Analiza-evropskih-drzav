import os

from analiza import (
    df, kazalniki_slo,
    analiza_drzava, analiza_kazalnik,
    analiza_scenarij,
)
from vizualizacija import (
    nalozi,
    graf_kazalnik_vse_drzave, graf_kazalnik_ena_drzava,
    graf_vsi_kazalniki,
)


def pocisti():
    os.system("cls" if os.name == "nt" else "clear")


def pritisni_enter():
    input("\n  [Enter za nadaljevanje]")


def izberi_drzavo():
    pocisti()
    drzave = sorted(df["country"].unique())
    print("\n  Izberi državo:")
    print("  0. Nazaj")

    for i, d in enumerate(drzave, 1):
        print(f"  {i}. {d}")

    izbira = input("\n  Vpiši številko: ").strip()

    if izbira == "0":
        return None

    if izbira.isdigit():
        idx = int(izbira) - 1
        if 0 <= idx < len(drzave):
            return drzave[idx]

    for d in drzave:
        if izbira.lower() in d.lower():
            return d

    print("  Država ni najdena.")
    pritisni_enter()
    return None

def izberi_kazalnik():
    pocisti()
    kazalniki = sorted(df["indicator"].unique())
    print("\n  Izberi kazalnik:")
    print("  0. Nazaj")

    for i, k in enumerate(kazalniki, 1):
        naziv, enota, _ = kazalniki_slo.get(k, (k, "", True))
        print(f"  {i:>2}. {naziv}  [{enota}]")

    izbira = input("\n  Vpiši številko: ").strip()

    if izbira == "0":
        return None

    if izbira.isdigit():
        idx = int(izbira) - 1
        if 0 <= idx < len(kazalniki):
            return kazalniki[idx]

    for k in kazalniki:
        naziv, _, _ = kazalniki_slo.get(k, (k, "", True))
        if izbira.lower() in k.lower() or izbira.lower() in naziv.lower():
            return k

    print("  Kazalnik ni najden.")
    pritisni_enter()
    return None


def meni_drzava():
    pocisti()
    print("\n  PODATKI ZA DRŽAVO")
    drzava = izberi_drzavo()
    if not drzava:
        return

    while True:
        pocisti()
        print(f"\n  {drzava.upper()}\n")
        print("  1  Vsi kazalniki — zadnje leto")
        print("  2  En kazalnik — vsa leta")
        print("  3  Graf — en kazalnik za vsa leta")
        print("  4  Graf — vsi kazalniki za vsa leta")
        print("  0  Nazaj")

        izbira = input("\n  Izbira: ").strip()

        if izbira == "0":
            break

        elif izbira == "1":
            pocisti()
            analiza_drzava(drzava)
            pritisni_enter()

        elif izbira == "2":
            kazalnik = izberi_kazalnik()
            if kazalnik:
                pocisti()
                d = df[
                    (df["country"] == drzava) &
                    (df["indicator"] == kazalnik)
                ].sort_values("year")

                naziv, enota, _ = kazalniki_slo.get(kazalnik, (kazalnik, "", True))
                print(f"\n  {drzava} — {naziv}\n")

                if d.empty:
                    print("  Ni podatkov.")
                else:
                    for _, v in d.iterrows():
                        print(f"  {int(v['year'])}  {v['value']:>10.2f} {enota}")

            pritisni_enter()

        elif izbira == "3":
            kazalnik = izberi_kazalnik()
            if kazalnik:
                graf_kazalnik_ena_drzava(nalozi(), kazalnik, drzava)

        elif izbira == "4":
            graf_vsi_kazalniki(nalozi(), drzava)


def meni_primerjava():
    pocisti()
    print("\n  PRIMERJAVA VSEH DRŽAV")
    kazalnik = izberi_kazalnik()
    if not kazalnik:
        return

    while True:
        pocisti()
        naziv, enota, _ = kazalniki_slo.get(kazalnik, (kazalnik, "", True))
        print(f"\n  {naziv}  [{enota}]\n")
        print("  1  Tekstovna primerjava")
        print("  2  Graf — vse države skozi čas")
        print("  0  Nazaj")

        izbira = input("\n  Izbira: ").strip()

        if izbira == "0":
            break

        elif izbira == "1":
            pocisti()
            analiza_kazalnik(kazalnik)
            pritisni_enter()

        elif izbira == "2":
            graf_kazalnik_vse_drzave(nalozi(), kazalnik)


def meni_scenariji():
    moznosti = {
        "1": "druzina",
        "2": "mladi",
        "3": "pokoj",
    }

    while True:
        pocisti()
        print("\n  ISKALNIK NAJBOLJŠE DRŽAVE\n")
        print("  1  Najboljša država za družino")
        print("  2  Najboljša država za mlade")
        print("  3  Najboljša država za upokojence")
        print("  0  Nazaj")

        izbira = input("\n  Izbira: ").strip()

        if izbira == "0":
            break

        kljuc = moznosti.get(izbira)

        if kljuc:
            pocisti()
            analiza_scenarij(kljuc)
            pritisni_enter()
        else:
            print("\n  Neveljavna izbira.")
            pritisni_enter()


def glavni_meni():
    while True:
        pocisti()
        print("\n  ANALIZA EVROPSKIH DRŽAV")
        print(f"  Države: {', '.join(sorted(df['country'].unique()))}")
        print(f"  Obdobje: {df['year'].min()}–{df['year'].max()}\n")
        print("  1  Podatki za posamezno državo")
        print("  2  Primerjava vseh držav za izbrani kazalnik")
        print("  3  Iskalnik najboljše države za družino, mlade ali upokojence")
        print("  0  Izhod")

        izbira = input("\n  Izbira: ").strip()

        if izbira == "1":
            meni_drzava()
        elif izbira == "2":
            meni_primerjava()
        elif izbira == "3":
            meni_scenariji()
        elif izbira == "0":
            print("\n  Konec analize.\n")
            break


if __name__ == "__main__":
    glavni_meni()