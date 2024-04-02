import json 
import spacy 

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus

def evaluate(corpus):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 2000000  
    plot_events = []
    for doc in corpus:
        events = extract_plot_events(doc, nlp)
        plot_events.append(events)
    return plot_events

def extract_plot_events(doc, nlp):
    doc = nlp(' '.join(doc))
    events = []
    for sent in doc.sents:
        for token in sent:
            if token.pos_ == 'VERB':
                subject = None
                object = None
                for child in token.children:
                    if child.dep_ == 'nsubj':
                        subject = child.text
                    elif child.dep_ == 'dobj':
                        object = child.text
                if subject and object:
                    event = f"{subject} {token.lemma_} {object}"
                    events.append(event)
    return events

def save_plot_events(plot_events, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(plot_events, f, indent=4)

def main():
    corpus = load_corpus('../data/preprocessed_corpus.json')
    plot_events = evaluate(corpus)
    save_plot_events(plot_events, '../data/plot_events.json')
    print("Plot events extracted and saved.")

if __name__ == "__main__":
    main()



