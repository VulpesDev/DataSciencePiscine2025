import sys
from matplotlib import pyplot as plt
import pandas as pd

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

# Check command-line args
if len(sys.argv) != 4:
    print("Usage: python3 TreeModel.py Train.csv Test.csv Validation.csv")
    sys.exit(1)

# Assign file paths
train_file = sys.argv[1]
test_file = sys.argv[2]
validation_file = sys.argv[3]

# Extract data from files
train_df = pd.read_csv(train_file)
X_train = train_df.iloc[:, :-1]
y_train = train_df.iloc[:, -1]

valid_df = pd.read_csv(validation_file)
y_valid = valid_df.iloc[:, -1]
X_valid = valid_df[X_train.columns]

test_df = pd.read_csv(test_file)
y_test = test_df.iloc[:, -1]
X_test = test_df[X_train.columns]

# Train model
clf = RandomForestClassifier(max_leaf_nodes=19, random_state=8 )
clf.fit(X_train, y_train)

# Predict
y_valid_pred = clf.predict(X_valid)
y_test_pred = clf.predict(X_test)

# Evaluate on validation set
f1 = f1_score(y_valid, y_valid_pred, average='weighted')
print(y_valid_pred)
print("F1 Score:", f1)

# Save predictions to Tree.txt
with open("Tree.txt", "w") as f:
    for value in y_test_pred:
        f.write(f"{value}\n")

print(y_test_pred)

# Display data on plot_tree graph
plt.figure(figsize=(20, 10))
tree.plot_tree(clf.estimators_[0], filled=True, feature_names=X_train.columns, class_names=clf.classes_)
plt.show()