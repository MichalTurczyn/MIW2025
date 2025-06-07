import math
import matplotlib.pyplot as plt

plik = open("dane_pogoda.txt", encoding="utf-8")
linie = plik.readlines()
plik.close()

kolumny = ["ID", "Pogoda", "Temperatura", "Wilgotność", "Wiatr", "Decyzja"]
dane = []
for linia in linie:
    czesci = linia.strip().split()
    rekord = {}
    for i in range(len(kolumny)):
        rekord[kolumny[i]] = czesci[i]
    dane.append(rekord)

def entropia(przyklady):
    decyzje = [x["Decyzja"] for x in przyklady]
    licznik = {}
    for d in decyzje:
        if d not in licznik:
            licznik[d] = 0
        licznik[d] += 1
    wynik = 0
    for klasa in licznik:
        p = licznik[klasa] / len(przyklady)
        wynik -= p * math.log2(p)
    return wynik

def gain(przyklady, atrybut):
    wartosci = list(set([x[atrybut] for x in przyklady]))
    entropia_pierwotna = entropia(przyklady)
    suma = 0
    for w in wartosci:
        podzbior = [x for x in przyklady if x[atrybut] == w]
        suma += (len(podzbior)/len(przyklady)) * entropia(podzbior)
    return entropia_pierwotna - suma

def id3(przyklady, atrybuty):
    decyzje = [x["Decyzja"] for x in przyklady]
    if decyzje.count(decyzje[0]) == len(decyzje):
        return decyzje[0]
    if len(atrybuty) == 0:
        return max(set(decyzje), key=decyzje.count)

    gainy = {}
    for a in atrybuty:
        gainy[a] = gain(przyklady, a)
    najlepszy = max(gainy, key=gainy.get)

    drzewo = {najlepszy: {}}
    for w in set([x[najlepszy] for x in przyklady]):
        filtr = [x for x in przyklady if x[najlepszy] == w]
        if not filtr:
            drzewo[najlepszy][w] = max(set(decyzje), key=decyzje.count)
        else:
            nowe_atrybuty = [a for a in atrybuty if a != najlepszy]
            drzewo[najlepszy][w] = id3(filtr, nowe_atrybuty)
    return drzewo

def rysuj_drzewo(drzewo, x=0.5, y=1.0, dx=0.2, dy=0.1, poziom=1, rodzic=None):
    if type(drzewo) == str:
        plt.text(x, y, drzewo, ha='center', bbox=dict(boxstyle="round", facecolor="lightgreen"))
        if rodzic:
            plt.plot([rodzic[0], x], [rodzic[1], y], 'k-')
        return
    for atrybut in drzewo:
        plt.text(x, y, atrybut, ha='center', bbox=dict(boxstyle="round", facecolor="lightblue"))
        if rodzic:
            plt.plot([rodzic[0], x], [rodzic[1], y], 'k-')
        mozliwe = list(drzewo[atrybut].keys())
        for i in range(len(mozliwe)):
            w = mozliwe[i]
            nowex = x - dx*(len(mozliwe)-1)/2 + dx*i
            nowey = y - dy
            plt.text((x + nowex)/2, (y + nowey)/2 + 0.01, w, ha='center', fontsize=9)
            rysuj_drzewo(drzewo[atrybut][w], nowex, nowey, dx/1.5, dy, poziom+1, (x, y))


atrybuty = ["Pogoda", "Temperatura", "Wilgotność", "Wiatr"]
drzewo = id3(dane, atrybuty)

plt.figure(figsize=(10, 6))
rysuj_drzewo(drzewo)
plt.axis('off')
plt.title("Drzewo Decyzyjne (ID3) - styl studencki")
plt.show()
