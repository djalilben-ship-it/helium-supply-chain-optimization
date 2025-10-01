# src/topsis.py
import numpy as np

def topsis(matrix, weights, impacts):
    """TOPSIS ranking for decision alternatives"""
    norm = matrix / np.sqrt((matrix**2).sum(axis=0))
    weighted = norm * weights

    ideal_best = np.where(impacts == "+", weighted.max(axis=0), weighted.min(axis=0))
    ideal_worst = np.where(impacts == "+", weighted.min(axis=0), weighted.max(axis=0))

    dist_best = np.linalg.norm(weighted - ideal_best, axis=1)
    dist_worst = np.linalg.norm(weighted - ideal_worst, axis=1)

    scores = dist_worst / (dist_best + dist_worst)
    return scores

if __name__ == "__main__":
    # Example: 3 ports × 3 criteria
    matrix = np.array([
        [300, 4, 7],  # Oran
        [500, 5, 6],  # Algiers
        [450, 3, 8]   # Skikda
    ])
    weights = np.array([0.5, 0.3, 0.2])  # from AHP
    impacts = np.array(["-", "+", "+"])  # distance(-), capacity(+), infra(+)

    scores = topsis(matrix, weights, impacts)
    ranking = np.argsort(scores)[::-1]
    print("Scores:", scores)
    print("Ranking (best to worst):", ranking)
