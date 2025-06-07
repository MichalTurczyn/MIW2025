from itertools import combinations, chain
from collections import defaultdict

def wczytaj_dane(nazwa_pliku):
    with open(nazwa_pliku, 'r', encoding='utf-8') as f:
        return [set(linia.strip().split(',')) for linia in f if linia.strip()]

def policz_wystapienia(transakcje_lista, kandydaci_zbiory):
    licznik_wystapien = defaultdict(int)
    for transakcja in transakcje_lista:
        for kandydat_zbior in kandydaci_zbiory:
            if kandydat_zbior.issubset(transakcja):
                licznik_wystapien[frozenset(kandydat_zbior)] += 1
    return licznik_wystapien

def odfiltruj_czeste(licznik_wystapien, prog_minimalny):
    return {zbior for zbior, liczba in licznik_wystapien.items() if liczba >= prog_minimalny}

def wygeneruj_kandydatow(poprzednie_zbiory_czeste, rozmiar_zbioru):
    elementy_unikalne = set(chain.from_iterable(poprzednie_zbiory_czeste))
    return [set(x) for x in combinations(elementy_unikalne, rozmiar_zbioru)]

def wygeneruj_reguly_asocjacyjne(zbiory_czeste, transakcje_lista, prog_jakosci_reguly):
    liczba_transakcji = len(transakcje_lista)
    lista_regul = []
    mapa_wsparcia = {}
    for zbior in zbiory_czeste:
        mapa_wsparcia[zbior] = sum(1 for t in transakcje_lista if zbior.issubset(t)) / liczba_transakcji

    for zbior_calkowity in zbiory_czeste:
        if len(zbior_calkowity) < 2:
            continue
        for i in range(1, len(zbior_calkowity)):
            for poprzednik_kandydat in combinations(zbior_calkowity, i):
                poprzednik = frozenset(poprzednik_kandydat)
                nastepnik = zbior_calkowity - poprzednik
                if not nastepnik:
                    continue
                wsparcie_reguly = mapa_wsparcia[zbior_calkowity]
                ufnosc_reguly = wsparcie_reguly / mapa_wsparcia.get(poprzednik, 1e-10)
                jakosc_reguly = wsparcie_reguly * ufnosc_reguly
                if jakosc_reguly >= prog_jakosci_reguly:
                    lista_regul.append((poprzednik, nastepnik, round(wsparcie_reguly, 3), round(ufnosc_reguly, 3), round(jakosc_reguly, 3)))
    return lista_regul

def algorytm_apriori(transakcje_lista, prog_czestosci_min=2, prog_jakosci_min=1/3):
    zbior_czestych_elementow = []
    aktualny_rozmiar = 1

    kandydaci_rozmiar_1 = [set([element]) for element in set(chain.from_iterable(transakcje_lista))]
    while True:
        licznik_dla_kandydatow = policz_wystapienia(transakcje_lista, kandydaci_rozmiar_1)
        czeste_z_filtracji = odfiltruj_czeste(licznik_dla_kandydatow, prog_czestosci_min)
        if not czeste_z_filtracji:
            break
        zbior_czestych_elementow.extend(czeste_z_filtracji)
        aktualny_rozmiar += 1
        kandydaci_rozmiar_1 = wygeneruj_kandydatow(czeste_z_filtracji, aktualny_rozmiar)

    reguly_wygenerowane = wygeneruj_reguly_asocjacyjne(zbior_czestych_elementow, transakcje_lista, prog_jakosci_min)
    return zbior_czestych_elementow, reguly_wygenerowane

if __name__ == '__main__':
    sciezka_do_pliku = 'pliki/paragony.txt'
    transakcje = wczytaj_dane(sciezka_do_pliku)
    czeste_zbiory_wynik, reguly_wynik = algorytm_apriori(transakcje, prog_czestosci_min=2, prog_jakosci_min=1/3)

    print("\nCZĘSTE ZBIORY (z częstościami):")
    calkowita_liczba_transakcji = len(transakcje)
    for zbior in czeste_zbiory_wynik:
        liczba_wystapien = sum(1 for t in transakcje if zbior.issubset(t))
        print(f"{set(zbior)} → wystąpień: {liczba_wystapien}, wsparcie: {round(liczba_wystapien / calkowita_liczba_transakcji, 3)}")

    print("\nREGUŁY ASOCJACYJNE:")
    for poprzednik, nastepnik, wsparcie_wartosc, ufnosc_wartosc, jakosc_wartosc in reguly_wynik:
        print(f"{set(poprzednik)} => {set(nastepnik)} | wsparcie={wsparcie_wartosc}, ufność={ufnosc_wartosc}, jakość={jakosc_wartosc}")