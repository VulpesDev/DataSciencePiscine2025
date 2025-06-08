import sys
import pandas as pd
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import f1_score

# Check command-line args
if len(sys.argv) != 4:
    print("Usage: python3 democracy.py Train.csv Test.csv Validation.csv")
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

# Define classifiers
clf1 = KNeighborsClassifier(n_neighbors=3)
clf2 = RandomForestClassifier(n_estimators=100, random_state=42)
clf3 = LogisticRegression(max_iter=3000)

#Create a voting classifier
voting_clf = VotingClassifier(estimators=[
    ('knn', clf1),
    ('rf', clf2),
    ('lr', clf3)
], voting='hard')

# Train model
voting_clf.fit(X_train, y_train)

# Evaluate on validation set
y_pred_val = voting_clf.predict(X_valid)
f1 = f1_score(y_valid, y_pred_val, pos_label='Jedi')
print(f"F1-Score on validation set: {f1:.4f}")

# Predict on test data
predictions = voting_clf.predict(X_test)

# Save predictions to Voting.txt
with open("Voting.txt", "w") as f:
    for label in predictions:
        f.write(f"{label}\n")