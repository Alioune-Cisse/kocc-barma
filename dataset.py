import torch
import pandas as pd
from collections import Counter
import re

class Dataset(torch.utils.data.Dataset):
    def __init__(
        self,
        args,
    ):
        self.args = args
        self.words = self.load_words()
        self.uniq_words = self.get_uniq_words()

        self.index_to_word = {index: word for index, word in enumerate(self.uniq_words)}
        self.word_to_index = {word: index for index, word in enumerate(self.uniq_words)}

        self.words_indexes = [self.word_to_index[w] for w in self.words]

    def load_words(self):
        #train_df = pd.read_csv('data/reddit-cleanjokes.csv')
        #text = train_df['Joke'].str.cat(sep=' ')
        # load ascii text and covert to lowercase
        filename = "https://github.com/Alioune-Cisse/pytorch-wolof-text-generator/raw/master/wolof_datasets.txt"
        raw_text = open(filename, 'r', encoding='utf-8').read()
        text_sale = raw_text.replace("\n"," ").lower()
        #text = re.sub('\W+',' ', text_sale)
        text = re.sub("#|@|\$|<|%|&|>|\*|§|\/", ' ', text_sale)
        return text.split(' ')

    def get_uniq_words(self):
        word_counts = Counter(self.words)
        return sorted(word_counts, key=word_counts.get, reverse=True)

    def get_alphabet(self):
      x = self.get_uniq_words()
      listes = sorted(set([re.sub(r'\W|\d', '', i) for i in x]))
      groups={}
      for word in listes[1:]:
          groups.setdefault(word[0],[]).append(word)
      return groups

    def __len__(self):
        return len(self.words_indexes) - self.args.sequence_length

    def __getitem__(self, index):
        return (
            torch.tensor(self.words_indexes[index:index+self.args.sequence_length]),
            torch.tensor(self.words_indexes[index+1:index+self.args.sequence_length+1]),
        )
