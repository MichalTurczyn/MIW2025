import numpy as np
from itertools import combinations


def znajdz_reguly_1_rzedu(atrybuty, decyzje):
    reguly_1 = []
    atrybuty_uzyte_w_regulach_1_rzedu = set()
    pokryte_obiekty = set()

    for i in range(atrybuty.shape[0]):
        if i in pokryte_obiekty:
            continue

        for kolumna in range(atrybuty.shape[1]):
            wartosc = atrybuty[i, kolumna]
            maska = atrybuty[:, kolumna] == wartosc
            decyzje_w_grupie = np.unique(decyzje[maska])
            if len(decyzje_w_grupie) == 1:
                reguly_1.append((i, kolumna, wartosc, decyzje_w_grupie[0]))
                atrybuty_uzyte_w_regulach_1_rzedu.add((kolumna, wartosc))
                pokryte_obiekty.update(np.where(maska)[0])
                break

    return reguly_1, atrybuty_uzyte_w_regulach_1_rzedu, pokryte_obiekty


def znajdz_reguly_2_rzedu(atrybuty, decyzje, pokryte_obiekty):
    reguly_2 = []
    num_atrybuty = atrybuty.shape[1]

    for i in range(atrybuty.shape[0]):
        if i in pokryte_obiekty:
            continue

        for kol1, kol2 in combinations(range(num_atrybuty), 2):
            wart1, wart2 = atrybuty[i, kol1], atrybuty[i, kol2]
            maska = (atrybuty[:, kol1] == wart1) & (atrybuty[:, kol2] == wart2)
            decyzje_w_grupie = np.unique(decyzje[maska])
            if len(decyzje_w_grupie) == 1:
                reguly_2.append((i, kol1, wart1, kol2, wart2, decyzje_w_grupie[0]))
                pokryte_obiekty.add(i)
                break

    return reguly_2


data = np.loadtxt("pliki/values.txt")
atrybuty = data[:, :-1]
decyzje = data[:, -1]

reguly_1, atrybuty_uzyte_w_regulach_1_rzedu, pokryte_obiekty = znajdz_reguly_1_rzedu(atrybuty, decyzje)
reguly_2 = znajdz_reguly_2_rzedu(atrybuty, decyzje, pokryte_obiekty)

print("Rząd I:")
for reg in reguly_1:
    kolumna, wartosc = reg[1], reg[2]
    maska = atrybuty[:, kolumna] == wartosc
    liczba = np.sum(maska)
    print(f"o{reg[0] + 1} (a{kolumna + 1}={int(wartosc)}) => d={int(reg[3])} [{liczba}]")

print("\nRząd II:")
for reg in reguly_2:
    kol1, wart1, kol2, wart2 = reg[1], reg[2], reg[3], reg[4]
    maska = (atrybuty[:, kol1] == wart1) & (atrybuty[:, kol2] == wart2)
    liczba = np.sum(maska)
    print(f"o{reg[0] + 1} (a{kol1 + 1}={int(wart1)}) ^ (a{kol2 + 1}={int(wart2)}) => d={int(reg[5])} [{liczba}]")