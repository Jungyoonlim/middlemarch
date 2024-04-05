import json
import os
import spacy

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus

def preprocess_text(text):
    return ' '.join(text)

def theme_identification(corpus):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 2000000
    preprocessed_corpus = [preprocess_text(doc) for doc in corpus]
    themes = []
    for doc in preprocessed_corpus:
        doc = nlp(doc)
        identified_themes = []
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN']:
                identified_themes.append(token.text)
        themes.append(identified_themes)
    return themes

def save_theme(theme, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(theme, f, ensure_ascii=False, indent=4)

def main():
    corpus = load_corpus('../data/preprocessed_corpus.json')
    theme_events = theme_identification(corpus)
    save_theme(theme_events, '../data/theme_identification.json')
    print("Themes identified and saved.")

if __name__ == '__main__':
    main()