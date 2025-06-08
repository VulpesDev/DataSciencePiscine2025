import sys
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier


# Check command-line args
if len(sys.argv) != 4:
    print("Usage: python3 KNN.py Train.csv Test.csv Validation.csv")
    sys.exit(1)

# Assign file paths
train_file = sys.argv[1]
test_file = sys.argv[2]
validation_file = sys.argv[3]

# Extract data from files
train_df = pd.read_csv(train_file)
X_train = train_df.iloc[:, :-1]
y_train = train_df.iloc[:, -1]

test_df = pd.read_csv(test_file)
y_test = test_df.iloc[:, -1]
X_test = test_df[X_train.columns]

valid_df = pd.read_csv(validation_file)
y_valid = valid_df.iloc[:, -1]
X_valid = valid_df[X_train.columns]

# Precision % according to the count of k-value
k_values = range(1, 30)
f1_scores = []
for k in k_values :
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(X_train, y_train)
            y_pred = knn.predict(X_valid)
            acc = accuracy_score(y_valid, y_pred)
            f1_scores.append(acc)
best_k = k_values[f1_scores.index(max(f1_scores))]
print("Best k: ", best_k)
print("F1 score for this k: ", f1_scores[best_k])
plt.plot(k_values, f1_scores)
plt.ylabel("accuracy")
plt.xlabel("k values")
plt.show()

# Save predictions in a file
k = best_k
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)
prediction = knn.predict(X_test)

with open("KNN.txt", "w") as f:
        for value in prediction:
            f.write(f"{value}\n")

