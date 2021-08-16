import torch
import torchtext
from torchtext.vocab import build_vocab_from_iterator
from torchtext.datasets import text_classification
import os

NGRAMS = 2

if not os.path.isdir('./.data'):
    os.mkdir('./.data')
train_dataset, test_dataset = text_classification.DATASETS['AG_NEWS'](root='./.data',
                                                                      ngrams=NGRAMS,
                                                                      vocab=None)
BATCH_SIZE = 16
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
