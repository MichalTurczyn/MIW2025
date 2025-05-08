import numpy as np
from collections import Counter
from itertools import combinations


def load_data():
    return np.array([
        [1, 1, 1, 1, 3, 1, 1],
        [1, 1, 1, 1, 3, 2, 1],
        [1, 1, 1, 3, 2, 1, 0],
        [1, 1, 1, 3, 3, 2, 1],
        [1, 1, 2, 1, 2, 1, 0],
        [1, 1, 2, 1, 2, 2, 1],
        [1, 1, 2, 2, 3, 1, 0],
        [1, 1, 2, 2, 4, 1, 1]
    ])


def compute_indiscernibility_matrix(data):
    n, m = data.shape
    m -= 1  # Ostatnia kolumna to decyzja
    matrix = np.full((n, n), None, dtype=object)  # Inicjalizujemy macierz jako None

    for i in range(n):
        for j in range(i + 1, n):  # Symetryczna macierz
            if data[i, -1] != data[j, -1]:  # Tylko jeśli decyzje są różne
                common_attrs = [f"a{idx + 1}" for idx in range(m) if data[i, idx] == data[j, idx]]
                matrix[i, j] = matrix[j, i] = common_attrs if common_attrs else []

    return matrix


def find_missing_attributes(matrix, data):
    """Znajduje atrybuty, które nie są obecne w danej kolumnie macierzy"""
    n = len(matrix)
    all_attributes = {f"a{i + 1}" for i in range(6)}  # Atrybuty od a1 do a6
    missing_attributes = {f"o{i + 1}": set(all_attributes) for i in range(n)}  # Inicjalizujemy zestawy atrybutów

    for j in range(n):
        present_attrs = set()
        for i in range(n):
            if matrix[i, j] is not None and matrix[i, j] != []:  # Jeśli nie jest pustą kratką
                present_attrs.update(matrix[i, j])

        # Usuwamy z zestawu obecnych atrybutów te, które się pojawiły
        missing_attributes[f"o{j + 1}"] -= present_attrs

    # Zwracamy brakujące atrybuty z wartościami i decyzją
    missing_data = {}
    for obj, attrs in missing_attributes.items():
        if attrs:
            missing_data[obj] = []
            obj_index = int(obj[1:]) - 1
            for attr in attrs:
                attr_index = int(attr[1:]) - 1
                value = data[obj_index, attr_index]
                decision = data[obj_index, -1]  # Ostatnia kolumna to decyzja
                missing_data[obj].append((attr, value, decision))

    return missing_data


def generate_first_order_rules(missing_data):
    """Generuje reguły I rzędu z pojedynczych brakujących atrybutów"""
    rules = []
    for obj, attributes in missing_data.items():
        for attr, value, decision in attributes:
            rule = f"({attr} = {value}) => (d = {decision})"
            rules.append(rule)
    return rules


def generate_second_order_rules(matrix, data, missing_data, first_order_rules):
    """Generuje reguły II rzędu na podstawie kombinacji brakujących atrybutów"""
    rules = []

    # Przekształć reguły I rzędu w zbiór pojedynczych atrybutów
    first_order_attr_combinations = {tuple(rule.split(") =")[0].strip("()").split(" ∧ ")) for rule in first_order_rules}

    for obj, attributes in missing_data.items():
        # Generowanie kombinacji atrybutów długości 2
        attr_combinations = combinations(attributes, 2)
        for combo in attr_combinations:
            attr1, value1, _ = combo[0]
            attr2, value2, _ = combo[1]

            # Sprawdzamy, czy para już istnieje w regułach I rzędu
            if (attr1, attr2) in first_order_attr_combinations or (attr2, attr1) in first_order_attr_combinations:
                continue  # Pomijamy kombinacje, które już występują w regułach I rzędu

            # Sprawdzamy, czy para atrybutów istnieje w macierzy nieodróżnialności
            for i in range(len(matrix)):
                for j in range(i + 1, len(matrix)):
                    if matrix[i, j] is not None:  # Jeśli jest lista atrybutów w tej komórce
                        if {attr1, attr2}.issubset(matrix[i, j]):  # Jeżeli para atrybutów jest wspólna
                            rule = f"({attr1} = {value1}) ∧ ({attr2} = {value2}) => (d = {data[i, -1]})"
                            rules.append(rule)

    return rules


def count_rule_support(rules):
    """Liczy support (liczba powtórzeń) reguł"""
    rule_counts = Counter(rules)
    return rule_counts


def print_rules_with_support(rule_counts):
    """Wypisuje reguły z supportem"""
    for rule, count in rule_counts.items():
        print(f"{rule} [{count}]")


# Główna logika
data = load_data()
matrix = compute_indiscernibility_matrix(data)

missing_data = find_missing_attributes(matrix, data)

# Generujemy reguły I rzędu
first_order_rules = generate_first_order_rules(missing_data)

# Generujemy reguły II rzędu
second_order_rules = generate_second_order_rules(matrix, data, missing_data, first_order_rules)

# Liczymy support reguł II rzędu
second_order_rule_counts = count_rule_support(second_order_rules)

# Wyświetlamy reguły I rzędu
print("\nReguły I rzędu:")
rule_counts_first = count_rule_support(first_order_rules)
print_rules_with_support(rule_counts_first)

# Wyświetlamy reguły II rzędu z liczbą powtórzeń
print("\nReguły II rzędu:")
print_rules_with_support(second_order_rule_counts)
