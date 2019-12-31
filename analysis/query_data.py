#
# Updated query_data (per query statistics) script for SIGIR 2020.
# Updated by David Maxwell on 12-30-2019
#

import os
import sys

# As we are using ifind mashed into this repository, we need to add that to our path before we can import from it.
path_cwd = os.getcwd()
path_levelup = os.path.abspath(os.path.join(path_cwd, '..'))
path_treconomics_base = os.path.join(path_levelup, 'treconomics_project')
sys.path.append(path_treconomics_base)
# End appending of treconomics_project path

from datetime import datetime, timedelta
from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from ifind.search.engines.whooshtrec import Whooshtrec
from ifind.search import Query, Response

from exp_time_log_reader import ExpTimeLogReader
from utils import get_query_performance_metrics, get_time_diff, is_relevant

PAGE_SIZE = 10

KEY = 'username condition interface taskid topic actions no_pages doc_count doc_depth doc_rel_count doc_rel_depth hover_count hover_trec_rel_count hover_trec_nonrel_count hover_depth doc_trec_rel_count doc_trec_nonrel_count doc_clicked_trec_rel_count doc_clicked_trec_nonrel_count query_time system_query_delay session_time document_time serp_lag new_total_serp pat1 pat2 pat3 pat4 pat5 pat10 pat15 pat20 pat25 pat30 pat40 pat50 rprec total_trec_rel_docs doc_trec_unjudged_count task_view_clicks ads_raw_hover_total ads_raw_hover_top ads_raw_hover_bot ads_raw_hover_side ads_unique_hover_total ads_unique_hover_top ads_unique_hover_bot ads_unique_hover_side ads_clicks_raw_sum ads_clicks_top_doc ads_clicks_bot_doc ads_clicks_side_doc ads_clicks_top_serp ads_clicks_bot_serp ads_clicks_side_serp'

print(KEY)

class QueryLogEntry(object):
    
    def __init__(self, key, vals, qrel_handler, engine=None, query_time=0):
        self.key = key
        self.qrel_handler = qrel_handler
        
        # Get the query terms -- we need these to run the query again and get performance.
        self.query = vals[10:]
        
        if self.query == '':
            # There's quote marks at the start and end of the query, remove them
            self.query[0] = self.query[0][1:]
            self.query[-1] = self.query[-1][:-1]
        
        # "Traditional" SERP components
        self.topic = vals[8]
        self.event_count = 0
        self.doc_count = 0
        self.doc_depth = 0
        self.hover_count = 0  # Added by David
        self.hover_depth = 0  # Added by David
        self.hover_trec_rel_count = 0
        self.hover_trec_nonrel_count = 0
        self.doc_rel_count = 0
        self.doc_marked_list = []
        self.doc_unmarked_list = []
        self.doc_rel_depth = 0
        self.doc_trec_rel_count = 0  # Records documents MARKED that are trec rel
        self.doc_trec_nonrel_count = 0  # Records documents MARKED that are not trec rel
        self.doc_trec_unjudged_count = 0 # Records documents MARKED that are UNJUDGED in the trec qrels
        self.pages = 0
        self.curr_page = 1
        self.session_start_time = '{date} {time}'.format(date=vals[0],time=vals[1])
        self.session_end_time = None
        self.query_time = query_time
        self.session_time = 0.0
        self.snippet_time = 0.0
        self.document_time = 0.0
        self.view_serp_time = 0
        self.last_serp_view_time = None  # Added by David
        self.curr_event = None
        self.last_event = None
        self.last_interaction_event = None
        self.last_interaction_time = None
        self.last_last_event = None
        self.doc_click_time = False
        self.task_view_clicks = 0

        # Probability variables, added by David (2016-11-30)
        self.doc_clicked_trec_rel_count = 0
        self.doc_clicked_trec_nonrel_count = 0
        
        self.query_response = None  # Stores the results for parsing later on.
        
        # Testing by David for new SERP
        self.last_serp_event = None
        self.new_total_serp = 0.0
        
        # Additional attributes to store details on system lag and imposed delays
        self.serp_lag_calculated_for = []  # Added by David, list of times for the queries we've worked out lag for!
        self.serp_lag = 0.0  # Added by David
        
        self.last_query_delay_time = None
        self.imposed_query_delay = 0.0
        self.system_query_delay = 0.0
        self.total_query_duration = 0.0
        self.last_document_delay_time = None
        self.imposed_document_delay = 0.0
        self.document_lag = 0.0

        # Advert hover and clicks
        self.ad_hovers_raw = {'ad-top': 0, 'ad-side': 0, 'ad-bot': 0} # The raw count of hover events for each of the ad positions.
        self.ad_hovers_unique = {'ad-top': 0, 'ad-side': 0, 'ad-bot': 0} # Hovers on adverts that are unique (i.e. no repeats on the same advert).
        self.ad_hovers_seen = [] # A list of the advert IDs that have been hovered over (helps with calculating ad_hovers_unique).

        self.ad_clicks_raw = {'top-lp': 0, 'bot-lp': 0, 'side-lp': 0, 'top-rp': 0, 'bot-rp': 0, 'side-rp': 0} # The raw count of clicks on adverts in each of the positions.
        
        # issue query to whoosh and get performance values
        self.p = []
        self.perf = ['0.0  ' * 14]
        
        if engine:
            q = Query(' '.join(self.query))
            q.skip = 1
            q.top = 1000
            (un,cond,interface,taskid,topicnum) = key.split(' ')
            #print "Issuing {0}".format(q.terms)
            
            response = engine.search(q)  # Search using BM25.
            
            self.perf = get_query_performance_metrics(self.qrel_handler, response.results, topicnum)
            self.query_response = response
            
        self.last_event='QUERY_ISSUED'
        self.last_time = '{date} {time}'.format(date=vals[0],time=vals[1])
    
    def __str__(self):
        q = ' '.join(self.query)
        
        performances = ' '.join(self.perf)
        serp_time = self.view_serp_time + self.snippet_time
        
        counts = "{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10} {11} {12}".format(
            self.pages,
            self.doc_count,
            self.doc_depth,
            self.doc_rel_count,
            self.doc_rel_depth,
            self.hover_count,
            self.hover_trec_rel_count,
            self.hover_trec_nonrel_count,
            self.hover_depth,
            self.doc_trec_rel_count,
            self.doc_trec_nonrel_count,
            self.doc_clicked_trec_rel_count,
            self.doc_clicked_trec_nonrel_count
        )
        
        times = "{0} {1} {2} {3} {4} {5}".format(
            self.query_time, self.system_query_delay, self.session_time, self.document_time, self.serp_lag, self.new_total_serp
        )
        
        task_view_str = str(self.task_view_clicks)

        ad_details_str = self.generate_ad_details_str()
        
        s = "{0} {1} {2} {3} {4} {5}".format(counts, times, performances, self.doc_trec_unjudged_count, task_view_str, ad_details_str)
        return s
    
    def generate_ad_details_str(self):
        """
        Generates a string of summary details relating to advert hovers and clicks.
        """
        hovers_raw_sum = self.ad_hovers_raw['ad-top'] + self.ad_hovers_raw['ad-bot'] + self.ad_hovers_raw['ad-side']
        hovers_unique_sum = self.ad_hovers_unique['ad-top'] + self.ad_hovers_unique['ad-bot'] + self.ad_hovers_unique['ad-side']

        clicks_raw_sum = self.ad_clicks_raw['top-lp'] + self.ad_clicks_raw['bot-lp'] + self.ad_clicks_raw['side-lp'] + self.ad_clicks_raw['top-rp'] + self.ad_clicks_raw['bot-rp'] + self.ad_clicks_raw['side-rp']

        return f"{hovers_raw_sum} {self.ad_hovers_raw['ad-top']} {self.ad_hovers_raw['ad-bot']} {self.ad_hovers_raw['ad-side']} {hovers_unique_sum} {self.ad_hovers_unique['ad-top']} {self.ad_hovers_unique['ad-bot']} {self.ad_hovers_unique['ad-side']} {clicks_raw_sum} {self.ad_clicks_raw['top-lp']} {self.ad_clicks_raw['bot-lp']} {self.ad_clicks_raw['side-lp']} {self.ad_clicks_raw['top-rp']} {self.ad_clicks_raw['bot-rp']} {self.ad_clicks_raw['side-rp']}"

    def update_times(self, curr_time):

        #print curr_time, self.last_time, get_time_diff(self.last_time, curr_time)

        if self.curr_event == 'DELAY_RESULTS_PAGE':
            self.serp_lag = get_time_diff(self.session_start_time, curr_time)
            self.last_query_delay_time = curr_time

        if self.curr_event == 'QUERY_COMPLETE':  # Was VIEW_SEARCH_RESULTS_PAGE
            if self.last_event == 'DELAY_RESULTS_PAGE':
                self.imposed_query_delay = get_time_diff(self.last_query_delay_time, curr_time)
            #if self.last_event == 'QUERY_END':  # Was QUERY_ISSUED
            #    self.serp_lag = get_time_diff(self.session_start_time, curr_time)
        
        if self.system_query_delay == 0.0 and self.curr_event == 'QUERY_END' and self.last_event == 'QUERY_START':
            self.system_query_delay = self.system_query_delay + get_time_diff(self.last_time, curr_time)

        if self.curr_event == 'DOCUMENT_DELAY_VIEW':
            # Document delay occurred, so track the time this happened at.
            self.last_document_delay_time = curr_time
            self.view_serp_time = self.view_serp_time + get_time_diff(self.last_time, curr_time)

        if self.curr_event == 'DOC_MARKED_VIEWED':
            if self.last_document_delay_time:
                if get_time_diff(self.last_document_delay_time, curr_time) < 10.0:
                    self.imposed_document_delay += get_time_diff(self.last_document_delay_time, curr_time)
                else:
                    self.view_serp_time += get_time_diff(self.last_time, curr_time)
            else:
                self.view_serp_time += get_time_diff(self.last_time, curr_time)

        if self.curr_event in ['DOCUMENT_HOVER_OUT', 'DOCUMENT_HOVER_IN', 'QUERY_FOCUS','VIEW_SAVED_DOCS','VIEW_TASK' ]:
            self.view_serp_time = self.view_serp_time + get_time_diff(self.last_time, curr_time)

        # This could be more robust.
        # What if the searcher were to view the list of documents marked, or view the task, whilst viewing a document?
        # Maybe this functionality should be disabled while a document is being viewed.
        # Commented out by DMAX on June 8th 2016 - replaced with more robust document time measures (see below).        
        #if self.last_event in ['DOC_MARKED_VIEWED','DOC_MARKED_RELEVANT','DOC_MARKED_NONRELEVANT']:
            #    self.document_time = self.document_time + get_time_diff(self.last_time, curr_time)
        
        # DMAX - Added new document time measures (June 8th 2016)
        # self.doc_click_time contains the document click time. Set to False otherwise.
        if not self.doc_click_time and self.curr_event == 'DOC_CLICKED':
            self.doc_click_time = curr_time
        
        # Added in VIEW_SAVED_DOCS to cater for the event where a searcher flips to the saved document screen instead.
        if self.doc_click_time and self.curr_event in ['QUERY_START', 'VIEW_SAVED_DOCS', 'PRACTICE_SEARCH_TASK_COMPLETED','TASK_ENDED','SESSION_COMPLETED','EXPERIMENT_TIMEOUT','SNIPPET_POSTTASK_SURVEY_STARTED','SEARCH_TASK_COMPLETED']:
            self.document_time = self.document_time + get_time_diff(self.doc_click_time, curr_time)
            self.doc_click_time = False
        # DMAX - End new document time measures
        
        # DMAX - Adding in new SERP details
        if not self.last_serp_event and self.curr_event == 'VIEW_SEARCH_RESULTS_PAGE':
            self.last_serp_event = curr_time
        #elif self.last_serp_event and self.curr_event == 'QUERY_FOCUS':
        #    print 'QF', curr_time
        elif self.last_serp_event and self.curr_event not in ['DOCUMENT_HOVER_IN', 'DOCUMENT_HOVER_OUT']:
            self.new_total_serp = self.new_total_serp + get_time_diff(self.last_serp_event, curr_time)
            self.last_serp_event = None
        # DMAX - End new SERP details
        
        # DMAX - Updated SERP lag time
        if self.curr_event == 'QUERY_END' and self.last_event == 'QUERY_START':
            self.serp_lag = self.serp_lag + get_time_diff(self.last_time, curr_time)
        # DMAX - End updated SERP lag time
    
    
    def end_query_session(self,end_time):
        # DMAX added in this condition to take the first event only.
        # Subsequent events add overhead to the time - that isn't strictly part of the session.
        if self.session_end_time is None:
                
                # Added by David on December 13, 2016
                # Last events (e.g. EXPERIMENT_TIMEOUT) should not be considered as the final session event.
                # Some people in the experiment walk away (or something) for several minutes, meaning that times are way out.
                # In this case, we roll back to the last interaction event - where the event is not EXPERIMENT_TIMEOUT or SESSION_COMPLETED.
                end_time = self.last_interaction_time
                self.session_end_time = end_time
                
                # print "END EVENT: {0}".format(self.last_interaction_event)
                # print "END TIME: {0}".format(self.last_interaction_time)
                
                self.session_time = get_time_diff(self.session_start_time, end_time)
            #print "session time", self.session_time
        
                self.update_times(end_time)
            #if self.last_event == 'VIEW_SEARCH_RESULTS_PAGE':
            #    self.snippet_time = self.snippet_time + get_time_diff(self.view_serp_time, end_time)
        
        # Adding some code to work out probabilities for clicking!
        relevant_count = 0
        
        for i in range(0, self.hover_depth):
            if self.hover_depth > len(self.query_response.results):
                continue
        
            if self.qrel_handler.get_value(self.topic, self.query_response.results[i].docid.decode('utf-8')) > 0:
                relevant_count = relevant_count + 1
            
        for i in range(0, self.hover_depth):
            docid_at_rank = self.query_response.results[i].docid.decode('utf-8')
            qrel_judgement = is_relevant(self.qrel_handler, self.topic, docid_at_rank)
            
            if qrel_judgement >= 1:
                self.hover_trec_rel_count = self.hover_trec_rel_count + 1
            else:
                self.hover_trec_nonrel_count = self.hover_trec_nonrel_count + 1
            
            # if is_relevant(self.qrel_handler, self.topic, docid_at_rank) <= 0:
            #     self.hover_trec_nonrel_count = self.hover_trec_nonrel_count + 1
            # else:
            #     self.hover_trec_rel_count = self.hover_trec_rel_count + 1
     
    def process(self, vals):
        self.event_count = self.event_count + 1
        self.curr_event = vals[9]
        self.update_times('{date} {time}'.format(date=vals[0],time=vals[1]))
        
        if 'VIEW_SEARCH_RESULTS_PAGE' in vals:
            n = 1
            if len(vals) == 11:
                n = int(vals[10])
            
            if self.pages < n:
                self.pages = n
            self.curr_page = n
        
        # When the "View Task" link is pushed.
        if 'VIEW_TASK' in vals:
            self.task_view_clicks += 1

        if 'DOC_MARKED_VIEWED' in vals:
            m = int(vals[14])
            #n = (self.curr_page - 1)* PAGE_SIZE + m
            if self.doc_depth < m:
                self.doc_depth = m

            self.doc_count = self.doc_count + 1
            qrel_judgement = is_relevant(self.qrel_handler, vals[8], vals[11])
            
            if qrel_judgement >= 1:
                self.doc_clicked_trec_rel_count = self.doc_clicked_trec_rel_count + 1
            else:
                self.doc_clicked_trec_nonrel_count = self.doc_clicked_trec_nonrel_count + 1
            
            # if is_relevant(self.qrel_handler, vals[7], vals[10]) <= 0:
            #     self.doc_clicked_trec_nonrel_count = self.doc_clicked_trec_nonrel_count + 1
            # else:
            #     self.doc_clicked_trec_rel_count = self.doc_clicked_trec_rel_count + 1
        
        if 'DOCUMENT_HOVER_IN' in vals:
            try:
                m = int(vals[-1])
                self.hover_count += 1
            
                if m > self.hover_depth:
                    self.hover_depth = m
            except ValueError: # Assume that an advert has been hovered over (either ad-top, ad-side, ad-bot)
                self.ad_hovers_raw[vals[-1]] = self.ad_hovers_raw[vals[-1]] + 1

                # Calculate unique hovers (i.e. hover events for ads that have not been hovered over before)
                ad_id = vals[-3]

                if ad_id not in self.ad_hovers_seen:
                    self.ad_hovers_seen.append(ad_id)
                    self.ad_hovers_unique[vals[-1]] = self.ad_hovers_unique[vals[-1]] + 1

        if 'AD_CLICKED' in vals:
            ad_position = vals[-4]
            ad_id = vals[-5]

            self.ad_clicks_raw[ad_position] = self.ad_clicks_raw[ad_position] + 1

            # Possible position values
            # 'top-lp' is on DOC
            # 'bot-lp' is on DOC
            # 'side-lp' is on DOC

            # 'top-rp' is on SERP
            # 'bot-rp' is on SERP
            # 'side-rp' is on SERP
        
        if 'DOC_MARKED_RELEVANT' in vals:
            r = int(vals[13])
            if r > 0:
                self.doc_rel_count = self.doc_rel_count + 1
                self.doc_marked_list.append(vals[11])
                qrel_judgement = is_relevant(self.qrel_handler, vals[8], vals[11])
                m = int(vals[14]) # The ranking depth
                
                if qrel_judgement >= 1:
                    self.doc_trec_rel_count = self.doc_trec_rel_count + 1
                else:
                    self.doc_trec_nonrel_count = self.doc_trec_nonrel_count + 1
                    
                    if qrel_judgement == -1:
                        self.doc_trec_unjudged_count = self.doc_trec_unjudged_count + 1
                
                if self.doc_rel_depth < m:
                    self.doc_rel_depth = m
        
        if 'DOC_MARKED_NONRELEVANT' in vals:
            self.doc_unmarked_list.append(vals[11])
                    
        self.last_last_event = self.last_event
        self.last_event = vals[9]
        self.last_time = '{date} {time}'.format(date=vals[0], time=vals[1])
        
        # When the task finished, what are we looking for?
        if (vals[8] not in ['CONCEPT_LISTING_COMPLETED', 'TASK_COMPLETED', 'PRACTICE_SEARCH_TASK_COMPLETED']):
            self.last_interaction_event = vals[9]
            self.last_interaction_time = '{date} {time}'.format(date=vals[0], time=vals[1])

class ExpLogEntry(object):

    def __init__(self, key, qrel_handler, engine=None):
        self.qrel_handler = qrel_handler
        self.key = key
        self.title = ''
        self.state = ''
        self.event_count = 0
        self.queries = []
        self.current_query = None
        self.last_event_time = None
        self.last_query_focus_time = None
        self.engine = engine
        self.query_ended_previously = False

    def __str__(self):
        
        s = ""
        for q in self.queries:
            sq = "%s %d %s\n" % (self.key, self.event_count, str(q))
            if len(sq) > 5:
                s = s + sq
        return s.strip()

    def getTitle(self):
        return self.title

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        

    def process(self, vals):
        self.event_count = self.event_count + 1

        #self.last_event_time
        # We want to measure query time from the last QUERY_FOCUS event.
        # We could do it from the first, but we decided this could be too unreliable...
        # So every time we see a new QUERY_FOCUS, we override what we have before and update the time accordingly.
        
        # Commented out this line so that this is overwritten
        #if self.last_query_focus_time is None:

        if ('QUERY_FOCUS' in vals):
            self.last_query_focus_time = '{date} {time}'.format(date=vals[0],time=vals[1])

        if self.last_query_focus_time is None:
            if ('VIEW_SEARCH_BOX' in vals):
                self.last_query_focus_time = '{date} {time}'.format(date=vals[0],time=vals[1])
        
        # End de-dentation

        
        if ('QUERY_ISSUED' in vals):
            # new query, create a query log entry
            if self.current_query:
                if self.last_query_focus_time:
                    lqft = self.last_query_focus_time
                else:
                    lqft = self.last_event_time  # We didn't see a FOCUS or VIEW_SEARCH_BOX, so fallback to last event time.

                self.current_query.end_query_session(lqft)

            #print "QUERY ISSUED:", vals[8:]
            #print self.last_query_focus_time, ':::', vals[1], ':::', get_time_diff(self.last_query_focus_time, vals[1])
            #print
            if self.last_query_focus_time is None:
                self.last_query_focus_time = self.last_event_time
            
            self.current_query = QueryLogEntry(self.key, vals, self.qrel_handler, self.engine, get_time_diff(self.last_query_focus_time, '{date} {time}'.format(date=vals[0],time=vals[1])))
            self.last_query_focus_time = None
            self.query_ended_previously = False
            self.queries.append(self.current_query)
        else:
            if self.current_query:
                # process result under this query object
                self.current_query.process(vals)
        
        # probably should put a condition on this (start task, doc viewed, view serp, etc, ) not all/any
        self.last_event_time = '{date} {time}'.format(date=vals[0],time=vals[1])

        event = vals[9]
        if event in ['PRACTICE_SEARCH_TASK_COMPLETED','TASK_COMPLETED','CONCEPT_LISTING_COMPLETED']:
            #print 'search task complete - event'
            if self.current_query and not self.query_ended_previously:
                #print "end of search session"
                self.current_query.end_query_session('{date} {time}'.format(date=vals[0],time=vals[1]))
                self.query_ended_previously = True
        
        # Code for removing documents that were previously marked, but are then reselected as non-relevant.
        all_docs_unmarked = []
        
        for query_object in self.queries:
            all_docs_unmarked = all_docs_unmarked + query_object.doc_unmarked_list
            query_object.doc_unmarked_list = []
        
        topic = self.key.split(' ')[4]
        
        for query_object in self.queries:
            for docid in all_docs_unmarked:
                if docid in query_object.doc_marked_list:
                    query_object.doc_marked_list.remove(docid)
            
            query_object.doc_rel_count = len(query_object.doc_marked_list)
            query_object.doc_trec_unjudged_count = 0
            query_object.doc_trec_nonrel_count = 0
            query_object.doc_trec_rel_count = 0
            
            for docid in query_object.doc_marked_list:
                qrel_judgement = is_relevant(self.qrel_handler, topic, docid)
                
                if qrel_judgement >= 1:
                    query_object.doc_trec_rel_count = query_object.doc_trec_rel_count + 1
                else:
                    query_object.doc_trec_nonrel_count = query_object.doc_trec_nonrel_count + 1
                    
                    if qrel_judgement == -1:
                        query_object.doc_trec_unjudged_count = query_object.doc_trec_unjudged_count + 1
                
                # if is_relevant(self.qrel_handler, topic, docid) <= 0:
                #     query_object.doc_trec_nonrel_count = query_object.doc_trec_nonrel_count + 1
                # else:
                #     query_object.doc_trec_rel_count = query_object.doc_trec_rel_count + 1
            
        
        # for query_object in self.queries:
        #     for docid in all_docs_unmarked:
        #         if docid in query_object.doc_marked_list:
        #             topic = self.key.split(' ')[4]
        #
        #             query_object.doc_marked_list.remove(docid)
        #             query_object.doc_rel_count = query_object.doc_rel_count - 1
        #
        #             if is_relevant(self.qrel_handler, topic, docid) == 0:
        #                 query_object.doc_clicked_trec_nonrel_count = query_object.doc_clicked_trec_nonrel_count - 1
        #             else:
        #                 query_object.doc_clicked_trec_rel_count = query_object.doc_clicked_trec_rel_count - 1
            
def main():
    if len(sys.argv) == 5:
        filename = sys.argv[1]
        qrels = TrecQrelHandler(sys.argv[2])
        my_whoosh_doc_index_dir = sys.argv[3]
        stopword_file = sys.argv[4]

        # Create a search engine like in experiment_configuration.py.
        search_engine = Whooshtrec(
            whoosh_index_dir=my_whoosh_doc_index_dir,
            stopwords_file=stopword_file,
            model=1,
            newschema=True,
            implicit_or=True)
        
        search_engine.key_name = 'bm25'
        search_engine.set_fragmenter(frag_type=2, surround=40)
        search_engine.set_model(1, pval=0.75)
        # End create search engine

        elr = ExpTimeLogReader(ExpLogEntry, qrels, search_engine)
        elr.process(filename)
        elr.report(False)
    else:
        print(f"{sys.argv[0]} <logfile> <qrelsfile> <indexpath> <stopwordsfile>")

if __name__ == "__main__":
    sys.exit(main())
