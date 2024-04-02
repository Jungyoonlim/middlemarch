import json
import spacy

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus

def evaluate(corpus):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 2000000
    char_events = []
    for doc in corpus:
        events = analyze_character_mentions(doc, nlp)
        char_events.append(events)
    return char_events

def analyze_character_mentions(corpus, nlp):
    doc = nlp(' '.join(corpus))
    char_events = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            char_events.append(ent.text)
    return char_events

def save_char_events(char_events, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(char_events, f, indent=4)

def main():
    corpus = load_corpus('../data/preprocessed_corpus.json')
    char_events = evaluate(corpus)
    save_char_events(char_events, '../data/char_events.json')
    print("Character events extracted and saved.")

if __name__ == "__main__":
    main()

