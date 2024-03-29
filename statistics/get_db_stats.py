import json
from parse_db import read_ppdb
from progress.bar import Bar
from collections import Counter


def read_data(path_to_json_file):
    with open(path_to_json_file, 'r') as f:
        content = json.load(f)
    return content


def write_results_to_file(counter, key_to_look_for, pdb):
    with open('results.txt', 'a') as outfile:
        line_to_write = "{0}\t{1}\t{2}\n".format(
            counter, key_to_look_for, pdb[key_to_look_for]['ENTAILMENT'])
        outfile.write(line_to_write)


def main():
    # previously used content = read_data('./noun_corrections_INC_ED.json')
    content = read_data('noun_corrections_INC_ED.json')
    print(len(content))
    print("read pdb")
    pdb = read_ppdb('../data/ppdb/ppdb-xxxl-lexical.txt')
    bar = Bar('Processing', max=len(content))
    total = 0
    matches = 0
    match_per_sent_total = 0
    entailment_types = Counter()
    for counter, elem in enumerate(content, 1):
        matches_in_pair = 0
        for pair in elem['Differences']:
            total += 1
            source = pair[0]
            target = pair[1]
            key_to_look_for = "{0}#{1}".format(
                source[0].lower(), target[0].lower())
            try:
                print(pdb[key_to_look_for])
                matches += 1
                matches_in_pair += 1
                entailment_types[pdb[key_to_look_for]['ENTAILMENT']] += 1

            except KeyError:
                with open('missing_cases.txt', 'a') as out_file:
                    line_to_write = "{0}\t{1}\n".format(
                        counter, key_to_look_for)
                    out_file.write(line_to_write)

        if matches_in_pair > 0:
            match_per_sent_total += 1
        bar.next()
    bar.finish()
    total_matches = matches / total
    print("Total Pairs in Corpus: ", len(content))
    print("Sents with matches:", match_per_sent_total)
    print('Percentage:', (match_per_sent_total/len(content)))
    print("-------------------------------------")
    print("Total differences: ", total)
    print("Matches: ", matches)
    print("Perc: ", total_matches)
    print("----------------------------------------")
    print(entailment_types)


main()
