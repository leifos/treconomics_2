#
# Updated per-topic summary parser for SIGIR 2018 Diversity Study.
# Takes data from the interaction log (USER_PERFORMANCE entries) and the per-query summary.
# Also excludes users that did not complete all four search tasks.
# 
# Author: David Maxwell
# Date: 2018-01-16
#

import sys
from utils import get_time_diff

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
            
        # A user performance summary line -- store everything recorded here!
        # This seems to be vastly reduced from previous studies (in terms of what is reported).
        if topic == 'VIEW_PERFORMANCE':  # Topic is right; the log file is inconsistent.
            perf_topic = line[7]

            details[username][perf_topic]['total_marked'] = line[9]
            details[username][perf_topic]['accuracy'] = line[10]
            details[username][perf_topic]['relevant_docs'] = line[11]
            details[username][perf_topic]['nonrelevant_docs'] = line[12]
    
    f.close()
    print(details)
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
        topic = line[5]
        
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
            
            entry_dict = summary_data[user][topic]
            
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
            entry_dict['new_at_1'] = []
            entry_dict['new_at_5'] = []
            entry_dict['new_at_10'] = []
            entry_dict['new_at_20'] = []
            entry_dict['adcg_5'] = []
            entry_dict['adcg_10'] = []
            entry_dict['was_task_view_clicked'] = 0
            entry_dict['task_view_count'] = 0
            
            entry_dict['clicked_trec_rel'] = 0
            entry_dict['clicked_trec_nonrel'] = 0
            entry_dict['hover_trec_rel'] = 0
            entry_dict['hover_trec_nonrel'] = 0
            
            for line in query_data[user][topic]:
                entry_dict['total_query_time'] = entry_dict['total_query_time'] + float(line[20])
                entry_dict['total_document_time'] = entry_dict['total_document_time'] + float(line[23])
                entry_dict['hover_count'] = entry_dict['hover_count'] + int(float(line[12]))
                entry_dict['documents_clicked'] = entry_dict['documents_clicked'] + int(line[8])
                entry_dict['document_click_depths'] = entry_dict['document_click_depths'] + [int(line[9])]
                entry_dict['serp_pages'] = entry_dict['serp_pages'] + int(line[7])
                entry_dict['total_serp_time'] = entry_dict['total_serp_time'] + float(line[25])
                
                entry_dict['p1'] = entry_dict['p1'] + [float(line[26])]
                entry_dict['p5'] = entry_dict['p5'] + [float(line[30])]
                entry_dict['p10'] = entry_dict['p10'] + [float(line[31])]
                entry_dict['p20'] = entry_dict['p20'] + [float(line[33])]
                
                entry_dict['new_at_1'] += [float(line[41])]
                entry_dict['new_at_5'] += [float(line[42])]
                entry_dict['new_at_10'] += [float(line[43])]
                entry_dict['new_at_20'] += [float(line[44])]
                
                entry_dict['adcg_5'] += [float(line[45])]
                entry_dict['adcg_10'] += [float(line[46])]
                
                # Used for calculating probabilities
                entry_dict['clicked_trec_rel'] += int(line[18])
                entry_dict['clicked_trec_nonrel'] += int(line[19])
                entry_dict['hover_trec_rel'] += int(line[13])
                entry_dict['hover_trec_nonrel'] += int(line[14])
                
                # Adding the task view clicked
                entry_dict['task_view_count'] = int(line[52])
                entry_dict['was_task_view_clicked'] = 0
                
                if entry_dict['task_view_count'] > 0:
                    entry_dict['was_task_view_clicked'] = 1
    
    f.close()
    return summary_data

def main(log_path, per_query_summary_path, filter_practice_topic=True):
    """
    Main function -- preps the data structures, and outputs the topic summaries.
    """
    log_data = get_log_data(log_path)
    filtered_log_data = log_data
    #query_summarised_data = get_summary_data(per_query_summary_path, filtered_log_data)
    
    # print 'user,topic,diversity,algorithm,tasktype,target,pass_or_fail,total_saved,trec_rels_saved,trec_nonrels_saved,trec_unassessed_saved,accuracy,trec_accuracy,estimated_accuracy,estimated_rels,docs_marked_with_new_entities,new_entities_found,queries_issued,documents_examined,documents_examined_per_query,documents_examined_depth_per_query,serp_pages_viewed,serp_pages_viewed_per_query,session_duration,total_query_time,per_query_time,total_document_time,per_document_time,total_serp_time,time_per_snippet,mean_p1,mean_p5,mean_p10,mean_p20,pm,pmr,pmn,pc,pcr,pcn,mean_new_at_1,mean_new_at_5,mean_new_at_10,mean_new_at_20,mean_adcg_5,mean_adcg_10,was_task_view_clicked,task_view_count'
    
    # for user in filtered_log_data:
    #     for topic in filtered_log_data[user]:
    #         if topic == PRACTICE_TOPIC and filter_practice_topic:
    #             continue
            
    #         log_entry = filtered_log_data[user][topic]
    #         query_summary_entry = query_summarised_data[user][topic]
            
    #         if log_entry['diversity'] == '1' or log_entry['diversity'] == '3':
    #             algorithm = 1  # 1 == diverisifed algorithm system (YoYo)
    #         else:
    #             algorithm = 0  # 0 == non-diversified algorithm (Hula)
            
    #         if log_entry['diversity'] == '1' or log_entry['diversity'] == '2':
    #             tasktype = 1  # 1 == aspectual retrieval task
    #         else:
    #             tasktype = 0  # 0 == ad-hoc retrieval task
            
    #         query_summary_entry['time_per_snippet'] = 0.0
            
    #         if query_summary_entry['hover_count'] > 0:
    #             query_summary_entry['time_per_snippet'] = query_summary_entry['total_serp_time'] / float(query_summary_entry['hover_count'])
            
    #         # Work out probabilities
    #         query_summary_entry['pm'] = 0.0
    #         query_summary_entry['pmr'] = 0.0
    #         query_summary_entry['pmn'] = 0.0
    #         query_summary_entry['pc'] = 0.0
    #         query_summary_entry['pcr'] = 0.0
    #         query_summary_entry['pcn'] = 0.0
            
    #         if (float(query_summary_entry['clicked_trec_rel']) + float(query_summary_entry['clicked_trec_nonrel'])) > 0:
    #             query_summary_entry['pm'] = (float(log_entry['trec_rels']) + float(log_entry['trec_nonrels']) + float(log_entry['trec_unassessed'])) / (float(query_summary_entry['clicked_trec_rel']) + float(query_summary_entry['clicked_trec_nonrel']))
            
    #         if query_summary_entry['clicked_trec_rel'] > 0:
    #             query_summary_entry['pmr'] = float(log_entry['trec_rels']) / float(query_summary_entry['clicked_trec_rel'])
            
    #         if query_summary_entry['clicked_trec_nonrel'] > 0:
    #             query_summary_entry['pmn'] = (float(log_entry['trec_nonrels']) + float(log_entry['trec_unassessed'])) / float(query_summary_entry['clicked_trec_nonrel'])
            
    #         if (query_summary_entry['hover_trec_rel'] + query_summary_entry['hover_trec_nonrel']) > 0:
    #             query_summary_entry['pc'] = (float(query_summary_entry['clicked_trec_rel']) + float(query_summary_entry['clicked_trec_nonrel'])) / (query_summary_entry['hover_trec_rel'] + query_summary_entry['hover_trec_nonrel'])
            
    #         if query_summary_entry['hover_trec_rel'] > 0:
    #             query_summary_entry['pcr'] = float(query_summary_entry['clicked_trec_rel']) / query_summary_entry['hover_trec_rel']
            
    #         if query_summary_entry['hover_trec_nonrel'] > 0:
    #             query_summary_entry['pcn'] = float(query_summary_entry['clicked_trec_nonrel']) / query_summary_entry['hover_trec_nonrel']
            
    #         print '{user},{topic},{diversity},{algorithm},{tasktype},{target},{indicator},{total},{trec_rels},{trec_nonrels},{trec_unassessed},{acc},{trec_acc},{estimated_acc},{estimated_rels},{entity_new_docs},{new_entities_found},{queries_issued},{documents_examined},{documents_examined_per_query},{documents_examined_depth_per_query},{serp_pages_viewed},{serp_pages_viewed_per_query},{session_duration},{total_query_time},{per_query_time},{total_document_time},{per_document_time},{total_serp_time},{time_per_snippet},{mean_p1},{mean_p5},{mean_p10},{mean_p20},{pm},{pmr},{pmn},{pc},{pcr},{pcn},{mean_new_at_1},{mean_new_at_5},{mean_new_at_10},{mean_new_at_20},{mean_adcg_5},{mean_adcg_10},{was_task_view_clicked},{task_view_count}'.format(
    #             user=user,
    #             topic=topic,
    #             diversity=log_entry['diversity'],
    #             algorithm=algorithm,
    #             tasktype=tasktype,
    #             target=log_entry['target'],
    #             indicator=(0 if log_entry['indicator'] == 'FAIL' else 1),  # 0 if FAIL, 1 if PASS
    #             total=log_entry['total'],
    #             trec_rels=log_entry['trec_rels'],
    #             trec_nonrels=log_entry['trec_nonrels'],
    #             trec_unassessed=log_entry['trec_unassessed'],
    #             acc=log_entry['acc'],
    #             trec_acc=log_entry['trec_acc'],
    #             estimated_acc=log_entry['estimated_acc'],
    #             estimated_rels=log_entry['estimated_rels'],
    #             entity_new_docs=log_entry['diversity_new_docs'],
    #             new_entities_found=log_entry['diversity_new_entities'],
    #             queries_issued=query_summary_entry['queries_issued'],
    #             documents_examined=query_summary_entry['documents_clicked'],
    #             documents_examined_per_query=query_summary_entry['documents_clicked'] / float(query_summary_entry['queries_issued']),
    #             documents_examined_depth_per_query=sum(query_summary_entry['document_click_depths']) / float(query_summary_entry['queries_issued']),
    #             serp_pages_viewed=query_summary_entry['serp_pages'],
    #             serp_pages_viewed_per_query=query_summary_entry['serp_pages'] / float(query_summary_entry['queries_issued']),
    #             session_duration=get_time_diff(log_entry['start'], log_entry['end']),
    #             total_query_time=query_summary_entry['total_query_time'],
    #             per_query_time=query_summary_entry['total_query_time'] / float(query_summary_entry['queries_issued']),
    #             total_document_time=query_summary_entry['total_document_time'],
    #             per_document_time=query_summary_entry['total_document_time'] / float(query_summary_entry['documents_clicked']),
    #             total_serp_time=query_summary_entry['total_serp_time'],
    #             time_per_snippet=query_summary_entry['time_per_snippet'],
                
                
    #             mean_p1=sum(query_summary_entry['p1'])/float(len(query_summary_entry['p1'])),
    #             mean_p5=sum(query_summary_entry['p5'])/float(len(query_summary_entry['p5'])),
    #             mean_p10=sum(query_summary_entry['p10'])/float(len(query_summary_entry['p10'])),
    #             mean_p20=sum(query_summary_entry['p20'])/float(len(query_summary_entry['p20'])),
                
    #             pm=query_summary_entry['pm'],
    #             pmr=query_summary_entry['pmr'],
    #             pmn=query_summary_entry['pmn'],
    #             pc=query_summary_entry['pc'],
    #             pcr=query_summary_entry['pcr'],
    #             pcn=query_summary_entry['pcn'],
                
    #             mean_new_at_1=sum(query_summary_entry['new_at_1'])/float(len(query_summary_entry['new_at_1'])),
    #             mean_new_at_5=sum(query_summary_entry['new_at_5'])/float(len(query_summary_entry['new_at_5'])),
    #             mean_new_at_10=sum(query_summary_entry['new_at_10'])/float(len(query_summary_entry['new_at_10'])),
    #             mean_new_at_20=sum(query_summary_entry['new_at_20'])/float(len(query_summary_entry['new_at_20'])),
                
    #             mean_adcg_5=sum(query_summary_entry['adcg_5'])/float(len(query_summary_entry['adcg_5'])),
    #             mean_adcg_10=sum(query_summary_entry['adcg_10'])/float(len(query_summary_entry['adcg_10'])),
                
    #             was_task_view_clicked=query_summary_entry['was_task_view_clicked'],
    #             task_view_count=query_summary_entry['task_view_count'],
    #         )
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <log_path> <per_query_summary_path>")
        sys.exit(1)
    
    log_path = sys.argv[1]
    per_query_summary_path = sys.argv[2]
    main(log_path, per_query_summary_path)