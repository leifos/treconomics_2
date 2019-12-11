#
# Hacky script that calculates the P@k for a series of queries.
# Not complying with good SE practices; just munged together.
# Dumps the output to stdout. Pipe it to a file.
# You may need to comment out the print statements in the ifind Whooshtrec class (lines 177 and 204)
#
# Author: David
# Updated: 2019-12-07
#

# Change the following vars below.

qrels_path = 'TREC2005.qrels.txt'  # Where is the TREC QRELs file to use?
input_file = 'query.in'  # Where is the list of queries to execute in batch? CSV (topicnumber,terms)
index_path = 'small100index/'  # Where is the new index?
stopwords_file = 'stopwords.txt'  # Where are the stopwords (for the querying process)?
implicit_or = True  # OR (True) or AND (False) query terms?
bm25_beta = 0.75  # What value of beta should we use for the retrieval model?

################
import sys
import os
pp = os.path.abspath("../")
sys.path.append(pp)
from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from ifind.search.engines.whooshtrec import Whooshtrec
from ifind.search import Query

f = open(input_file, 'r')
queries = []

for line in f:
    line = line.strip().split(',')
    topic = line[0]
    terms = line[1]

    queries.append({'topic': topic, 'terms': terms})

f.close()
qrels = TrecQrelHandler(qrels_path)

def run_query(engine, q_str):
    """
    Executes the query.
    Returns a set of results. ifind results object.
    """
    query = Query(q_str)
    query.skip = 1
    query.top = 20
    return engine.search(query)

def get_patk(qrels, topic, results, up_to):
    """
    Rudimentary function to calculate the precision@up_to.
    Returns a float.
    """
    judgements = []
    i = 0

    for doc in results:
        if i == up_to:
            break
        
        judgement = qrels.get_value(topic, doc.docid.decode("utf-8"))

        if judgement > 0:
            judgements.append(1)
        else:
            judgements.append(0)

        i = i + 1
    
    if len(judgements) == 0:
        return 0.0

    return sum(judgements) / float(up_to)

search_engine = Whooshtrec(
    whoosh_index_dir=index_path,
    stopwords_file=stopwords_file,
    model=1,
    newschema=True,
    implicit_or=implicit_or)

search_engine.key_name = 'bm25'
search_engine.set_model(1, pval=bm25_beta)
search_engine.set_fragmenter(frag_type=2, surround=40)

print('terms,topic,p1,p3,p5,p10,p20,no_of_hits')

dfile = open("retrieved.docids","w")

for query in queries:
    topic = query['topic']
    terms = query['terms']

    results = run_query(search_engine, terms)
    for doc in results:
        dfile.write(doc.docid.decode("utf-8")+os.linesep)


    pat1 = get_patk(qrels, topic, results, 1)
    pat3 = get_patk(qrels, topic, results, 3)
    pat5 = get_patk(qrels, topic, results, 5)
    pat10 = get_patk(qrels, topic, results, 10)
    pat20 = get_patk(qrels, topic, results, 20)
    no_of_hits = len(results)

    print(f"{terms},{topic},{pat1},{pat3},{pat5},{pat10},{pat20},{no_of_hits}")

dfile.close()
