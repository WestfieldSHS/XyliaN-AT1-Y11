import json

with open('vocab.json', 'r', encoding='utf-8') as f:
    vocab = json.load(f)
import random
#Welcome message
print("Welcome to Vocabulary! Here are some wordd to expand your lexicon:")
#loop through vocab and print each word and its definition
for word in random.sample(list(vocab.keys()), min(5, len(vocab))):  # Print only 10 random words/Refresh daily features
    info = vocab[word]
    print(f'{word} ({info["type"]}): {info["definition"]}')