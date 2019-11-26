__author__ = 'leif'
import os
import socket
import logging
import logging.config
import logging.handlers
from treconomics.autocomplete_trie import AutocompleteTrie
from ifind.search.engines.whooshtrec import Whooshtrec
from treconomics.experiment_setup import ExperimentSetup

work_dir = os.getcwd()
# when deployed this needs to match up with the hostname, and directory to where the project is


#my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex/')
my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/newindex/')

my_whoosh_query_index_dir = os.path.join(work_dir, "/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file = os.path.join(work_dir, "data/TREC2005.qrels.txt")
stopword_file = os.path.join(work_dir, "data/stopwords.txt")
data_dir = os.path.join(work_dir, "data")

print("Work DIR: " + work_dir)
print("QRELS File: " + qrels_file)
print("my_whoosh_doc_index_dir: " + my_whoosh_doc_index_dir)
print("Stopword file: " + stopword_file)

event_logger = logging.getLogger('event_log')
event_logger.setLevel(logging.INFO)
event_logger_handler = logging.FileHandler(os.path.join(my_experiment_log_dir, 'experiment.log'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
event_logger_handler.setFormatter(formatter)
event_logger.addHandler(event_logger_handler)

# workflow must always start with startexperiment/


snippet_flow = [
    'startexperiment/', 'preexperiment/UK/',
    'demographicssurvey/',
    'prepracticetask/0/','taskspacer2/0/', 'search/0/', 'postpracticetask/0/', 'taskspacer',
    'snippetpretask/1/','taskspacer2/1/', 'search/1/', 'snippetposttask/1/','systemsnippetposttask/1/',
        'taskspacer',
    'snippetpretask/2/', 'taskspacer2/2/','search/2/', 'snippetposttask/2/','systemsnippetposttask/2/',
        'taskspacer',
    'snippetpretask/3/','taskspacer2/3/', 'search/3/', 'snippetposttask/3/','systemsnippetposttask/3/',
     'taskspacer',
    'snippetpretask/4/','taskspacer2/4/', 'search/4/', 'snippetposttask/4/','systemsnippetposttask/4/',
    'taskspacer', 'snippetexitsurvey/', 'performance/', 'endexperiment/',
    'logout/'
]

diversity_flow = [
    'startexperiment/', 'preexperiment/UK/',
    'demographicssurvey/',
    'prepracticetask/0/', 'search/0/', 'diversityperformancepractice/', 'postpracticetask/0/', 'taskspacer/',
    'snippetpretask/1/', 'taskspacerwithdetails/1/', 'search/1/', 'diversityposttask/1/','systemdiversityposttask/1/',
        'taskspacer',
    'snippetpretask/2/','taskspacerwithdetails/2/','search/2/', 'diversityposttask/2/','systemdiversityposttask/2/',
        'taskspacer',
    'snippetpretask/3/','taskspacerwithdetails/3/', 'search/3/', 'diversityposttask/3/','systemdiversityposttask/3/',
     'taskspacer',
    'snippetpretask/4/','taskspacerwithdetails/4/', 'search/4/', 'diversityposttask/4/','systemdiversityposttask/4/',
    'taskspacer', 'diversityexitsurvey/', 'diversityperformance/', 'endexperiment/',
    'logout/'
]



test_flow = [
    'startexperiment/', 'preexperiment/UK/', 'search/1/', 'search/2/','search/3/', 'search/4/',
    #'demographicssurvey/', 'pst-findas/', 'pst-numbers/', 'taskspacer',
    'perceptionsurvey/', 'nasasurvey/', 'systemsurvey/', 'personalitysurvey/',
    'prepracticetask/0/', 'search/0/', 'postpracticetask/0/', 'taskspacer/',
    'pretaskquestions/1/', 'taskspacerwithdetails/1/', 'taskspacer',
    'pretaskquestions/2/', 'taskspacerwithdetails/2/', 'taskspacer',
    'pretaskquestions/3/', 'taskspacer',
    'pretaskquestions/4/',
    'endexperiment/',
    'logout/'
]

test_flow2 = [
    'startexperiment/', 'preexperiment/UK/',
    #'demographicssurvey/', 'pst-findas/', 'pst-numbers/', 'personalitysurvey/', 'taskspacer',

    'prepracticetask/0/', 'search/0/', 'postpracticetask/0/', 'taskspacer/',

    'pretaskquestions/1/', 'taskspacerwithdetails/1/', 'search/1/',
    'perceptionsurvey/1/', 'systemsurvey/1/', 'conceptlistingsurvey/1/1/',
    'taskspacer',
    'search/2/','search/3/', 'search/4/',
    'endexperiment/',
    'logout/'
]





pst_flow = [
    'startexperiment/', 'pst-findas/','taskspacer','pst-numbers/', 'endexperiment/', 'logout/'
]



suggestion_trie = None
"""
suggestion_trie = AutocompleteTrie(
    min_occurrences=3,
    suggestion_count=8,
    include_stopwords=False,
    stopwords_path=os.path.join(work_dir, "data/stopwords.txt"),
    vocab_path=os.path.join(work_dir, "data/vocab.txt"),
    vocab_trie_path=os.path.join(work_dir, "data/vocab_trie.dat"))
"""

search_engine = Whooshtrec(
    whoosh_index_dir=my_whoosh_doc_index_dir,
    stopwords_file=stopword_file,
    model=1,
    newschema=True)

search_engine.key_name = 'bm25'
search_engine.set_fragmenter(frag_type=2, surround=40)


exp_sigir2019 = ExperimentSetup(
    workflow=test_flow2,
    engine=search_engine,
    practice_topic='367',
    topics=['347', '341', '435', '408'],
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='BM25 - interfaces with different Ads',
    trie=suggestion_trie,
    autocomplete=False,
    timeout=[150, 600, 600, 600, 600])  # 300s = 5min; 600s = 10min; 1200s = 20min



exp_pst = ExperimentSetup(
    workflow=pst_flow,
    engine=search_engine,
    practice_topic='367',
    topics=['347', '341', '435', '408'],
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='standard condition bm25 test',
    trie=suggestion_trie,
    autocomplete=False,
    timeout=[150, 600, 600, 600, 600])  # 300s = 5min; 600s = 10min; 1200s = 20min


# these correspond to conditions
experiment_setups = [exp_sigir2019, exp_pst]
