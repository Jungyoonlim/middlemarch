import requests
import os
import json

def download_text(url, output_dir):
    response = requests.get(url)
    if response.status_code == 200:
        text = response.text
        filename = os.path.join(output_dir, url.split("/")[-1] + ".txt")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

def collect_gutenberg_texts(urls, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for url in urls:
        download_text(url, output_dir)

# Example usage
urls = [
    "https://www.gutenberg.org/files/1524/1524-0.txt",  # Hamlet by William Shakespeare
    "https://www.gutenberg.org/files/1727/1727-0.txt",  # Pride and Prejudice by Jane Austen
    "https://www.gutenberg.org/files/145/145-0.txt",    # Middlemarch by George Eliot
    "https://www.gutenberg.org/files/1661/1661-0.txt",  # The Adventures of Sherlock Holmes by Arthur Conan Doyle
    "https://www.gutenberg.org/files/1952/1952-0.txt",  # The Yellow Wallpaper by Charlotte Perkins Gilman
    "https://www.gutenberg.org/files/84/84-0.txt",      # Frankenstein; Or, The Modern Prometheus by Mary Wollstonecraft Shelley
    "https://www.gutenberg.org/files/98/98-0.txt",      # A Tale of Two Cities by Charles Dickens
    "https://www.gutenberg.org/files/1342/1342-0.txt",  # Pride and Prejudice by Jane Austen
    "https://www.gutenberg.org/files/11/11-0.txt",      # Alice's Adventures in Wonderland by Lewis Carroll
    "https://www.gutenberg.org/files/345/345-0.txt",    # Dracula by Bram Stoker
]
output_dir = "../data/raw_texts"
collect_gutenberg_texts(urls, output_dir)

def save_expanded_corpus(output_dir):
    expanded_corpus = []
    for file in os.listdir(output_dir):
        if file.endswith(".txt"):
            file_path = os.path.join(output_dir, file)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
                expanded_corpus.append({"text": text})

    with open("../data/expanded_corpus.json", "w") as f:
        json.dump(expanded_corpus, f, indent=4)

# Example usage
output_dir = "../data/raw_texts"
save_expanded_corpus(output_dir)