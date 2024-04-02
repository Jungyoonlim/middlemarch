import json
import spacy 
from spacy.attrs import LEMMA, POS, DEP
from collections import Counter

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus

def evaluate(corpus):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 2000000
    stylistic_features = []
    for doc_item in corpus:
        if isinstance(doc_item, str):
            doc = doc_item
        elif isinstance(doc_item, list):
            doc = ' '.join(doc_item)
        else:
            doc = doc_item.get('text', '')
        features = analyze_stylistic_features(doc, nlp)
        stylistic_features.append(features)
    return stylistic_features

def analyze_stylistic_features(doc, nlp):
    """
    Analyzes various stylistic features of a given text document.
    
    Args:
        doc (str): The text document to analyze.
        nlp (spacy.lang.en.English): The spaCy language model instance.
        
    Returns:
        dict: A dictionary containing the extracted stylistic features.
    """
    
    # Parse the document with spaCy
    doc = nlp(doc)
    
    # Initialize feature dictionaries
    pos_counts = Counter()
    dep_counts = Counter()
    
    # Iterate over tokens and count POS tags and dependencies
    for token in doc:
        pos_counts[token.pos_] += 1
        dep_counts[token.dep_] += 1
        
    # Calculate lexical diversity (ratio of unique words to total words)
    unique_words = set([token.lemma_ for token in doc])
    lexical_diversity = len(unique_words) / len(doc)
    
    # Calculate average word length
    word_lengths = [len(token.text) for token in doc if not token.is_punct]
    avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0
    
    # Calculate average sentence length
    sentences = list(doc.sents)
    sentence_lengths = [len(sent) for sent in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
    
    # Construct feature dictionary
    features = {
        'pos_counts': dict(pos_counts),
        'dep_counts': dict(dep_counts),
        'lexical_diversity': lexical_diversity,
        'avg_word_length': avg_word_length,
        'avg_sentence_length': avg_sentence_length
    }
    
    return features


def save_stylistic_features(stylistic_features, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stylistic_features, f, indent=4)

def main():
    corpus = load_corpus('../data/preprocessed_corpus.json')
    stylistic_features = evaluate(corpus)
    save_stylistic_features(stylistic_features, '../data/stylistic_features.json')
    print("Stylistic features extracted and saved.")

if __name__ == "__main__":
    main()