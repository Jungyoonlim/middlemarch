import json 
import spacy 

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus

def evalute(corpus):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 20000000
    symbols = []
    for doc in nlp.pipe(corpus, batch_size=1000):
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN']:
                symbols.append(token.text)
    symbols = list(set(symbols))
    save_symbols(symbols, 'symbols.json')

def analyze_symbols(corpus, nlp):
    pass

def save_symbols(symbols, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(symbols, f, ensure_ascii=False, indent=4)

def main():
    pass

if __name__ == '__main__':
    main()

