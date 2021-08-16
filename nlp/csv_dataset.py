import io

from torchtext.data.utils import ngrams_iterator
from torchtext.vocab import build_vocab_from_iterator
from torchtext.data.utils import get_tokenizer
from torchtext.utils import unicode_csv_reader
from torchtext.datasets.text_classification import TextClassificationDataset, _create_data_from_iterator


def _csv_iterator(data_path,
                  ngrams,
                  skip_header=True,
                  yield_cls=False,
                  label_col=6,
                  token_col=[1, 5],
                  label_mapping={
                      "simulation": 0,
                      "hardware": 1,
                      "edge_computing": 2
                  }):
    tokenizer = get_tokenizer("spacy", "en_core_web_sm")
    with io.open(data_path, encoding="utf8") as f:
        reader = unicode_csv_reader(f)
        if skip_header:
            next(reader, None)
        for row in reader:
            tokens = ' '.join([j for i, j in enumerate(row) if i in token_col])
            tokens = tokenizer(tokens)
            if yield_cls:
                yield label_mapping[row[label_col]], ngrams_iterator(tokens, ngrams)
            else:
                yield ngrams_iterator(tokens, ngrams)


def csv_dataset(csv_path, ngrams):
    vocab = build_vocab_from_iterator(_csv_iterator(csv_path, ngrams))
    train_data, train_labels = _create_data_from_iterator(
        vocab, _csv_iterator(csv_path, ngrams, yield_cls=True), False)
    return TextClassificationDataset(vocab, train_data, train_labels)
