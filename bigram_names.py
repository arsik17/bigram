import collections
import random
import pandas as pd
import matplotlib.pyplot as plt

def read_names(file_name):
    with open(file_name, 'r') as file:
        name_list = file.read().splitlines()
    return name_list

def calculate_probs(name_list, f=1):
    pair_count = collections.defaultdict(int)
    total_count = 0

    for name in name_list:
        name = '^' + name + '$'
        total_count += len(name) - 1
        for i in range(len(name) - 1):
            pair = name[i] + name[i+1]
            pair_count[pair] += 1
    
    for pair in set(pair_count.keys()):
        pair_count[pair] += f
    
    pair_probs = {}
    for pair, count in pair_count.items():
        prob = count / (total_count + f * len(set(pair_count.keys())))
        pair_probs[pair] = prob
    
    return pair_probs

def generate_name(pair_probs):
    name = ''
    current_letter = '^'

    while current_letter != '$':
        name += current_letter
        possible_pairs = [pair for pair in pair_probs.keys() if pair.startswith(current_letter)]
        probabilities = [pair_probs[pair] for pair in possible_pairs]
        current_letter = random.choices(possible_pairs, probabilities)[0][1]
        # print(current_letter)

    if name[1:].isspace() or len(name[1:]) < 2 or len(name[1:]) > 15:
        name = '^' + generate_name(pair_probs)
    
    return name[1:]

def visualize_probs(pair_probs):
    data = {'Bigram': [], 'Probability': []}

    for bigram, probability in pair_probs.items():
        data['Bigram'].append(bigram)
        data['Probability'].append(probability)

    df = pd.DataFrame(data)
    df = df.sort_values('Probability', ascending=False).reset_index(drop=True)

    plt.figure(figsize=(10, 6))
    plt.bar(df['Bigram'], df['Probability'])
    plt.xlabel('Bigram')
    plt.ylabel('Probability')
    plt.title('Bigram Probabilities')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('bigram_probabilities.png')
    
name_list = read_names('names.txt')
pair_probs = calculate_probs(name_list, f=0.1)
print('Generated name is: ' + generate_name(pair_probs))
visualize_probs(pair_probs)