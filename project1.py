# -*- coding: utf-8 -*-
"""Untitled10.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j0_lORYuEBuxdZkMB6pGSanqNq99ZTux
"""

pip install kagglehub pandas scikit-learn nltk

# Import necessary libraries
import kagglehub
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

# Step 1: Download the dataset using kagglehub
path = kagglehub.dataset_download("lakshmi25npathi/imdb-dataset-of-50k-movie-reviews")
print("Path to dataset files:", path)

# Step 2: Load the dataset (Assuming 'IMDB Dataset.csv' is the file name, adjust if necessary)
file_path = f"{path}/IMDB Dataset.csv"
data = pd.read_csv(file_path)

# Display the first few rows of the dataset
print(data.head())

# Step 3: Data Preprocessing
# Clean text by removing stopwords
stop_words = set(stopwords.words('english'))

def clean_text(text):
    # Remove stopwords and punctuation from text
    words = text.split()
    cleaned_text = ' '.join([word for word in words if word.lower() not in stop_words])
    return cleaned_text

# Apply the clean_text function to the reviews column
data['cleaned_review'] = data['review'].apply(clean_text)

# Step 4: Split the data into training and testing sets
X = data['cleaned_review']
y = data['sentiment'].apply(lambda x: 1 if x == 'positive' else 0)  # Convert 'positive' -> 1 and 'negative' -> 0

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Step 5: Convert text data into numerical features using CountVectorizer
vectorizer = CountVectorizer(max_features=5000)  # Limit to top 5000 features for efficiency
X_train_cv = vectorizer.fit_transform(X_train)
X_test_cv = vectorizer.transform(X_test)

# Step 6: Train a Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train_cv, y_train)

# Step 7: Make predictions on the test set
y_pred = classifier.predict(X_test_cv)

# Step 8: Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Step 9: Function for sentiment prediction on user input
def predict_sentiment(sentence):
    # Clean the input sentence
    cleaned_sentence = clean_text(sentence)
    # Convert the cleaned sentence to a vector using the same vectorizer
    sentence_cv = vectorizer.transform([cleaned_sentence])
    # Predict the sentiment (0: Negative, 1: Positive)
    prediction = classifier.predict(sentence_cv)
    if prediction == 1:
        return "Positive"
    else:
        return "Negative"

# Step 10: Test the model with a user input sentence
user_input = input("Enter a movie review: ")
sentiment = predict_sentiment(user_input)
print(f"The sentiment of the review is: {sentiment}")

