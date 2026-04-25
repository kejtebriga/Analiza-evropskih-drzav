# Analiza evropskih držav

## Opis projekta

Projekt analizira 8 evropskih držav na podlagi podatkov iz World Bank API za obdobje 2000–2023.

V projektu primerjamo naslednje kazalnike:
- BDP na prebivalca,
- pričakovano življenjsko dobo,
- stopnjo brezposelnosti,
- brezposelnost mladih,
- delež internetnih uporabnikov,
- stopnjo inflacije,
- umrljivost dojenčkov,
- stopnjo rodnosti.

Podatke najprej pridobimo iz World Bank API. Program za vsako državo in vsak kazalnik pošlje zahtevo na API, prejme podatke v obliki JSON, iz njih izbere leto, vrednost, državo in kazalnik ter jih shrani v datoteko `world_bank_data.csv`.

Nato se podatki iz CSV datoteke preberejo v programu in uporabijo za analizo, primerjave ter prikaz grafov.

Cilj projekta je omogočiti pregled ključnih kazalnikov za posamezno državo, primerjavo držav med seboj ter izbiro najboljše države glede na različne življenjske situacije.
## Namestitev 

```bash
pip install requests pandas matplotlib scikit-learn
```

## Zagon 

Program zaženemo v dveh korakih:

1. Prenesemo podatke iz World Bank:
   python pridobi_podatke.py

2. Zaženemo program:
   python tekstovni_vmesnik.py

---

## Struktura projekta

```
├── pridobi_podatke.py   # prenos podatkov iz World Bank API, ki se shranijo v CSV
├── analiza.py           # obdelava podatkov, izračun scenarijev
├── vizualizacija.py     # risanje grafov z matplotlib
├── tekstovni_vmesnik.py # tekstovni uporabniški vmesnik
└── world_bank_data.csv  # preneseni podatki 
```
## Tekstovni vmesnik

Program deluje kot tekstovni vmesnik, kjer uporabnik izbira med različnimi možnostmi.

Uporabnik lahko:

### 1. Analizira posamezno državo
- vidi vse kazalnike za zadnje leto (2023),
- vidi en kazalnik za vsa leta,
- ter prikaže grafe (en kazalnik vsa leta ali vsi kazalniki za vsa leta).

### 2. Primerja države
- izbere en kazalnik (npr. BDP ali brezposelnost),
- in vidi razvrstitev vseh držav glede na povprečno vrednost kazalnika v celotnem obdobju ali graf, ki kaže spreminjanje vrednosti kazalnika skozi leta.

### 3. Uporabi scenarije
- program izbere najboljšo državo za družino, mlade ali upokojence

## Razlaga scenarijev 

Scenariji nam pomagajo izbrati državo, ki je najbolj primerna za življenje
- za družino,
- za mlade,
- za upokojence.

Pri tem uporabimo podatke več različnih kazalnikov, ki skupaj bolje opisujejo kakovost življenja.
Vsak kazalnik pa smiselno utežimo, saj nimajo vsi enakega vpliva.

### Izbira kazalnikov

Kazalniki so izbrani glede na smiselnost za posamezen scenarij:

- **Družina**
  - življenjska doba → kakovost zdravstva
  - umrljivost dojenčkov → varnost otrok
  - brezposelnost mladih → prihodnost otrok
  - BDP → življenjski standard

- **Mladi**
  - brezposelnost mladih → možnosti zaposlitve
  - BDP → plače in življenjski standard
  - internet → dostop do tehnologije

- **Upokojenci**
  - življenjska doba → zdravje
  - inflacija → stabilnost cen
  - BDP → standard
  - umrljivost → kakovost zdravstva



### Vloga uteži

Uteži določajo, kako pomemben je posamezen kazalnik v scenariju.

Na primer:
- pri družini sta bolj pomembna zdravje in varnost,
- pri mladih so pomembnejše zaposlitvene možnosti,
- pri upokojencih pa stabilnost in inflacija.

Zato imajo kazalniki različne uteži.

Brez uteži bi vsi kazalniki vplivali enako.


### Postopek izračuna

Za vsak scenarij izračun poteka v več korakih:

1. **Povprečje skozi čas**
   Za vsako državo izračunamo povprečje kazalnikov v obdobju 2000–2023.
   S tem zmanjšamo vpliv posameznih let.

2. **Upoštevanje smeri kazalnikov**
   Nekateri kazalniki so boljši, če so višji (npr. BDP),
   drugi pa, če so nižji (npr. brezposelnost).
   Zato vrednosti po potrebi obrnemo.

3. **Normalizacija**
   Ker imajo kazalniki različne enote (USD, %, leta),
   jih pretvorimo na skupno lestvico od 0 do 1.

4. **Uteženo povprečje**
   Vsak kazalnik prispeva k rezultatu glede na svojo pomembnost (utež).

## Vir podatkov

World Bank Open Data: https://data.worldbank.org/

---
