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
    'documents_clicked',
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
        self.queries_total_issued = 0
        self.documents_clicked = 0
    
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
            self.documents_clicked += self.get_value(query_session, 'document_click_count', int)
    
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