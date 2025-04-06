import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder

# Load the dataset
file_path = '../data_sources/mathv4_processed_3.csv'
data = pd.read_csv(file_path)

# Display basic information about the dataset
def explore_data(data):
    print(data.head())
    print(data.info())
    print(data.describe())

# Preprocess the data
def preprocess_data(data):
    # Fill missing values
    data.fillna('', inplace=True)
    
    # Combine text features
    data['combined_text'] = data['Problem'] + ' ' + data['Type'] + ' ' + data['Solution']
    
    # Encode the difficulty level
    label_encoder = LabelEncoder()
    data['Difficulty_encoded'] = label_encoder.fit_transform(data['Difficulty'])
    
    # Vectorize the text data
    vectorizer = TfidfVectorizer(max_features=500)
    X = vectorizer.fit_transform(data['combined_text']).toarray()
    y = data['Difficulty_encoded']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, label_encoder

# Run exploration and preprocessing
explore_data(data)
X_train, X_test, y_train, y_test, label_encoder = preprocess_data(data) 