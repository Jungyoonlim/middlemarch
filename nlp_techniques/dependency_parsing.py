import spacy
import json

nlp = spacy.load('en_core_web_sm')
nlp.max_length = 2000000

def load_preprocessed_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus 

def perform_dependency_parsing(corpus):
    parsed_corpus = []
    for doc in corpus:
        doc_chunks = [' '.join(doc[i:i+500000]) for i in range(0, len(doc), 500000)]  # Join tokens into a string
        parsed_doc = []
        for chunk in doc_chunks:
            parsed_chunk = nlp(chunk)
            parsed_doc.extend([(token.text, token.dep_, token.head.text) for token in parsed_chunk])
        parsed_corpus.append(parsed_doc)
    return parsed_corpus

preprocessed_corpus = load_preprocessed_corpus('../data/preprocessed_corpus.json')
parsed_corpus = perform_dependency_parsing(preprocessed_corpus)

with open('../data/parsed_corpus.json', 'w') as f:
    json.dump(parsed_corpus, f, indent=4)