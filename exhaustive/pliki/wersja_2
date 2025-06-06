from itertools import combinations

"""
Otwieranie pliku w formacie txt i przekształcanie na macierz tab.
:return: tab, rows, columns, args
"""
tab = []
with open("pliki/values.txt", "r") as file:
    for line in file:
        tab.append(line.strip().split())

rows = len(tab)
columns = len(tab[0])

args = [f"a{col + 1}" for col in range(columns - 1)]



def create_ind_matrix():
    """
    Tworzenie macierzy nieodroznialnosci z tab[].
    :return: ind_matrix
    """
    ind_matrix = {}

    for o in range(rows):
        d = tab[o][-1]
        ind_matrix[f"o{o + 1}"] = {}

        for row in range(rows):
            if tab[row][-1] == d:
                ind_matrix[f"o{o + 1}"][f"o{row + 1}"] = "-"

            else:
                descriptors = []
                for col in range(columns - 1):
                    if tab[o][col] == tab[row][col]:
                        descriptors.append(f"a{col + 1}")
                        ind_matrix[f"o{o + 1}"][f"o{row + 1}"] = descriptors

    return ind_matrix


def show_ind_matrix(ind_matrix):
    print("Macierz nierozróżnialności:")
    for key, value in ind_matrix.items():
        print(f"{key}: {value}")


def exhaustive(ind_matrix):
    for key, value in ind_matrix.items():
        print(f"\nDla {key}:")
        prev_combinations = set()

        for rank in range(1, rows + 1):
            print(f"Reguly {rank} rzedu:")
            all_combinations = set(combinations(args, rank))
            existing_combinations = set()

            for sub_key, sub_value in value.items():
                if sub_value != '-':
                    row_combinations = set(combinations(sub_value, rank))
                    existing_combinations.update(row_combinations)

            missing_combinations = all_combinations - existing_combinations

            """ Tu dodać pobieranie atrybutów tzn a2 = 2 itd"""
            delete_prev_combinations = set()

            for comb in missing_combinations:
                has_subset = False

                for prev_comb in prev_combinations:
                    if set(prev_comb).issubset(set(comb)):
                        has_subset = True
                        break

                if not has_subset:
                    delete_prev_combinations.add(comb)

            prev_combinations = missing_combinations
            print(delete_prev_combinations, end="")
            print("")



ind_matrix = create_ind_matrix()
show_ind_matrix(ind_matrix)
exhaustive(ind_matrix)