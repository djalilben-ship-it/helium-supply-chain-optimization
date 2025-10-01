# src/ahp.py
import numpy as np

def ahp(matrix):
    """Simple AHP weight calculation from pairwise comparison matrix"""
    column_sum = np.sum(matrix, axis=0)
    normalized = matrix / column_sum
    weights = np.mean(normalized, axis=1)
    return weights

if __name__ == "__main__":
    # Example comparison matrix (3 criteria)
    comparison_matrix = np.array([
        [1,   3,   0.5],
        [1/3, 1,   0.25],

        [2,   4,   1]
    ])
    weights = ahp(comparison_matrix)
    print("Criteria Weights:", weights)
