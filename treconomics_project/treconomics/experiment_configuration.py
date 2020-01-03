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

# getcwd() doesn't seem to work on the droplet; hardcode the path.
if socket.gethostname() == 'treconomics-server':
    work_dir = '/home/treconomics/treconomics_2/treconomics_project/'

#my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/fullindex/')
my_whoosh_doc_index_dir = os.path.join(work_dir, 'data/nytindex3/')

my_whoosh_query_index_dir = os.path.join(work_dir, "/trec_query_index/index")
my_experiment_log_dir = work_dir
qrels_file = os.path.join(work_dir, "data/sorted.nyt.aq.qrels")
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

sigir2020_flow = [
    'startexperiment/', 'preexperiment/UK/',
    'demographicssurvey/',
    'prepracticetask/0/', 'search/0/', 'postpracticetask/0/',
    'taskspacer2/0/',
    'pst-findas/',
    'taskspacer2/pst/',
    'pretaskquestions/1/', 'taskspacerwithdetails/1/', 'search/1/', 'conceptlistingsurvey/1/1/', 'posttaskquestions/1/',
    'perceptionsurvey/1/', 'systemsurvey/1/',
    'taskspacer2/1/',
    'pretaskquestions/2/', 'taskspacerwithdetails/2/', 'search/2/', 'conceptlistingsurvey/2/1/', 'posttaskquestions/2/',
    'perceptionsurvey/2/', 'systemsurvey/2/',
    'taskspacer2/2/',
    'pretaskquestions/3/', 'taskspacerwithdetails/3/', 'search/3/', 'conceptlistingsurvey/3/1/', 'posttaskquestions/3/',
    'perceptionsurvey/3/', 'systemsurvey/3/',
    'taskspacer2/3/',
    'pretaskquestions/4/', 'taskspacerwithdetails/4/', 'search/4/', 'conceptlistingsurvey/4/1/', 'posttaskquestions/4/',
    'perceptionsurvey/4/', 'systemsurvey/4/',
    'taskspacer2/4/',
    'pst-numbers/',
    'personalitysurvey/',
    'overall/',
    'performance/',
    'endexperiment/',
    'logout/'
]


sigir2020_reduced_flow = [
    'startexperiment/', 'preexperiment/UK/',
    'taskspacer', 'overall/', 'conceptlistingsurvey/1/1/',
    'prepracticetask/0/', 'search/0/', 'postpracticetask/0/','taskspacer2/0/',
    'taskspacerwithdetails/1/', 'search/1/', 'taskspacer2/1/',
    'taskspacerwithdetails/2/', 'search/2/','taskspacer2/2/',
    'taskspacerwithdetails/3/', 'search/3/', 'taskspacer2/3/',
    'taskspacerwithdetails/4/', 'search/4/', 'taskspacer2/4/',
    'performance/','performance/','performance/',
    'endexperiment/',
    'logout/'
]

#sigir2020_flow = sigir2020_reduced_flow




pst_flow = [
    'startexperiment/', 'pst-numbers/', 'pst-findas/','taskspacer','endexperiment/', 'logout/'
]



suggestion_trie = None

suggestion_trie = AutocompleteTrie(
    min_occurrences=3,
    suggestion_count=8,
    include_stopwords=False,
    stopwords_path=os.path.join(work_dir, "data/stopwords.txt"),
    vocab_path=os.path.join(work_dir, "data/vocab.txt"),
    vocab_trie_path=os.path.join(work_dir, "data/vocab_trie.dat"))

search_engine = Whooshtrec(
    whoosh_index_dir=my_whoosh_doc_index_dir,
    stopwords_file=stopword_file,
    model=1,
    newschema=True,
    implicit_or=True)

search_engine.key_name = 'bm25'
search_engine.set_fragmenter(frag_type=2, surround=40)
search_engine.set_model(1, pval=0.75)


timeouts = [240, 480, 480, 480, 480]
topics_a = ['347', '341', '435', '408']
topics_b = ['341', '347', '408','435']

topics_c = ['435', '408', '347', '341']
topics_d = ['408', '435', '341', '347']



exp_sigir2020a = ExperimentSetup(
    workflow=sigir2020_flow ,
    engine=search_engine,
    practice_topic='367',
    topics=topics_a,
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='BM25 - interfaces with different Ads',
    trie=suggestion_trie,
    autocomplete=True,
    timeout=timeouts)  # 300s = 5min; 600s = 10min; 1200s = 20min


exp_sigir2020b = ExperimentSetup(
    workflow=sigir2020_flow ,
    engine=search_engine,
    practice_topic='367',
    topics=topics_b,
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='BM25 - interfaces with different Ads',
    trie=suggestion_trie,
    autocomplete=True,
    timeout=timeouts)  # 300s = 5min; 600s = 10min; 1200s = 20min


exp_sigir2020c = ExperimentSetup(
    workflow=sigir2020_flow ,
    engine=search_engine,
    practice_topic='367',
    topics=topics_c,
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='BM25 - interfaces with different Ads',
    trie=suggestion_trie,
    autocomplete=True,
    timeout=timeouts)  # 300s = 5min; 600s = 10min; 1200s = 20min


exp_sigir2020d = ExperimentSetup(
    workflow=sigir2020_flow,
    engine=search_engine,
    practice_topic='367',
    topics=topics_d,
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='BM25 - interfaces with different Ads',
    trie=suggestion_trie,
    autocomplete=True,
    timeout=timeouts)  # 300s = 5min; 600s = 10min; 1200s = 20min


exp_sigir2020test = ExperimentSetup(
    workflow=sigir2020_flow,
    engine=search_engine,
    practice_topic='367',
    topics=topics_d,
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='BM25 - interfaces with different Ads',
    trie=suggestion_trie,
    autocomplete=True,
    timeout=timeouts)  # 300s = 5min; 600s = 10min; 1200s = 20min





exp_pst = ExperimentSetup(
    workflow=pst_flow,
    engine=search_engine,
    practice_topic='367',
    topics=topics_a,
    rpp=10,
    practice_interface=4,
    interface=[1, 2, 3, 4],
    rotation_type=1,
    description='standard condition bm25 test',
    trie=suggestion_trie,
    autocomplete=False,
    timeout=[150, 600, 600, 600, 600])  # 300s = 5min; 600s = 10min; 1200s = 20min


# these correspond to conditions
#CONDITIONS
experiment_setups = [exp_pst, exp_sigir2020a, exp_sigir2020b, exp_sigir2020c, exp_sigir2020d, exp_sigir2020test]


user_conditions = []
for topic_rotation in range(1,5):
    for interface_rotation in range(0,12):
        user_conditions.append([topic_rotation, interface_rotation])

# add additional user conditions here.
user_conditions.append([1,10])
user_conditions.append([1,1])
user_conditions.append([1,3])
user_conditions.append([2,0])
user_conditions.append([2,1])
user_conditions.append([2,2])
#
user_conditions.append([2,3])
user_conditions.append([2,4])
user_conditions.append([2,5])
user_conditions.append([2,6])
user_conditions.append([2,7])
user_conditions.append([2,8])
user_conditions.append([2,9])
user_conditions.append([2,10])

# Must get next
user_conditions.append([3,1])
user_conditions.append([4,7])
user_conditions.append([4,11])
user_conditions.append([3,7])
user_conditions.append([4,2])
user_conditions.append([4,5])

user_conditions.append([3,1])
user_conditions.append([4,7])
user_conditions.append([4,11])
user_conditions.append([3,7])
user_conditions.append([4,2])
user_conditions.append([4,5])

user_conditions.append([2,2])


user_conditions.append([4,5])
user_conditions.append([4,5])
user_conditions.append([4,2])
user_conditions.append([4,11])
user_conditions.append([4,5])
user_conditions.append([4,2])
user_conditions.append([4,11])
user_conditions.append([4,5])
user_conditions.append([4,2])
user_conditions.append([4,11])
user_conditions.append([4,5])
user_conditions.append([4,2])
user_conditions.append([4,11])
user_conditions.append([4,5])
user_conditions.append([4,5])
user_conditions.append([4,2])
user_conditions.append([4,11])
user_conditions.append([4,5])
user_conditions.append([4,2])
user_conditions.append([4,11])




#print(user_conditions)


#print("For condition 1(a)")
#for r in range(0, 13):
#    print ("User on Rotation", r)
#    for t in range(0, 5):
#        des = exp_sigir2020a.get_exp_dict(t, r)
#        print("Taskno: {} Rotation: {} Topic: {} Interface:  {}".format(t,  r, des['topic'], des['interface']))
