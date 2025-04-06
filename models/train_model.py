import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from preprocess_data import preprocess_data
import pandas as pd

# Load and preprocess the data
X_train, X_test, y_train, y_test, label_encoder = preprocess_data(pd.read_csv('../data_sources/mathv4_processed_3.csv'))

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Make predictions
y_pred = rf_classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)

print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(report)

# Save the trained model
joblib.dump(rf_classifier, 'random_forest_model.joblib') 