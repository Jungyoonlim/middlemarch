import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def load_expanded_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    return words

def preprocess_corpus(corpus):
    preprocessed_corpus = []
    for text in corpus:
        preprocessed_text = preprocess_text(text['text'])
        preprocessed_corpus.append(preprocessed_text)
    return preprocessed_corpus

# Example usage
expanded_corpus = load_expanded_corpus('../data/expanded_corpus.json')
preprocessed_corpus = preprocess_corpus(expanded_corpus)

# Save the preprocessed corpus
with open('../data/preprocessed_corpus.json', 'w') as f:
    json.dump(preprocessed_corpus, f, indent=4)