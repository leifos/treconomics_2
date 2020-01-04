#
# Log parser mark II (revised from previous iteration)
# Used for SIGIR 2020 experiment
# Kill me
#
# Author: David Maxwell
# Date: 2020-01-04
#

import os
import sys

# As we are using ifind mashed into this repository, we need to add that to our path before we can import from it.
path_cwd = os.getcwd()
path_levelup = os.path.abspath(os.path.join(path_cwd, '..'))
path_treconomics_base = os.path.join(path_levelup, 'treconomics_project')
sys.path.append(path_treconomics_base)
# End appending of treconomics_project path

from ifind.search import Query
from ifind.search.engines.whooshtrec import Whooshtrec
from ifind.seeker.trec_qrel_handler import TrecQrelHandler
from utils import get_time_diff, get_query_performance_metrics

SEPARATOR = ','  # What does each column get separated by?
EVENT_SEARCH_SESSION_COMPLETE = 'SEARCH_TASK_COMPLETE'

# The unique key for identifying a user. Also used as the first portion of the output line.
KEY_LIST = ['username', 'condition', 'interface', 'task', 'topic']

# What do you want to output? Put the names of QueryLogEntry instance variables here and they will be output.
QUERY_SESSION_COLUMNS = ['time_system_query_delay',
                         'time_on_serp',
                         'time_on_documents',
                         'time_session_overall',
                         'clicks_on_view_task',
                         'serp_page_viewed_to',
                         'document_click_count',
                         'document_click_count_trec_rel',
                         'document_click_count_trec_nonrel',
                         'document_click_count_trec_unassessed',
                         'document_click_depth',
                         'document_click_depth_trec_rel',
                         'document_click_depth_trec_nonrel',
                         'document_click_depth_trec_unassessed',
                         'document_hover_count',
                         'document_hover_count_trec_rel',
                         'document_hover_count_trec_nonrel',
                         'document_hover_count_trec_unassessed',
                         'document_hover_depth',
                         'document_hover_depth_trec_rel',
                         'document_hover_depth_trec_nonrel',
                         'document_hover_depth_trec_unassessed',
                         'document_saved_count',
                         'document_saved_count_trec_rel',
                         'document_saved_count_trec_nonrel',
                         'document_saved_count_trec_unassessed',
                         'document_saved_depth',
                         'document_saved_depth_trec_rel',
                         'document_saved_depth_trec_nonrel',
                         'document_saved_depth_trec_unassessed',
                         'seen',
                         'seen_trec_rel',
                         'seen_trec_nonrel',
                         'seen_trec_unassessed',
                         'ad_hover_count',
                         'ad_hover_count_top',
                         'ad_hover_count_side',
                         'ad_hover_count_bot',
                         'ad_click_count',
                         'ad_click_count_top',
                         'ad_click_count_side',
                         'ad_click_count_bot',]

# What columns do you want for the performance side of things? Put them here.
PERFORMANCE_COLUMNS = ['p1',
                       'p2',
                       'p5',
                       'p10',
                       'p20',
                       'rprec',
                       'total_relevant_docs',]

class LogReader(object):
    """
    Class that provides the necessary mechanisms to parse the log file.
    """
    def __init__(self, log_entry_reader, qrel_handler, search_engine=None):
        self.log_entry_reader = log_entry_reader
        self.qrel_handler = qrel_handler
        self.search_engine = search_engine
        self.entries = {}
    
    def process(self, filename):
        if os.path.exists(filename):
            f = open(filename, 'r')

            for line in f:
                line = line.strip().split(' ')

                key_information = {
                    'username': line[3],
                    'condition': line[4],
                    'interface': line[5],
                    'task': line[7],
                    'topic': line[8],
                }

                action = line[9]

                key_str = ""

                # Generate the user/topic key string from KEY_LIST.
                for key in KEY_LIST:
                    if key_str == "":
                        key_str = f"{key_information[key]}"
                    else:
                        key_str = f"{key_str}{SEPARATOR}{key_information[key]}"

                # This line is to be ignored; as the wrong QRELs were used during the experiment, we cannot trust the values.
                if action == 'VIEW_PERFORMANCE':
                    continue
                
                if key_str in self.entries.keys():
                    entry = self.entries[key_str]
                else:
                    entry = self.log_entry_reader(key_str, self.qrel_handler, self.search_engine)
                
                entry.process(line)
                self.entries[key_str] = entry

            f.close()
            
            # Could do topic_summaries here.
            for key in self.entries.keys():
                pass
        else:
            raise FileNotFoundError(f"Log file {filename} cannot be found.")
    
    def report(self, show_key=False):
        """
        Reports back to stdout the results of the log parsing.
        If show_key, then a key of all the column names is also provided as the first line if output.
        The method makes use of the SEPARATOR variable to separate columns. Can switch between CSV/TSV by changing this variable.
        """
        pass
        if show_key:
            header_key = ""
            
            # Generate the key header string from the KEY_LIST.
            for key in KEY_LIST:
                if header_key == "":
                    header_key = f"{key}"
                else:
                    header_key = f"{header_key}{SEPARATOR}{key}"
            
            # Add in no_of_actions.
            header_key = f"{header_key}{SEPARATOR}no_of_actions"

            # Now add in the remaining columns from QueryLogEntry.
            for key in QUERY_SESSION_COLUMNS:
                header_key = f"{header_key}{SEPARATOR}{key}"
            
            # And finally, add in the performance column headers (if required).
            if self.search_engine:
                for key in PERFORMANCE_COLUMNS:
                    header_key = f"{header_key}{SEPARATOR}{key}"
            
            print(header_key)

        for key in self.entries.keys():
            print(self.entries[key])


class LogEntryReader(object):
    """
    Tracks information about a particular user's set of queries.
    For each query, a QueryLogEntry is created (and tracks specific details about the session).
    """
    def __init__(self, key, qrel_handler, search_engine=None):
        self.key = key
        self.qrel_handler = qrel_handler
        self.search_engine = search_engine

        self.event_count = 0
        self.queries = []
        self.current_query = None

        self.last_event_time = None
        self.last_query_focus_time = None
        self.query_ended_previously = False

    def process(self, line):
        """
        Handles the major query session start/end events.
        Looks for QUERY_FOCUS/VIEW_SEARCH_BOX events and QUERY_ISSUED events to track querying time.
        Also tracks SEARCH_TASK_COMPLETE events to end query sessions.
        """
        self.event_count += 1
        action = line[9]

        # If a query focus event happens, track the date/time - may be used for query time (if a query is issued!).
        if action == 'QUERY_FOCUS':
            self.last_query_focus_time = f'{line[0]} {line[1]}'
        
        # This is an alternative way to measure query time if the QUERY_FOCUS event does not get triggered.
        # Unlikely, but good to have.
        if self.last_query_focus_time is None and action == 'VIEW_SEARCH_BOX':
            self.last_query_focus_time = f'{line[0]} {line[1]}'
        
        # Now the important stuff -- when a query is issued, we need to track that.
        if action == 'QUERY_ISSUED':
            if self.current_query:
                if self.last_query_focus_time:
                    last_query_focus_time = self.last_query_focus_time
                # In a worst-case scenario, no QUERY_FOCUS or VIEW_SEARCH_BOX was logged; use the last event time as a fallback.
                else:
                    last_query_focus_time = self.last_event_time
                
                self.current_query.end_query_session(last_query_focus_time)
            
            # We need a fallback time if there is no prior query focus.
            if self.last_query_focus_time is None:
                self.last_query_focus_time = self.last_event_time
            
            # For a new query, create a QueryLogEntry to track all the interactions that take place within that query's session lifespan.
            time_diff = get_time_diff(self.last_query_focus_time, f"{line[0]} {line[1]}")
            self.current_query = QueryLogEntry(self.qrel_handler, self.key, line, search_engine=self.search_engine, query_time=time_diff)

            self.last_query_focus_time = None
            self.query_ended_previously = False
            self.queries.append(self.current_query)
        # Not a QUERY_ISSUED event, so we simply need to process what the line tells us.
        else:
            if self.current_query:  # Do we have a current query? This weeds out any prior surveys, etc.
                self.current_query.process(line)  # Process the line -- in the QueryLogEntry.
        
        # When the search task is completed (injected by preprocessor), end the query session, too.
        if action == EVENT_SEARCH_SESSION_COMPLETE and self.current_query and not self.query_ended_previously:
            self.current_query.end_query_session(f"{line[0]} {line[1]}")
            self.query_ended_previously = True
        
        self.last_event_time = f"{line[0]} {line[1]}"
    
    def __str__(self):
        return_str = ""

        for query in self.queries:
            return_str = f"{return_str}{self.key}{SEPARATOR}{self.event_count}{SEPARATOR}{query}{os.linesep}"

        return return_str.strip()


class QueryLogEntry(object):
    """
    For a query, tracks all the interactions that take place during that query's "lifespan".
    By "lifespan", we mean all the interactions from when the query was issued, to the next query issuance (or the entire search session ending).
    """
    def __init__(self, qrel_handler, key, line, search_engine=None, query_time=0):
        self.qrel_handler = qrel_handler
        self.search_engine = search_engine
        self.key = key

        # The line parameter we take allows us to extract the query terms.
        self.query = ' '.join(line[10:])
        self.query = self.query[1:]
        self.query = self.query[:-1]

        self.topic = line[8]

        self.last_event = None # Tracks the previous event.
        self.last_time = None  # Tracks the time of the previous event.
        self.last_last_event = None  # Tracks the previous previous event -- sometimes we need it!
        self.last_serp_event = None  # When did the last event related to the SERP take place?
        
        # Instance variables to store counts.
        self.event_count = 0  # How many events took place in this query session?
        self.clicks_on_view_task = 0  # How many times did the user click on the 'View Task' link (for the popup)?
        self.serp_page_viewed_to = 0  # What was the deepest SERP page viewed (i.e. the x of 'page x of y')?

        self.document_click_count = 0  # How many times were documents viewed (unique documents, ignoring the same clicked documents)?
        self.document_click_count_trec_rel = 0  # Same as above, but filtered for TREC relevant documents only.
        self.document_click_count_trec_nonrel = 0  # Same as above, but for TREC nonrel documents only.
        self.document_click_count_trec_unassessed = 0  # Same as above, but for unassessed documents (not TREC assessed).
        self.document_clicked_list = []  # What documents were clicked? Used to help the calculation above.

        self.document_click_depth = 0  # What was the greatest depth in the results that a document was clicked?
        self.document_click_depth_trec_rel = 0  # Same as above, but considering only TREC relevant documents.
        self.document_click_depth_trec_nonrel = 0  # Same as above, but considering only TREC nonrelevant documents.
        self.document_click_depth_trec_unassessed = 0  # Same as above, applying only to TREC unassessed documents.

        self.document_hover_count = 0  # The number of times a hover event occurs (ignoring documents that have been hovered before).
        self.document_hover_count_trec_rel = 0  # Same as above, but for only TREC relevant documents.
        self.document_hover_count_trec_nonrel = 0  # Same as above, but considering only TREC nonrelevant documents.
        self.document_hover_count_trec_unassessed = 0  # Same as above, but for TREC unassessed documents.
        self.document_hover_list = []  # The list of documents hovered over previously (used for the calculations above).

        self.document_hover_depth = 0  # The greatest depth for to which the subject hovered over a document snippet.
        self.document_hover_depth_trec_rel = 0  # Same as above, considering only TREC relevant documents.
        self.document_hover_depth_trec_nonrel = 0  # Same as above, considering only TREC nonrelevant documents.
        self.document_hover_depth_trec_unassessed = 0  # Same as above, considering only TREC unassessed documents.

        self.document_saved_count = 0  # How many documents were saved as relevant by the subject (marked)?
        self.document_saved_count_trec_rel = 0  # Subset of the above; TREC relevant, saved documents.
        self.document_saved_count_trec_nonrel = 0  # Subset of the above; TREC nonrelevant, saved documents.
        self.document_saved_count_trec_unassessed = 0  # Subset of the above; TREC unassessed, saved documents.
        self.document_saved_list = []  # A list of all the documents that have been saved.

        self.document_saved_depth = 0  # What was the greatest depth at which a document was saved?
        self.document_saved_depth_trec_rel = 0  # A subset of the above for TREC relevant documents only.
        self.document_saved_depth_trec_nonrel = 0  # A subset of the above for TREC nonrelevant documents only.
        self.document_saved_depth_trec_unassessed = 0  # A subset of the above for TREC unassessed documents only.

        self.seen = 0  # How many snippets have been seen by the subject?
        self.seen_trec_rel = 0  # How many snippets have been seen that are TREC relevant?
        self.seen_trec_nonrel = 0  # How many snippets have been seen that are TREC nonrelevant?
        self.seen_trec_unassessed = 0  # How many snippets have been seen that are TREC unassessed?

        self.ad_hover_count = 0  # How many adverts have been hovered over?
        self.ad_hover_count_top = 0  # Same as above, but filtering on the top set only.
        self.ad_hover_count_side = 0  # Same as above, but filtering on the side set.
        self.ad_hover_count_bot = 0  # Same as above, but on the bottom set.

        self.ad_click_count = 0  # How many adverts were clicked on in total?
        self.ad_click_count_top = 0  # A subset of the above; considering ads on the top only
        self.ad_click_count_side = 0  # A subset of the above; considering ads on the side only
        self.ad_click_count_bot = 0  # A subset of the above; considering ads on the bottom only

        # Instance variables to store times.
        self.time_system_query_delay = 0.0  # Elapsed time for query lag (from QUERY_START to QUERY_END), in seconds.
        self.time_on_serp = 0.0  # Elapsed time spend examining content on the SERP, in seconds.
        self.time_document_clicked = None # When was the last DOC_CLICKED event?
        self.time_on_documents = 0.0  # Elapsed time spent on documents.
        self.time_session_start = f"{line[0]} {line[1]}"  # When did the search session start? Get this from the line variable.
        self.time_session_end = None  # When did the session end? Saved in end_query_session().
        self.time_session_overall = 0.0  # The overall session time. From QUERY_FOCUS to the end event.

        # For storing performance measures.
        self.performance = None  # A dictionary of performance measures.
        self.rankings = None  # The document rankings.

        # Got a search engine? Use the damn search engine!
        if self.search_engine:
            self.calculate_performance()

    def calculate_performance(self):
        """
        If a search engine is provided to an instance of this class, this method is called to execute the query and calculate performance measures.
        If no search engine is provided, this method is skipped.
        """
        query = Query(self.query)
        query.skip = 1
        query.top = 50

        response = self.search_engine.search(query)
        measures = get_query_performance_metrics(self.qrel_handler, response.results, self.topic)

        self.performance = {}
        self.rankings = response.results

        for key in PERFORMANCE_COLUMNS:
            self.performance[key] = measures[key]
    
    def process(self, line):
        """
        Given a line (from the LogEntryReader), process what the line says.
        This does not include events that end a query session; only events that take place within.
        """
        self.event_count += 1
        self.curr_event = line[9]
        self.update_times(f'{line[0]} {line[1]}')

        # When the user is presented with a SERP, do this.
        if self.curr_event == 'VIEW_SEARCH_RESULTS_PAGE':
            page_no = int(line[10])

            if page_no > self.serp_page_viewed_to:
                self.serp_page_viewed_to = page_no
        
        # When the user clicks the 'View Task' link, do this.
        if self.curr_event == 'VIEW_TASK':
            self.clicks_on_view_task += 1

        # When a document is clicked, do this.
        if self.curr_event == 'DOC_MARKED_VIEWED':
            docid = line[11]
            rank = int(line[14])
            qrel_judgement = self.qrel_handler.get_value_if_exists(self.topic, docid)

            # Work out the number of clicks that have been made on documents.
            if docid not in self.document_clicked_list:
                self.document_clicked_list.append(docid)
                self.document_click_count += 1

                if qrel_judgement is None:
                    self.document_click_count_trec_unassessed += 1
                elif qrel_judgement < 1:
                    self.document_click_count_trec_nonrel += 1
                else:
                    self.document_click_count_trec_rel += 1
            
            # Work out the click depth(s).
            if rank > self.document_click_depth:
                self.document_click_depth = rank
            
            if qrel_judgement is None:
                if rank > self.document_click_depth_trec_unassessed:
                    self.document_click_depth_trec_unassessed = rank
            elif qrel_judgement < 1:
                if rank > self.document_click_depth_trec_nonrel:
                    self.document_click_depth_trec_nonrel = rank
            else:
                if rank > self.document_click_depth_trec_rel:
                    self.document_click_depth_trec_rel = rank
        
        # When an organic result or advertisement is hovered over, do this.
        if self.curr_event == 'DOCUMENT_HOVER_IN':
            try:  # If this succeeds, this is a document.
                rank = int(line[14])
                docid = line[11]
                qrel_judgement = self.qrel_handler.get_value_if_exists(self.topic, docid)

                # Calculate the number of hover events.
                if docid not in self.document_hover_list:
                    self.document_hover_list.append(docid)
                    self.document_hover_count += 1

                    if qrel_judgement is None:
                        self.document_hover_count_trec_unassessed += 1
                    elif qrel_judgement < 1:
                        self.document_hover_count_trec_nonrel += 1
                    else:
                        self.document_hover_count_trec_rel += 1
                
                # Calculate the hover depths.
                if rank > self.document_hover_depth:
                    self.document_hover_depth = rank
                
                if qrel_judgement is None:
                    if rank > self.document_hover_depth_trec_unassessed:
                        self.document_hover_depth_trec_unassessed = rank
                elif qrel_judgement < 1:
                    if rank > self.document_hover_depth_trec_nonrel:
                        self.document_hover_depth_trec_nonrel = rank
                else:
                    if rank > self.document_hover_depth_trec_rel:
                        self.document_hover_depth_trec_rel = rank
            except ValueError:  # Assume here that an advert has been hovered over.
                ad_position = line[14]
                self.ad_hover_count += 1

                if ad_position == 'ad-top':
                    self.ad_hover_count_top += 1
                elif ad_position == 'ad-side':
                    self.ad_hover_count_side += 1
                elif ad_position == 'ad-bot':
                    self.ad_hover_count_bot += 1
        
        # When a document is saved as relevant, do this.
        if self.curr_event == 'DOC_MARKED_RELEVANT':
            docid = line[11]
            rank = int(line[14])
            qrel_judgement = self.qrel_handler.get_value_if_exists(self.topic, docid)
            
            # Calculate the number of save events.
            if docid not in self.document_saved_list:
                self.document_saved_list.append(docid)
                self.document_saved_count += 1
            
                if qrel_judgement is None:
                    self.document_saved_count_trec_unassessed += 1
                elif qrel_judgement < 1:
                    self.document_saved_count_trec_nonrel += 1
                else:
                    self.document_saved_count_trec_rel += 1
            
            # Calculate the save depths.
            if rank > self.document_saved_depth:
                self.document_saved_depth = rank
            
            if qrel_judgement is None:
                if rank > self.document_saved_depth_trec_unassessed:
                    self.document_saved_depth_trec_unassessed = rank
            elif qrel_judgement < 1:
                if rank > self.document_saved_depth_trec_nonrel:
                    self.document_saved_depth_trec_nonrel = rank
            else:
                if rank > self.document_saved_depth_trec_rel:
                    self.document_saved_depth_trec_rel = rank
        
        # When an advertisement is clicked, do this.
        if self.curr_event == 'AD_CLICKED':
            ad_position = line[11]
            self.ad_click_count += 1

            if ad_position.startswith('top'):
                self.ad_click_count_top += 1
            elif ad_position.startswith('side'):
                self.ad_click_count_side += 1
            elif ad_position.startswith('bot'):
                self.ad_click_count_bot += 1
        
        self.last_last_event = self.last_event
        self.last_event = self.curr_event
        self.last_time = f"{line[0]} {line[1]}"

    def update_times(self, curr_time):
        """
        Called from process(). Updates the various times that are being tracked, considering how the current event changes them.
        """
        # Work out any system query delay.
        if self.time_system_query_delay == 0.0 and self.curr_event == 'QUERY_END' and self.last_event == 'QUERY_START':
            self.time_system_query_delay += get_time_diff(self.last_time, curr_time)
        
        # Update the last document click time.
        if not self.time_document_clicked and self.curr_event == 'DOC_CLICKED':
            self.time_document_clicked = curr_time
        
        # Measure time on documents.
        if self.time_document_clicked and self.curr_event in ['QUERY_START', 'VIEW_SAVED_DOCS', EVENT_SEARCH_SESSION_COMPLETE]:
            self.time_on_documents += get_time_diff(self.time_document_clicked, curr_time)
            self.time_document_clicked = None  # Reset the last document clicked time.
        
        # Simple way to calculate SERP time (new_total_serp in previous revision)
        if not self.last_serp_event and self.curr_event == 'VIEW_SEARCH_RESULTS_PAGE':
            self.last_serp_event = curr_time
        elif self.last_serp_event and self.curr_event not in ['DOCUMENT_HOVER_IN', 'DOCUMENT_HOVER_OUT']:
            self.time_on_serp += get_time_diff(self.last_serp_event, curr_time)
            self.last_serp_event = None
    
    def end_query_session(self, end_time):
        """
        Called from LogEntryReader. This is called when a query session has come to an end.
        For example, this is called when a QUERY_ISSUED event takes place (ending the previous one), or when the search session ends in entirety.
        This is called once, when the QUERY SESSION ends -- not the SEARCH SESSION.
        """
        if self.time_session_end is None:  # Only execute if we haven't calculated this already.
            self.time_session_end = end_time
            self.time_session_overall = get_time_diff(self.time_session_start, self.time_session_end)
        
        # At the end of the session, we can work out seen depths.
        # These require the search engine to get the rankings.
        if ('seen' in QUERY_SESSION_COLUMNS or 'seen_trec_rel' in QUERY_SESSION_COLUMNS or 'seen_trec_nonrel' in QUERY_SESSION_COLUMNS or 'seen_trec_unassessed' in QUERY_SESSION_COLUMNS) and not self.search_engine:
            raise ValueError("You want to display a 'seen' value, but have not specified a search engine. The search engine needs to be present to get a list of rankings. Try again with the search engine configured.")

        # The seen depth is usuall the hover depth.
        seen_depth = self.document_hover_depth
        position = 0

        # If True, the click depth is deeper. Maybe a hover event didn't reach in time. Whatever; change the value.
        if self.document_click_depth > seen_depth:
            seen_depth = self.document_click_depth
        
        # We can assume we have document rankings now, as the search engine presence check was done above.
        # Loop through the rankings to seen_depth. Update the seen counters.
        for document in self.rankings:
            if position == seen_depth:
                break
            
            docid = document.docid.decode('utf-8')
            qrel_judgement = self.qrel_handler.get_value_if_exists(self.topic, docid)

            if qrel_judgement is None:
                self.seen_trec_unassessed += 1
            elif qrel_judgement < 1:
                self.seen_trec_nonrel += 1
            else:
                self.seen_trec_rel += 1
            
            self.seen += 1
            position += 1

    def __str__(self):
        return_str = ""

        # Append the counts in order.
        for key in QUERY_SESSION_COLUMNS:
            if return_str == "":
                return_str = f"{getattr(self, key)}"
            else:
                return_str = f"{return_str}{SEPARATOR}{getattr(self, key)}"
        
        # If required, include the performance measures.
        if self.search_engine:
            for key in PERFORMANCE_COLUMNS:
                return_str = f"{return_str}{SEPARATOR}{self.performance[key]}"
        
        return return_str


def main(log_path, qrel_path, index_path=None, stopwords_path=None):
    """
    Begins the arduous process of parsing the log file.
    Creates the necessary data structures and objects, and creates a LogReader object to start the process.
    """
    qrels_handler = TrecQrelHandler(qrel_path)
    search_engine = None

    # If this condition is met, we create a search engine object.
    if index_path is not None and stopwords_path is not None:
        search_engine = Whooshtrec(
            whoosh_index_dir=index_path,
            stopwords_file=stopwords_path,
            model=1,
            newschema=True,
            implicit_or=True)
        
        search_engine.key_name = 'bm25'
        search_engine.set_fragmenter(frag_type=2, surround=40)
        search_engine.set_model(1, pval=0.75)

    log_reader = LogReader(LogEntryReader, qrels_handler, search_engine=search_engine)
    log_reader.process(log_path)
    log_reader.report(show_key=True)

if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        print(f"Usage: {sys.argv[0]} <log_path> <qrels_path> <index_path:optional> <stopwords_path:optional>")
        print(f"Note: <index_path> and <stopwords_path> are optional; if you specify one, both are required.")
        print(f"If you specify these optional arguments, queries will be executed and performance values will be supplied.")
        sys.exit(1)
    
    log_path = sys.argv[1]
    qrels_path = sys.argv[2]
    index_path = None
    stopwords_path = None

    if len(sys.argv) > 3:
        if len(sys.argv) != 5:
            print("You need to specify <index_path> AND <stopwords_path>!")
            sys.exit(1)
        
        index_path = sys.argv[3]
        stopwords_path = sys.argv[4]
    
    main(log_path, qrels_path, index_path=index_path, stopwords_path=stopwords_path)
    sys.exit(0)