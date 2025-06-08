import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ground_truth = np.loadtxt('truth.txt', dtype=str)
predictions = np.loadtxt('predictions.txt', dtype=str)

positive = 'Sith'
negative = 'Jedi'

# Compute confusion matrix
TP = sum((t == positive and p == positive) for t, p in zip(ground_truth, predictions))
TN = sum((t == negative and p == negative) for t, p in zip(ground_truth, predictions))
FP = sum((t == negative and p == positive) for t, p in zip(ground_truth, predictions))
FN = sum((t == positive and p == negative) for t, p in zip(ground_truth, predictions))

# Compute printing calculations
Precision_1 = TN / (TN + FN)
Recall_1 = TN / (TN + FP)
F1_1 = 2 * (Precision_1 * Recall_1) / (Precision_1 + Recall_1)
total_1 = sum(ground_truth == negative)

Precision_2 = TP / (TP + FP)
Recall_2 = TP / (TP + FN)
F1_2 = 2 * (Precision_2 * Recall_2) / (Precision_2 + Recall_2)
total_2 = sum(ground_truth == positive)

Accuracy = (TP + TN) / (TP + FP + FN + TN)
total_3 = total_1 + total_2
data = {
    'Class': [negative, positive],
    'Precision': [Precision_1, Precision_2],
    'Recall': [Recall_1, Recall_2],
    'F1-Score': [F1_1, F1_2],
    'total': [total_1, total_2]
}

df = pd.DataFrame(data)
print(df.round(2))
print('accuracy', Accuracy, total_3)

# Format into a 2x2 matrix
conf_matrix = np.array([[TN, FP],
                        [FN, TP]])
print(conf_matrix)

# Display matrix
plt.figure(figsize=(5, 4))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='viridis', xticklabels=['0', '1'], yticklabels=['0', '1'])
plt.title("Confusion Matrix")
plt.show()
