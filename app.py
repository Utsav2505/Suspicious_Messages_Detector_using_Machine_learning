from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

app = Flask(__name__)
loaded_model = joblib.load(r'model\RandomForestClassifier_model.joblib')
tfidf_vectorizer = joblib.load(r'model\tfidf_vectorizer.joblib')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/check', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the input from the form or JSON request
        chat = request.form['chat']
        chat_tfidf = tfidf_vectorizer.transform([chat])
        
        result = loaded_model.predict(chat_tfidf)
        
        if result[0] == 1:
            return render_template('result.html', prediction="The message is suspicious.")
        else:
            return render_template('result.html', prediction="The message is not suspicious.")

if __name__ == '__main__':
    app.run(debug=True)
