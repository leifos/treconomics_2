#
# Updated per-topic summary parser for SIGIR 2020 adverts study.
# Takes data from the interaction log (USER_PERFORMANCE entries) and the per-query summary.
# Also excludes users that did not complete all four search tasks.
# 
# Author: David Maxwell
# Date: 2020-01-01
#

import os
import sys
from utils import get_time_diff

# As we are using ifind mashed into this repository, we need to add that to our path before we can import from it.
path_cwd = os.getcwd()
path_levelup = os.path.abspath(os.path.join(path_cwd, '..'))
path_treconomics_base = os.path.join(path_levelup, 'treconomics_project')
sys.path.append(path_treconomics_base)
# End appending of treconomics_project path

from ifind.seeker.trec_qrel_handler import TrecQrelHandler

EXAMINED_TOPICS = ['341', '347', '367', '408', '435']  # What topics are expected?
PRACTICE_TOPIC = '367'  # ID of the practice topic


def get_log_data(log_path):
    """
    Returns a data structure representing data gathered from the log file -- including a status for each user,
    and whether they completed the tasks asked of them. This data is used to filter the dataset.
    """
    details = {}
    f = open(log_path, 'r')
    
    for line in f:
        line = line.strip().split(' ')

        # The log is messy. We need to clean the input for this line. Jeez.
        while '' in line:
            line.remove('')

        date_time = '{date} {time}'.format(date=line[0], time=line[1])
        username = line[3]
        topic = line[8]
        action = line[9]
        condition = line[4]
        interface = line[5]
        
        if username not in details:
            details[username] = {}
        
        # Log file is a mess. Jesus.
        if topic != 'VIEW_PERFORMANCE':
            if topic not in details[username]:
                details[username][topic] = {}
            
            # The start of the practice search task, or a standard search task.
            if action in ['PRACTICE_SEARCH_TASK_COMMENCED', 'SEARCH_TASK_COMMENCED']:
                details[username][topic]['start'] = date_time
            
            # If we hit this action, the task has been completed.
            if action in ['TASK_ENDED', 'CONCEPT_LISTING_COMPLETED']:
                details[username][topic]['end'] = date_time
            
            details[username][topic]['condition'] = condition
            details[username][topic]['interface'] = interface
            
        # A user performance summary line -- store everything recorded here!
        # This seems to be vastly reduced from previous studies (in terms of what is reported).
        if topic == 'VIEW_PERFORMANCE':  # Topic is right; the log file is inconsistent.
            perf_topic = line[7]

            details[username][perf_topic]['total_marked'] = line[9]
            details[username][perf_topic]['accuracy'] = line[10]
            details[username][perf_topic]['relevant_docs'] = line[11]
            details[username][perf_topic]['nonrelevant_docs'] = line[12]
    
    f.close()
    return details

def get_summary_data(per_query_summary_path, filtered_log_data):
    """
    Given the path to the summary file, and a dictionary of filtered log data, returns a further dictionary
    containing information aggregated over all queries for a given user/topic combination in the query summary file.
    """
    f = open(per_query_summary_path, 'r')
    query_data = {}
    summary_data = {}

    # This is grossly inefficient, but it will do for now.
    # First, extract from the summary file all of the lines we want to parse.
    for line in f:
        line = line.strip().split(' ')
        user = line[0]
        topic = line[4]

        if user == 'username':
            continue

        if user in filtered_log_data.keys() and topic in filtered_log_data[user].keys():
            if user not in query_data:
                query_data[user] = {}
            
            if topic not in query_data[user]:
                query_data[user][topic] = []
            
            query_data[user][topic].append(line)
    
    # Now we have each line we wish to parse, we can do our data extraction/summation/averaging.
    for user in query_data:
        for topic in query_data[user]:
            if user not in summary_data:
                summary_data[user] = {}
            
            if topic not in summary_data[user]:
                summary_data[user][topic] = {}
            
            # Reference to the dictionary we are going to be adding K/V pairs to.
            entry_dict = summary_data[user][topic]
            
            # Create the blank entries for the user/topic combination.
            entry_dict['queries_issued'] = len(query_data[user][topic])
            entry_dict['hover_count'] = 0
            entry_dict['documents_clicked'] = 0
            entry_dict['document_click_depths'] = []
            entry_dict['serp_pages'] = 0
            entry_dict['total_query_time'] = 0
            entry_dict['total_document_time'] = 0
            entry_dict['total_serp_time'] = 0
            entry_dict['p1'] = []
            entry_dict['p5'] = []
            entry_dict['p10'] = []
            entry_dict['p20'] = []
            entry_dict['was_task_view_clicked'] = 0
            entry_dict['task_view_count'] = 0

            # Blanks for values used to compute probabilities.
            entry_dict['clicked_trec_rel'] = 0
            entry_dict['clicked_trec_nonrel'] = 0
            entry_dict['hover_trec_rel'] = 0
            entry_dict['hover_trec_nonrel'] = 0

            # Blanks for values related to adverts go here.
            entry_dict['ads_hover_total'] = 0
            entry_dict['ads_hover_top'] = 0
            entry_dict['ads_hover_bot'] = 0
            entry_dict['ads_hover_side'] = 0

            entry_dict['ads_clicks_total'] = 0
            entry_dict['ads_clicks_top'] = 0
            entry_dict['ads_clicks_bot'] = 0
            entry_dict['ads_clicks_side'] = 0

            # Now add the data from the query_data.txt line. Check query_data_key.txt for positions.
            # Remember that positions are zero-based...
            for line in query_data[user][topic]:
                entry_dict['total_query_time'] += float(line[19])
                entry_dict['total_document_time'] += float(line[22])
                entry_dict['hover_count'] += int(line[11])
                entry_dict['documents_clicked'] += int(line[7])
                entry_dict['document_click_depths'] += [int(line[8])]
                entry_dict['serp_pages'] += int(line[6])
                entry_dict['total_serp_time'] += float(line[24])

                entry_dict['p1'] += [float(line[25])]
                entry_dict['p5'] += [float(line[29])]
                entry_dict['p10'] += [float(line[30])]
                entry_dict['p20'] += [float(line[32])]

                # Used for calculating probabilities
                entry_dict['clicked_trec_rel'] += int(line[17])  # Is this correct, and is the one below correct?
                entry_dict['clicked_trec_nonrel'] += int(line[18])
                entry_dict['hover_trec_rel'] += int(line[12])
                entry_dict['hover_trec_nonrel'] += int(line[13])

                # Adding the task view clicked
                entry_dict['task_view_count'] = int(line[40])
                entry_dict['was_task_view_clicked'] = 0

                if entry_dict['task_view_count'] > 0:
                    entry_dict['was_task_view_clicked'] = 1
                
                # Add code for advert data processing here.
                entry_dict['ads_hover_total'] += int(line[41])
                entry_dict['ads_hover_top'] += int(line[42])
                entry_dict['ads_hover_bot'] += int(line[43])
                entry_dict['ads_hover_side'] += int(line[44])

                entry_dict['ads_clicks_total'] += int(line[49])
                entry_dict['ads_clicks_top'] += (int(line[50]) + int(line[53]))
                entry_dict['ads_clicks_bot'] += (int(line[51]) + int(line[54]))
                entry_dict['ads_clicks_side'] += (int(line[52]) + int(line[55]))

    f.close()
    return summary_data

def compute_qrel_stats(qrels):
    """
    Returns a dictionary of basic statistics about each topic, given a QRELs handler.
    Uses the topic list defined by EXAMINED_TOPICS.
    """
    return_dict = {}

    for topic in EXAMINED_TOPICS:
        return_dict[topic] = {}
        doc_list = qrels.get_doc_list(topic)

        return_dict[topic]['total_listed_docs'] = len(doc_list)
        return_dict[topic]['total_rels'] = 0
        return_dict[topic]['total_nonrels'] = 0

        for doc in doc_list:
            judgement = qrels.get_value(topic, doc)

            if judgement < 1:
                return_dict[topic]['total_nonrels'] += 1
            else:
                return_dict[topic]['total_rels'] += 1
    
    return return_dict

def main(log_path, per_query_summary_path, qrels, filter_practice_topic=True):
    """
    Main function -- preps the data structures, and outputs the topic summaries.
    """
    log_data = get_log_data(log_path)
    filtered_log_data = log_data
    query_summarised_data = get_summary_data(per_query_summary_path, filtered_log_data)
    qrel_stats = compute_qrel_stats(qrels)

    # Print the key.
    key_f = open('topic_summaries_key.txt', 'r')
    key_str = ""

    for key_line in key_f:
        key_line = key_line.strip()
        key_str = f"{key_str},{key_line}"

    print(key_str[1:])
    key_f.close()
    # End print key.

    for user in filtered_log_data:
        for topic in filtered_log_data[user]:
            if topic == PRACTICE_TOPIC and filter_practice_topic:
                continue
            
            log_entry = filtered_log_data[user][topic]
            query_summary_entry = query_summarised_data[user][topic]

            query_summary_entry['time_per_snippet'] = 0.0

            if query_summary_entry['hover_count'] > 0:
                query_summary_entry['time_per_snippet'] = query_summary_entry['total_serp_time'] / float(query_summary_entry['hover_count'])
            
            # Work out probabilities
            query_summary_entry['pm'] = 0.0
            query_summary_entry['pmr'] = 0.0
            query_summary_entry['pmn'] = 0.0
            query_summary_entry['pc'] = 0.0
            query_summary_entry['pcr'] = 0.0
            query_summary_entry['pcn'] = 0.0

            if (float(query_summary_entry['clicked_trec_rel']) + float(query_summary_entry['clicked_trec_nonrel'])) > 0:
                query_summary_entry['pm'] = (float(log_entry['total_marked'])) / (float(query_summary_entry['clicked_trec_rel']) + float(query_summary_entry['clicked_trec_nonrel']))
            
            if query_summary_entry['clicked_trec_rel'] > 0:
                query_summary_entry['pmr'] = float(log_entry['relevant_docs']) / float(query_summary_entry['clicked_trec_rel'])
            
            # This may not be correct. I think I am missing some data.
            if query_summary_entry['clicked_trec_nonrel'] > 0:
                query_summary_entry['pmn'] = (float(log_entry['nonrelevant_docs'])) / float(query_summary_entry['clicked_trec_nonrel'])
            
            if (query_summary_entry['hover_trec_rel'] + query_summary_entry['hover_trec_nonrel']) > 0:
                query_summary_entry['pc'] = (float(query_summary_entry['clicked_trec_rel']) + float(query_summary_entry['clicked_trec_nonrel'])) / (query_summary_entry['hover_trec_rel'] + query_summary_entry['hover_trec_nonrel'])
            
            if query_summary_entry['hover_trec_rel'] > 0:
                query_summary_entry['pcr'] = float(query_summary_entry['clicked_trec_rel']) / query_summary_entry['hover_trec_rel']
            
            if query_summary_entry['hover_trec_nonrel'] > 0:
                query_summary_entry['pcn'] = float(query_summary_entry['clicked_trec_nonrel']) / query_summary_entry['hover_trec_nonrel']

            # Print everything out. Check order is correct for key.
            print(  f"{user}," \
                    f"{topic}," \
                    f"{log_entry['condition']}," \
                    f"{log_entry['interface']}," \
                    f"{log_entry['accuracy']}," \
                    f"{log_entry['total_marked']}," \
                    f"{log_entry['relevant_docs']}," \
                    f"{log_entry['nonrelevant_docs']}," \

                    f"{query_summary_entry['queries_issued']}," \
                    f"{query_summary_entry['documents_clicked']}," \
                    f"{query_summary_entry['documents_clicked'] / float(query_summary_entry['queries_issued'])}," \
                    f"{sum(query_summary_entry['document_click_depths']) / float(query_summary_entry['queries_issued'])}," 
                    f"{query_summary_entry['serp_pages']}," \
                    f"{query_summary_entry['serp_pages'] / float(query_summary_entry['queries_issued'])}," \
                    f"{get_time_diff(log_entry['start'], log_entry['end'])}," \
                    f"{query_summary_entry['total_query_time']}," \
                    f"{query_summary_entry['total_query_time'] / float(query_summary_entry['queries_issued'])}," \
                    f"{query_summary_entry['total_document_time']}," \
                    f"{query_summary_entry['total_document_time'] / float(query_summary_entry['documents_clicked'])}," \
                    f"{query_summary_entry['total_serp_time']}," \
                    f"{query_summary_entry['time_per_snippet']}," \

                    f"{sum(query_summary_entry['p1'])/float(len(query_summary_entry['p1']))}," \
                    f"{sum(query_summary_entry['p5'])/float(len(query_summary_entry['p5']))}," \
                    f"{sum(query_summary_entry['p10'])/float(len(query_summary_entry['p10']))}," \
                    f"{sum(query_summary_entry['p20'])/float(len(query_summary_entry['p20']))}," \

                    f"{query_summary_entry['pm']}," \
                    f"{query_summary_entry['pmr']}," \
                    f"{query_summary_entry['pmn']}," \
                    f"{query_summary_entry['pc']}," \
                    f"{query_summary_entry['pcr']}," \
                    f"{query_summary_entry['pcn']}," \

                    f"{query_summary_entry['was_task_view_clicked']}," \
                    f"{query_summary_entry['task_view_count']}," \

                    f"{query_summary_entry['ads_hover_total']}," \
                    f"{query_summary_entry['ads_hover_top']}," \
                    f"{query_summary_entry['ads_hover_bot']}," \
                    f"{query_summary_entry['ads_hover_side']}," \

                    f"{query_summary_entry['ads_clicks_total']}," \
                    f"{query_summary_entry['ads_clicks_top']}," \
                    f"{query_summary_entry['ads_clicks_bot']}," \
                    f"{query_summary_entry['ads_clicks_side']}," \
    )

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <log_path> <per_query_summary_path> <qrels_path>")
        sys.exit(1)
    
    log_path = sys.argv[1]
    per_query_summary_path = sys.argv[2]
    qrels = TrecQrelHandler(sys.argv[3])
    main(log_path, per_query_summary_path, qrels, filter_practice_topic=True)