#
# Given a query, runs it against the index. Spits out the top 50 documents, and the p@k scores.
#
# Author: David Maxwell
# Date: 2020-01-03
#

import os
import sys
from utils import get_query_performance_metrics

# As we are using ifind mashed into this repository, we need to add that to our path before we can import from it.
path_cwd = os.getcwd()
path_levelup = os.path.abspath(os.path.join(path_cwd, '..'))
path_treconomics_base = os.path.join(path_levelup, 'treconomics_project')
sys.path.append(path_treconomics_base)
# End appending of treconomics_project path

from ifind.search import Query, Response
from ifind.search.engines.whooshtrec import Whooshtrec
from ifind.seeker.trec_qrel_handler import TrecQrelHandler

def main(index_path, stopword_path, qrels_path, topic_num, query_terms):
    # Create a search engine like in experiment_configuration.py.
    search_engine = Whooshtrec(
        whoosh_index_dir=index_path,
        stopwords_file=stopword_path,
        model=1,
        newschema=True,
        implicit_or=True)
    
    search_engine.key_name = 'bm25'
    search_engine.set_fragmenter(frag_type=2, surround=40)
    search_engine.set_model(1, pval=0.75)
    # End create search engine

    q = Query(query_terms)
    q.skip = 1
    q.top = 1000

    qrels = TrecQrelHandler(qrels_path)
    response = search_engine.search(q)
    performance = get_query_performance_metrics(qrels, response.results, topic_num)

    print(f"Query: {query_terms}")
    print(f"Topic: {topic_num}")
    print(f"Results returned: {len(response)}")
    print(f"P@1: {performance[0]}")
    print(f"P@5: {performance[4]}")
    print(f"P@10: {performance[5]}")
    print(f"P@20: {performance[7]}")
    print(f"rprec: {performance[-2]}")
    print(f"Total number of relevant docs (TREC topic): {performance[-1]}")
    print()
    print("Top 50 results:")
    
    i = 0

    for doc in response.results:
        if i == 49:
            break

        print(doc.docid.decode('utf-8'))
        i = i + 1


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print(f"Usage: {sys.argv[0]} <index_path> <stopword_path> <qrels_path> <topic_num> <query_terms:end>")
        print("Query terms can have spaces in them -- anything after the topic number is considered a query.")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], ' '.join(sys.argv[5:]))

