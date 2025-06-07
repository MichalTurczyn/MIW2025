from itertools import combinations

dane = []
with open("pliki/values.txt", "r") as plik:
    for linia in plik:
        dane.append(linia.strip().split())

wiersze = len(dane)
kolumny = len(dane[0])

atrybuty = [f"a{kol + 1}" for kol in range(kolumny - 1)]


def pobierz_wartosc_atrybutu(indeks_obiektu, nazwa_atrybutu):
    indeks_atrybutu = int(nazwa_atrybutu[1:]) - 1
    return dane[indeks_obiektu][indeks_atrybutu]


def formatuj_kombinacje_z_wartosciami(kombinacja, indeks_obiektu):
    sformatowane_atrybuty = []
    for atr in kombinacja:
        wartosc = pobierz_wartosc_atrybutu(indeks_obiektu, atr)
        sformatowane_atrybuty.append(f"{atr} = {wartosc}")
    return "(" + " ∧ ".join(sformatowane_atrybuty) + ")"


def utworz_macierz_nierozroznialnosci():
    macierz_niero = {}

    for o in range(wiersze):
        decyzja = dane[o][-1]
        macierz_niero[f"o{o + 1}"] = {}

        for w in range(wiersze):
            if dane[w][-1] == decyzja:
                macierz_niero[f"o{o + 1}"][f"o{w + 1}"] = "-"
            else:
                deskryptory = []
                for kol in range(kolumny - 1):
                    if dane[o][kol] == dane[w][kol]:
                        deskryptory.append(f"a{kol + 1}")
                macierz_niero[f"o{o + 1}"][f"o{w + 1}"] = deskryptory

    return macierz_niero


def pokaz_macierz_nierozroznialnosci(macierz_niero):
    print("Macierz nierozróżnialności:")
    for klucz, wartosc in macierz_niero.items():
        print(f"{klucz}: {wartosc}")


def wyczerpujace_wg_stopnia(macierz_niero):
    finalne_reguly = {}

    for klucz_obiektu, relacje in macierz_niero.items():
        indeks_obiektu = int(klucz_obiektu[1:]) - 1
        decyzja_obiektu = dane[indeks_obiektu][-1]

        niepozadane_kombinacje = set()
        for klucz_obiektu_powiazanego, deskryptory in relacje.items():
            if deskryptory != '-' and deskryptory:
                for r in range(1, len(deskryptory) + 1):
                    for komb in combinations(deskryptory, r):
                        niepozadane_kombinacje.add(frozenset(komb))

        charakterystyczne_kombinacje_dla_obiektu = set()

        for stopien_nr in range(1, len(atrybuty) + 1):
            for komb in combinations(atrybuty, stopien_nr):
                zamrozona_komb = frozenset(komb)

                jest_charakterystyczna = True
                for niep_komb in niepozadane_kombinacje:
                    if zamrozona_komb.issubset(niep_komb):
                        jest_charakterystyczna = False
                        break

                if jest_charakterystyczna:
                    charakterystyczne_kombinacje_dla_obiektu.add(zamrozona_komb)

        minimalne_charakterystyczne_kombinacje = set()
        for c1 in charakterystyczne_kombinacje_dla_obiektu:
            jest_minimalna = True
            for c2 in charakterystyczne_kombinacje_dla_obiektu:
                if c1 != c2 and c2.issubset(c1):
                    jest_minimalna = False
                    break
            if jest_minimalna:
                minimalne_charakterystyczne_kombinacje.add(c1)

        for min_komb_zamrozony in minimalne_charakterystyczne_kombinacje:
            min_komb_krotka = tuple(sorted(list(min_komb_zamrozony)))
            sformatowana_regula_str = formatuj_kombinacje_z_wartosciami(min_komb_krotka, indeks_obiektu)

            klucz_czesci_decyzyjnej = (sformatowana_regula_str, decyzja_obiektu)

            if klucz_czesci_decyzyjnej not in finalne_reguly:
                finalne_reguly[klucz_czesci_decyzyjnej] = set()
            finalne_reguly[klucz_czesci_decyzyjnej].add(klucz_obiektu)

    reguly_pogrupowane_wg_stopnia = {}

    for (regula_str, wartosc_decyzji), zbior_obiektow in finalne_reguly.items():
        stopien = regula_str.count('a')

        if stopien not in reguly_pogrupowane_wg_stopnia:
            reguly_pogrupowane_wg_stopnia[stopien] = set()

        liczba_wsparcia = len(zbior_obiektow)
        sformatowana_czesc_decyzyjna = f"(d={wartosc_decyzji})[{liczba_wsparcia}]"

        reguly_pogrupowane_wg_stopnia[stopien].add(f"  [{regula_str}] => {sformatowana_czesc_decyzyjna}")

    for stopien in sorted(reguly_pogrupowane_wg_stopnia.keys()):
        nazwa_stopnia = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"][stopien - 1] if stopien <= 10 else str(stopien)
        print(f"\n---")
        print(f"## Rząd {nazwa_stopnia} ({stopien} atrybut{'y' if 1 < stopien < 5 else 'ów' if stopien >= 5 else ''}):")

        for wyjscie_reguly_str in sorted(list(reguly_pogrupowane_wg_stopnia[stopien])):
            print(wyjscie_reguly_str)


macierz_nier = utworz_macierz_nierozroznialnosci()
pokaz_macierz_nierozroznialnosci(macierz_nier)
wyczerpujace_wg_stopnia(macierz_nier)