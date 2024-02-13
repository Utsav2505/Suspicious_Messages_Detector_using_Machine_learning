import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

data = pd.read_csv(r'dataset\Suspicious Communication on Social Platforms.csv')
X=data.drop(columns=['tagging'])
y=data['tagging']

data['comments'] = data['comments'].str.lower()

def remove_punctuation(text):
    punctuation_pattern = r'[^\w\s]'
    return re.sub(punctuation_pattern, '', text)

data['comments'] = data['comments'].apply(remove_punctuation)
print(data['comments'])

# stop words removal
def remove_stopwords(text, language):
    stop_words = set(stopwords.words(language))
    word_tokens = text.split()
    filtered_text = [word for word in word_tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)
data['comments'] = data['comments'].apply(lambda x: remove_stopwords(x, 'english'))
print(data['comments'])

# Stemming

stemmer = PorterStemmer()
 
def stem_words(text):
    word_tokens = text.split()
    stems = [stemmer.stem(word) for word in word_tokens]
    return stems
data['comments'] = data['comments'].apply(lambda x: stem_words(x))
print(data['comments'])



# model.fit(X,y)
X_train, X_test, y_train, y_test = train_test_split(data['comments'], data['tagging'], test_size=0.2, random_state=42)

X_train_str = X_train.apply(lambda x: ' '.join(x))
X_test_str = X_test.apply(lambda x: ' '.join(x))

# TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=5000) 

# Fit and transform
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train_str)

# Transform test data
X_test_tfidf = tfidf_vectorizer.transform(X_test_str)

RandomForestClassifier_model = RandomForestClassifier()

# Train the model
RandomForestClassifier_model.fit(X_train_tfidf, y_train)

# predictions
y_pred = RandomForestClassifier_model.predict(X_test_tfidf)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

print(classification_report(y_test, y_pred))

joblib.dump(RandomForestClassifier_model,'model\RandomForestClassifier_model.joblib')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')