from nltk.tokenize import word_tokenize
import pickle
import nltk
from collections import Counter

path_to_markers = '../data/discourse_markers.pickle'
with open(path_to_markers, 'rb') as pickle_in:
    markers = pickle.load(pickle_in)


def type_token_ratio(document):
    """
        Input: tokenize document 
        Returns: the type-token-ratio for a document.
    """
    # first tokenize the document
    document = word_tokenize(document)
    all_tokens = [token for token in document]
    num_of_tokens = len(all_tokens)
    unique_tokens = list(set(all_tokens))
    num_of_unique_tokens = len(unique_tokens)
    type_token_ratio = num_of_unique_tokens/num_of_tokens
    return type_token_ratio


def check_discourse_matches(tokens):
    """
        Input: tokenized sent or document from wikihow_instance
    """
    total = 0
    unigram_matches = 0
    bigram_matches = 0
    trigram_matches = 0
    fourgram_matches = 0
    fivegram_matches = 0
    # print("-----")
    # Later zal dit meteen het document zijn/de tokens.
    tokens = word_tokenize(tokens)
    #tokens = regex_tokeniser(tokens)
    for token in tokens:
        if token in markers.keys():
            if 'fivegrams' in markers[token].keys():
                fivegrams = [[tokens[i], tokens[i+1], tokens[i+2],
                              tokens[i+3], tokens[i+4]] for i in range(len(tokens)-5)]
                for fivegram in fivegrams:
                    if fivegram in markers[token]['fivegrams']:
                        fivegram_matches += 1
                        total += 1
                        # print(fivegram_matches, '#',
                        #      markers[token]['fivegrams'])
                        # print("\n")

            if 'fourgrams' in markers[token].keys():
                fourgrams = [[tokens[i], tokens[i+1], tokens[i+2],
                              tokens[i+3]] for i in range(len(tokens)-4)]
                for fourgram in fourgrams:
                    if fourgram in markers[token]['fourgrams']:
                        fourgram_matches += 1
                        total += 1
                        # print(fourgram, '#', markers[token]['fourgrams'])
                        # print("\n")

            if 'trigrams' in markers[token].keys():
                trigrams = [[tokens[i], tokens[i+1], tokens[i+2]]
                            for i in range(len(tokens)-3)]
                for trigram in trigrams:
                    if trigram in markers[token]['trigrams']:
                        trigram_matches += 1
                        total += 1
                        # print(trigram, '#', markers[token]['trigrams'])
                        # print("\n")

            if 'bigrams' in markers[token].keys():
                bigrams = [[tokens[i], tokens[i+1]]
                           for i in range(len(tokens)-2)]
                for bigram in bigrams:
                    if bigram in markers[token]['bigrams']:
                        bigram_matches += 1
                        total += 1
                        #print(bigram, markers[token]['bigrams'])
                        # print("\n")
            if 'unigrams' in markers[token].keys():
                # print(token, '#', markers[token]['unigrams'])
                unigram_matches += 1
                total += 1
    return {"score": unigram_matches + bigram_matches + trigram_matches + fourgram_matches + fivegram_matches}


def mark_cases(context, matches, source=True):
    if source:
        match = [elem[0][0].lower() for elem in matches]
    else:
        match = [elem[1][0].lower() for elem in matches]

    tokenized_doc = word_tokenize(context)
    document = [word[0] for word in nltk.pos_tag(tokenized_doc)]

    final_rep = []
    for word in document:
        if word.lower() in match:
            word = word + "__REV__"
            final_rep.append(word)
        else:
            final_rep.append(word)
    coherence_score = compute_coherence(final_rep)
    return coherence_score


def compute_coherence(doc):
    """
        Input: X formatted with __REV__
    """

    freq = Counter()
    d = {}
    for word in doc:
        if '__REV__' in word:
            freq[word.lower()] += 1
    bow = dict(freq)
    coherence_score = 0
    for key, _ in bow.items():
        if bow[key] > 1:
            coherence_score += 1
        else:
            coherence_score += 0
    try:
        score = coherence_score / len(bow)
    except ZeroDivisionError:
        score = 0
    return score
    #d["score"] = score
    # return d
