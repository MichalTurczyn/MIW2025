def algorytm_lem2(dane, nazwy_atrybutow):
    obiekty = dane[1:]
    atrybuty_warunkowe = [wiersz[:-2] for wiersz in obiekty]
    decyzje = [wiersz[-2] for wiersz in obiekty]
    identyfikatory_obiektow = [wiersz[-1] for wiersz in obiekty]

    klasy_decyzyjne = {}
    for indeks, decyzja in enumerate(decyzje):
        if decyzja not in klasy_decyzyjne:
            klasy_decyzyjne[decyzja] = []
        klasy_decyzyjne[decyzja].append(indeks)

    reguly = []
    pokryte_obiekty = set()

    for decyzja, indeksy_klasy in klasy_decyzyjne.items():
        niepokryte_w_klasie = [i for i in indeksy_klasy if i not in pokryte_obiekty]

        while niepokryte_w_klasie:
            licznik_deskryptorow = {}
            for indeks_atrybutu in range(len(nazwy_atrybutow)):
                for indeks_obiektu in niepokryte_w_klasie:
                    wartosc = atrybuty_warunkowe[indeks_obiektu][indeks_atrybutu]
                    klucz = (indeks_atrybutu, wartosc)
                    licznik_deskryptorow[klucz] = licznik_deskryptorow.get(klucz, 0) + 1

            najlepszy_deskryptor = None
            maks_licznik = 0
            for (indeks_atrybutu, wartosc), liczba in licznik_deskryptorow.items():
                if liczba > maks_licznik or (liczba == maks_licznik and najlepszy_deskryptor is None):
                    maks_licznik = liczba
                    najlepszy_deskryptor = (indeks_atrybutu, wartosc)

            if not najlepszy_deskryptor:
                break

            indeks_atrybutu, najlepsza_wartosc = najlepszy_deskryptor
            pasujace_obiekty = set()
            for i in range(len(obiekty)):
                if atrybuty_warunkowe[i][indeks_atrybutu] == najlepsza_wartosc:
                    pasujace_obiekty.add(i)

            spojna = True
            for indeks_obiektu in pasujace_obiekty:
                if decyzje[indeks_obiektu] != decyzja:
                    spojna = False
                    break

            if spojna:
                warunki_reguly = [najlepszy_deskryptor]
                pokrycie_reguly = pasujace_obiekty & set(niepokryte_w_klasie)
                reguly.append({
                    'warunki': warunki_reguly,
                    'decyzja': decyzja,
                    'pokrycie': len(pokrycie_reguly),
                    'obiekty': [identyfikatory_obiektow[i] for i in pokrycie_reguly]
                })
                pokryte_obiekty.update(pokrycie_reguly)
                niepokryte_w_klasie = [i for i in indeksy_klasy if i not in pokryte_obiekty]
            else:
                biezace_obiekty = pasujace_obiekty & set(niepokryte_w_klasie)
                warunki_reguly = [najlepszy_deskryptor]

                while True:
                    kolejny_deskryptor = None
                    maks_licznik = 0
                    tymczasowe_liczniki = {}
                    for indeks_obiektu in biezace_obiekty:
                        for indeks_atrybutu in range(len(nazwy_atrybutow)):
                            if any(warunek[0] == indeks_atrybutu for warunek in warunki_reguly):
                                continue
                            wartosc = atrybuty_warunkowe[indeks_obiektu][indeks_atrybutu]
                            klucz = (indeks_atrybutu, wartosc)
                            tymczasowe_liczniki[klucz] = tymczasowe_liczniki.get(klucz, 0) + 1

                    for (indeks_atrybutu, wartosc), liczba in tymczasowe_liczniki.items():
                        if liczba > maks_licznik or (liczba == maks_licznik and kolejny_deskryptor is None):
                            maks_licznik = liczba
                            kolejny_deskryptor = (indeks_atrybutu, wartosc)

                    if not kolejny_deskryptor:
                        break

                    warunki_reguly.append(kolejny_deskryptor)

                    aktualne_dopasowanie = set(range(len(obiekty)))
                    for indeks_atrybutu, wartosc in warunki_reguly:
                        dopasowanie = set()
                        for i in range(len(obiekty)):
                            if atrybuty_warunkowe[i][indeks_atrybutu] == wartosc:
                                dopasowanie.add(i)
                        aktualne_dopasowanie = aktualne_dopasowanie & dopasowanie

                    spojna = True
                    for indeks_obiektu in aktualne_dopasowanie:
                        if decyzje[indeks_obiektu] != decyzja:
                            spojna = False
                            break

                    if spojna:
                        pokrycie_reguly = aktualne_dopasowanie & set(niepokryte_w_klasie)
                        reguly.append({
                            'warunki': warunki_reguly,
                            'decyzja': decyzja,
                            'pokrycie': len(pokrycie_reguly),
                            'obiekty': [identyfikatory_obiektow[i] for i in pokrycie_reguly]
                        })
                        pokryte_obiekty.update(pokrycie_reguly)
                        niepokryte_w_klasie = [i for i in indeksy_klasy if i not in pokryte_obiekty]
                        break
                    else:
                        biezace_obiekty = aktualne_dopasowanie & set(niepokryte_w_klasie)

    return reguly


def wypisz_reguly(reguly, nazwy_atrybutow):
    print("Reguły:")
    for i, regula in enumerate(reguly, 1):
        warunki = regula['warunki']
        decyzja = regula['decyzja']
        pokrycie = regula['pokrycie']
        obiekty = regula['obiekty']

        warunki_str = " ∧ ".join([f"({nazwy_atrybutow[atrybut]}={wartosc})" for atrybut, wartosc in warunki])
        print(f"Reguła {i}")
        print(f"{warunki_str} =⇒ (d={decyzja})", end="")
        if pokrycie > 1:
            print(f"[{pokrycie}]")
        else:
            print()
        print(f"   (obiekty: {', '.join(obiekty)})\n")


def wczytaj_dane_z_pliku(nazwa_pliku):
    dane = []
    with open(nazwa_pliku, 'r') as plik:
        pierwsza_linia = [int(x) for x in plik.readline().strip().split()]

        liczba_atrybutow_warunkowych = len(pierwsza_linia) - 1

        naglowek = [f'a{i + 1}' for i in range(liczba_atrybutow_warunkowych)] + ['decyzja', 'obiekt_id']
        dane.append(naglowek)

        identyfikator_1 = f"o{1}"
        dane.append(pierwsza_linia[:-1] + [pierwsza_linia[-1], identyfikator_1])

        for i, linia in enumerate(plik, start=2):
            wartosci = [int(x) for x in linia.strip().split()]
            identyfikator = f"o{i}"
            dane.append(wartosci[:-1] + [wartosci[-1], identyfikator])
    return dane


nazwa_pliku = 'pliki/values.txt'
dane = wczytaj_dane_z_pliku(nazwa_pliku)

nazwy_atrybutow = dane[0][:-2]

reguly = algorytm_lem2(dane, nazwy_atrybutow)
wypisz_reguly(reguly, nazwy_atrybutow)
