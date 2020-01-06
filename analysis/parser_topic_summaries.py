#
# Topic summaries generator mark II (revised from previous iteration)
# Used for SIGIR 2020 experiment
# Kill me
#
# Author: David Maxwell
# Date: 2020-01-05
#

import sys

# The key values (username, topic, condition, etc.) -- placed at the start of output lines.
KEY_LIST = ['username', 'condition', 'interface', 'task', 'topic']

# What values do you want to be in the output? These need to be instance variables in .
COMPUTED_VALUES = [
    'queries_total_issued',
    'document_clicked_total',
    'document_clicked_total_trec_rel',
    'document_clicked_total_trec_nonrel',
    'document_clicked_total_trec_unassessed',
    'document_clicked_per_query',
    'document_saved_total',
    'document_saved_total_trec_rel',
    'document_saved_total_trec_nonrel',
    'document_saved_total_trec_unassessed',
    'document_click_depth_per_query',
    'document_hover_total',
    'serps_viewed_total',
    'serps_viewed_per_query',
    'time_session_total',
    'time_query_total',
    'time_serp_total',
    'time_documents_total',
    'time_per_query',
    'time_per_document',
    'time_per_snippet',
    'mean_pm',
    'mean_pmr',
    'mean_pmn',
    'mean_pc',
    'mean_pcr',
    'mean_pcn',
    'accuracy_search_session',
    'mean_p1',
    'mean_p5',
    'mean_p10',
    'mean_p20',
    'mean_rprec',
]

SEPARATOR = ','  # What does each column get separated by?


class PerQueryOutputParser(object):
    """
    Handles the parsing of the log file, and keeps track of all the search sessions.
    """
    def __init__(self, filename):
        self.key_mappings = {}
        self.data = {}
        self.filename = filename
    
    def parse_file(self):
        f = open(self.filename, 'r')

        for line in f:
            line = line.strip().split(',')

            if line[0] == 'username':
                self.create_key_mappings(line)
                continue

            username = line[0]
            condition = line[1]
            interface = line[2]
            task = line[3]
            topic = line[4]

            if username not in self.data:
                self.data[username] = {}
            
            if topic not in self.data[username]:
                self.data[username][topic] = SearchSessionAggregator(self.key_mappings, username, condition, interface, task, topic)
            
            self.data[username][topic].add_line(line)
        f.close()

        self.calculate_values()

    def calculate_values(self):
        """
        Calculate the values that are required for output.
        """
        for username in self.data.keys():
            for topic in self.data[username].keys():
                self.data[username][topic].compute()
    
    def report(self):
        """
        Reports the computed data to stdout.
        """
        # First, print the key.
        header_key = ""

        for key in KEY_LIST:
            if header_key == "":
                header_key = f"{key}"
            else:
                header_key = f"{header_key}{SEPARATOR}{key}"
        
        # Now add the extra columns from this script.
        for key in COMPUTED_VALUES:
            header_key = f"{header_key}{SEPARATOR}{key}"
        
        print(header_key)

        # Now, we need to spit out the values for each of the search sessions.
        for username in self.data.keys():
            for topic in self.data[username].keys():
                print(self.data[username][topic])
    
    def create_key_mappings(self, line):
        """
        Sets the key_mappings instance variable.
        Keys are the column name you want, values are the column index corresponding to that name on an input line.
        """
        index = 0

        for key in line:
            self.key_mappings[key] = index
            index += 1


class SearchSessionAggregator(object):
    """
    Takes details for a given user/topic combination (a search session), and computes the aggregated values.
    """
    def __init__(self, key_mappings, username, condition, interface, task, topic):
        self.data = []
        self.key_mappings = key_mappings

        # Key variables.
        self.username = username
        self.condition = condition
        self.interface = interface
        self.task = task
        self.topic = topic

        # Instance variables below can be used in output. Make sure required output names match these variables!
        self.queries_total_issued = 0  # How many queries were issued over all query sessions?

        self.document_clicked_total = 0  # How many documents were clicked over all query sessions?
        self.document_clicked_total_trec_rel = 0  # Same as above, filtered for TREC relevant documents only.
        self.document_clicked_total_trec_nonrel = 0  # Same as above, filtered for TREC nonrelevant documents only.
        self.document_clicked_total_trec_unassessed = 0  # Same as above, filtered for TREC unassessed documents only.
        self.document_clicked_per_query = 0  # The total number of documents clicked, divided by the number of queries issued.

        self.document_saved_total = 0
        self.document_saved_total_trec_rel = 0
        self.document_saved_total_trec_nonrel = 0
        self.document_saved_total_trec_unassessed = 0

        self.document_click_depth_per_query = 0

        self.document_hover_total = 0
        self.document_hover_raw_total = 0

        self.serps_viewed_total = 0
        self.serps_viewed_per_query = 0
        
        self.time_session_total = 0.0
        self.time_query_total = 0.0
        self.time_serp_total = 0.0
        self.time_documents_total = 0.0
        self.time_per_query = 0.0
        self.time_per_document = 0.0
        self.time_per_snippet = 0.0

        self.mean_pm = 0.0
        self.mean_pmr = 0.0
        self.mean_pmn = 0.0
        self.mean_pc = 0.0
        self.mean_pcr = 0.0
        self.mean_pcn = 0.0

        self.accuracy_search_session = 0.0  # See calculate() below for a description of accuracy.

        self.mean_p1 = 0
        self.mean_p5 = 0
        self.mean_p10 = 0
        self.mean_p20 = 0
        self.mean_rprec = 0
        

        # These are used for storing values so a mean can be created (above).
        self.document_click_depths = []
        self.values_pm = []
        self.values_pmr = []
        self.values_pmn = []
        self.values_pc = []
        self.values_pcr = []
        self.values_pcn = []
        self.values_p1 = []
        self.values_p5 = []
        self.values_p10 = []
        self.values_p20 = []
        self.values_rprec = []
    
    def add_line(self, line):
        """
        Adds an input line (query summary) to the search session representation.
        """
        self.data.append(line)
    
    def compute(self):
        """
        Does the number crunching. Call this only when all input lines (query summaries) have been added.
        """
        self.queries_total_issued = len(self.data)

        for query_session in self.data:
            self.document_clicked_total += self.get_value(query_session, 'document_click_count', int)
            self.document_clicked_total_trec_rel += self.get_value(query_session, 'document_click_count_trec_rel', int)
            self.document_clicked_total_trec_nonrel += self.get_value(query_session, 'document_click_count_trec_nonrel', int)
            self.document_clicked_total_trec_unassessed += self.get_value(query_session, 'document_click_count_trec_unassessed', int)

            self.document_saved_total += self.get_value(query_session, 'document_saved_count', int)
            self.document_saved_total_trec_rel += self.get_value(query_session, 'document_saved_count_trec_rel', int)
            self.document_saved_total_trec_nonrel += self.get_value(query_session, 'document_saved_count_trec_nonrel', int)
            self.document_saved_total_trec_unassessed += self.get_value(query_session, 'document_saved_count_trec_unassessed', int)

            self.document_click_depths.append(self.get_value(query_session, 'document_click_depth', int))

            self.document_hover_total += self.get_value(query_session, 'document_hover_count', int)
            self.document_hover_raw_total += self.get_value(query_session, 'document_hover_count_raw', int)

            self.serps_viewed_total += self.get_value(query_session, 'serp_page_viewed_to', int)

            self.time_session_total += self.get_value(query_session, 'time_session_overall', float)
            self.time_query_total += self.get_value(query_session, 'time_query', float)
            self.time_serp_total += self.get_value(query_session, 'time_on_serp', float)
            self.time_documents_total += self.get_value(query_session, 'time_on_documents', float)

            self.values_pm.append(self.get_value(query_session, 'pm', float))
            self.values_pmr.append(self.get_value(query_session, 'pmr', float))
            self.values_pmn.append(self.get_value(query_session, 'pmn', float))
            self.values_pc.append(self.get_value(query_session, 'pc', float))
            self.values_pcr.append(self.get_value(query_session, 'pcr', float))
            self.values_pcn.append(self.get_value(query_session, 'pcn', float))

            self.values_p1.append(self.get_value(query_session, 'p1', float))
            self.values_p5.append(self.get_value(query_session, 'p5', float))
            self.values_p10.append(self.get_value(query_session, 'p10', float))
            self.values_p20.append(self.get_value(query_session, 'p20', float))
            self.values_rprec.append(self.get_value(query_session, 'rprec', float))
        
        self.document_clicked_per_query = self.document_clicked_total / float(self.queries_total_issued)

        self.document_click_depth_per_query = sum(self.document_click_depths) / float(self.queries_total_issued)
        
        self.serps_viewed_per_query = self.serps_viewed_total / float(self.queries_total_issued)

        self.time_per_query = self.time_query_total / float(self.queries_total_issued)

        if self.document_clicked_total > 0:
            self.time_per_document = self.time_documents_total / float(self.document_clicked_total)
        
        if self.document_hover_total > 0:

            depth = max(max(float(self.document_hover_raw_total), float(self.document_clicked_total)),3.0)
            #self.time_per_snippet = self.time_serp_total / float(self.document_hover_raw_total)
            self.time_per_snippet = self.time_serp_total / depth

        # Probabilities -- we have the probability of each query, so take the mean of them?
        # Not sure if this is 100% correct.
        self.mean_pm = sum(self.values_pm) / float(len(self.values_pm))
        self.mean_pmr = sum(self.values_pmr) / float(len(self.values_pmr))
        self.mean_pmn = sum(self.values_pmn) / float(len(self.values_pmn))
        self.mean_pc = sum(self.values_pc) / float(len(self.values_pc))
        self.mean_pcr = sum(self.values_pcr) / float(len(self.values_pcr))
        self.mean_pcn = sum(self.values_pcn) / float(len(self.values_pcn))

        # Accuracy -- the total number of TREC relevant documents saved, divided by the total number saved.
        if self.document_saved_total > 0:
            self.accuracy_search_session = self.document_saved_total_trec_rel / float(self.document_clicked_total)
        
        self.mean_p1 = sum(self.values_p1) / self.queries_total_issued
        self.mean_p5 = sum(self.values_p5) / self.queries_total_issued
        self.mean_p10 = sum(self.values_p10) / self.queries_total_issued
        self.mean_p20 = sum(self.values_p20) / self.queries_total_issued
        self.mean_rprec = sum(self.values_rprec) / self.queries_total_issued
    
    def get_value(self, line, key, cast_to=None):
        """
        Given an input line, returns the value at the column index, given by the key.
        """
        index = self.key_mappings[key]

        if cast_to:
            return cast_to(line[index])
        
        return line[index]

    def __str__(self):
        """
        A string representation of this session, used by the report() method.
        """
        # First, print the key.
        output_str = ""

        for key in KEY_LIST:
            value = getattr(self, key)

            if output_str == "":
                output_str = f"{value}"
            else:
                output_str = f"{output_str}{SEPARATOR}{value}"
        
        # Now add the extra columns from this script.
        for key in COMPUTED_VALUES:
            value = getattr(self, key)
            
            if type(value) == float:
                output_str = f"{output_str}{SEPARATOR}{value:.3f}"
            else:
                output_str = f"{output_str}{SEPARATOR}{value}"
        
        return output_str


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <per_query_output_file>")
        print("Get the per_query_output_file from parser_per_query.py.")
        sys.exit(1)
    
    parser = PerQueryOutputParser(sys.argv[1])
    parser.parse_file()
    parser.report()
