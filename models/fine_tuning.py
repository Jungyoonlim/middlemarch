import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from torch.utils.data import Dataset

def load_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        corpus = json.load(f)
    return corpus

def preprocess_data(corpus, tokenizer):
    preprocessed_data = []
    for doc in corpus:
        encoded_input = tokenizer(' '.join(doc), padding=True, truncation=True, return_tensors='pt')
        preprocessed_doc = {
            'input_ids': encoded_input['input_ids'].squeeze(),
            'attention_mask': encoded_input['attention_mask'].squeeze(),
            'labels': 0  # Placeholder label, replace with actual labels if available
        }
        preprocessed_data.append(preprocessed_doc)
    return preprocessed_data

class TextDataset(Dataset):
    def __init__(self, preprocessed_data):
        self.data = preprocessed_data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

def fine_tune_model(dataset):
    model_name = 'bert-base-uncased'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=16,
        learning_rate=2e-5
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    trainer.train()
    model.save_pretrained('./fine_tuned_model')

if __name__ == '__main__':
    corpus_file_path = '../data/preprocessed_corpus.json'
    corpus = load_corpus(corpus_file_path)
    
    model_name = 'bert-base-uncased'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    preprocessed_data = preprocess_data(corpus, tokenizer)
    dataset = TextDataset(preprocessed_data)
    fine_tune_model(dataset)