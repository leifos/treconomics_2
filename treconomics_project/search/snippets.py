__author__ = 'leif'
import nltk

from bs4 import BeautifulSoup

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(', '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

def extract_entities(summary):
    soup = BeautifulSoup(summary,'html.parser')
    text = soup.getText()
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    #print tokenized_sentences
    #print "--------------"
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    chunked_sentences = nltk.chunk.ne_chunk_sents(tagged_sentences, binary=True)
    entity_names = []
    for tree in chunked_sentences:
        # Print results per sentence
        # print extract_entity_names(tree)
        entity_names.extend(extract_entity_names(tree))

    return set(entity_names)

def entity_snippet(response):
    """
    Helper function that parses snippets and extract named entities.
    """
    for result in response.results:
        e_set = extract_entities(result.summary)
        result.summary = ' '.join(e_set)
    return response

