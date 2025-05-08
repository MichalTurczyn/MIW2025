from collections import defaultdict

d = [
    ['kapusta', 'ogorki', 'pomidory', 'kabaczki'],
    ['ogorki', 'pomidory', 'kabaczki'],
    ['cytryny', 'pomidory', 'woda'],
    ['cytryny', 'woda', 'jajka'],
    ['ogorki', 'grzybki', 'zoladkowa'],
    ['zoladkowa', 'ogorki', 'pomidory']
]

prog = 2
licznik_produktow = defaultdict(int)

for paragon in d:
    for produkt in paragon:
        licznik_produktow[produkt] += 1

f1_czeste_produkty = set()
for key in licznik_produktow:
    if licznik_produktow.get(key) >= prog:
        f1_czeste_produkty.add(key)

# z kombinacji bez powtorezn zbioru f1 tworzymy zbior c2
c2 = set()

licznik=0
for idx1 in len(licznik_produktow-1):
    for produkt2 in f1_czeste_produkty:
        c2.add((produkt1, produkt2))

