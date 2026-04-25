import requests
import pandas as pd
import time

# države ki jih primerjamo
drzave = ["SI", "AT", "HR", "HU", "IT", "CZ", "SK", "DE"]

# slovenska imena držav
imena_drzav = {
    "SI": "Slovenija",
    "AT": "Avstrija",
    "HR": "Hrvaška",
    "HU": "Madžarska",
    "IT": "Italija",
    "CZ": "Češka",
    "SK": "Slovaška",
    "DE": "Nemčija",
}

# kazalniki: ime v csv in koda na world bank
kazalniki = {
    "gdp_per_capita":     "NY.GDP.PCAP.CD",
    "life_expectancy":    "SP.DYN.LE00.IN",
    "internet_users":     "IT.NET.USER.ZS",
    "infant_mortality":   "SP.DYN.IMRT.IN",
    "unemployment":       "SL.UEM.TOTL.ZS",
    "youth_unemployment": "SL.UEM.1524.ZS",
    "inflation":          "FP.CPI.TOTL.ZG",
    "fertility_rate":     "SP.DYN.TFRT.IN",
}

zacetno_leto = 2000
koncno_leto  = 2023
izhodna_dat  = "world_bank_data.csv"


def prenesi_kazalnik(koda_drzave, koda_kazalnika):
    url = (
        f"https://api.worldbank.org/v2/country/{koda_drzave}"
        f"/indicator/{koda_kazalnika}"
        f"?format=json&per_page=1000"
    )
    try:
        odgovor = requests.get(url, timeout=60)
        odgovor.raise_for_status()
        podatki = odgovor.json()

        if not isinstance(podatki, list) or len(podatki) < 2:
            return []
        if podatki[1] is None:
            return []

        return podatki[1]

    except Exception as e:
        print(f"    napaka: {e}")
        return []


def main():
    print("Prenos podatkov — World Bank API")
    print(f"Države: {', '.join(imena_drzav.values())}")
    print(f"Obdobje: {zacetno_leto}–{koncno_leto}\n")

    vrstice = []

    for koda in drzave:
        ime = imena_drzav[koda]
        print(f"{ime}")

        for ime_kaz, koda_kaz in kazalniki.items():
            print(f"  {ime_kaz} ...", end=" ", flush=True)

            zapisi = prenesi_kazalnik(koda, koda_kaz)
            stevilo = 0

            for zapis in zapisi:
                if zapis["value"] is None:
                    continue

                try:
                    leto = int(zapis["date"])
                except ValueError:
                    continue

                if not (zacetno_leto <= leto <= koncno_leto):
                    continue

                vrstice.append({
                    "country":   ime,
                    "year":      leto,
                    "indicator": ime_kaz,
                    "value":     zapis["value"],
                })
                stevilo += 1

            print(f"({stevilo} let)")
            time.sleep(0.3)

    if not vrstice:
        print("\nNi podatkov za shraniti.")
        return

    df = pd.DataFrame(vrstice)
    df.to_csv(izhodna_dat, index=False, encoding="utf-8-sig")
    print(f"\nShranjeno: {izhodna_dat}")


if __name__ == "__main__":
    main()