# Vocabulary daily refresh feature
import json

with open('vocab.json', 'r', encoding='utf-8') as f:
    vocab = json.load(f)
#user data handling
with open('user.json', 'r', encoding='utf-8') as f:
    user = json.load(f)
import random #random module for selecting random words for daily refresh feature
#Welcome message
print("Welcome to Vocabulary! Here are some wordd to expand your lexicon:")
print() #blank line for better readability
#loop through vocab and print each word and its definition
for word in random.sample(list(vocab.keys()), min(5, len(vocab))):  # Print only 5 random words/Refresh daily features
    info = vocab[word]
    print(f'{word} ({info["type"]}): {info["definition"]}')
    print() #blank line for better readability

#favorite words feature
def add_to_favorites(word):
    if word in vocab:
        if word not in user['favorites']:
            user['favorites'].append(word)
            print(f' "{word}" added to your favorites!')
        else:
            print(f' "{word}" is already in your favorites.')
    else:
        None
        
#user review feature
def user_review(word):
    if word in vocab:
        review = input(f'Enter your review for word "{word}": ')
        user['reviews'][word] = review
        print(f'Review added for word "{word}".')