#4b average precision and other metrics

from sklearn.metrics import average_precision_score, adjusted_rand_score, normalized_mutual_info_score, fowlkes_mallows_score

# Ground truth labels
y_true = [0, 1, 1, 0, 1, 1]

# Predicted scores for average precision (e.g., probabilities)
y_scores = [0.1, 0.4, 0.35, 0.8, 0.65, 0.9]

# Predicted labels for clustering metrics
y_pred = [0, 1, 0, 0, 1, 1]

# Evaluation metrics
average_precision = average_precision_score(y_true, y_scores)
ari = adjusted_rand_score(y_true, y_pred)
nmi = normalized_mutual_info_score(y_true, y_pred)
fmi = fowlkes_mallows_score(y_true, y_pred)

# Print metrics
print(f'Average Precision-Recall Score: {average_precision:.2f}')
print(f'Adjusted Rand Index (ARI): {ari:.2f}')
print(f'Normalized Mutual Information (NMI): {nmi:.2f}')
print(f'Fowlkes-Mallows Index (FMI): {fmi:.2f}')
