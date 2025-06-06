from sklearn.datasets import load_iris
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter

# Załadowanie danych
iris = load_iris()
X = iris.data
y = iris.target

# Podział na dane treningowe i testowe
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)


# 1. Metryka euklidesowa
def euklidean_distance(x1, x2):
    return np.sqrt(np.sum((x1 - x2) ** 2))


# 2. Metryka Manhattan
def manhattan_distance(x1, x2):
    return np.sum(np.abs(x1 - x2))


# 3. Metryka cosinusowa
def cosine_similarity(x1, x2):
    dot_product = np.dot(x1, x2)
    norm_x1 = np.linalg.norm(x1)
    norm_x2 = np.linalg.norm(x2)
    return 1 - dot_product / (norm_x1 * norm_x2)  # Dystans to 1 - cosinus


# Funkcja klasyfikatora KNN
def knn_classifier(X_train, y_train, X_test, k, metric_fn):
    predictions = []

    for test_point in X_test:
        # Obliczamy odległości od punktu testowego do wszystkich punktów treningowych
        distances = []
        for i, train_point in enumerate(X_train):
            distance = metric_fn(test_point, train_point)
            distances.append((distance, i))

        # Sortowanie według odległości
        distances.sort(key=lambda x: x[0])

        # Wybór k najbliższych sąsiadów
        nearest_neighbors = [y_train[i] for _, i in distances[:k]]

        # Najczęstsza klasa wśród k sąsiadów
        most_common_class = Counter(nearest_neighbors).most_common(1)[0][0]
        predictions.append(most_common_class)

    return predictions


# Funkcja do obliczania dokładności
def accuracy(y_true, y_pred):
    return np.mean(np.array(y_true) == np.array(y_pred))


# Testowanie klasyfikatora z różnymi metrykami
k = 3

# Euklidesowa
y_pred_euclid = knn_classifier(X_train, y_train, X_test, k, euklidean_distance)
accuracy_euclid = accuracy(y_test, y_pred_euclid)
print(f"Accuracy with Euclidean distance: {accuracy_euclid:.4f}")

# Manhattan
y_pred_manhattan = knn_classifier(X_train, y_train, X_test, k, manhattan_distance)
accuracy_manhattan = accuracy(y_test, y_pred_manhattan)
print(f"Accuracy with Manhattan distance: {accuracy_manhattan:.4f}")

# Cosinus
y_pred_cosine = knn_classifier(X_train, y_train, X_test, k, cosine_similarity)
accuracy_cosine = accuracy(y_test, y_pred_cosine)
print(f"Accuracy with Cosine similarity: {accuracy_cosine:.4f}")
