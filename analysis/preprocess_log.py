import sys

#
# Author: David Maxwell
# Date: 2020-01-02
#

# What do we do in this script?
# - Work out the final interaction that takes place during each search session -- and whacks in a SEARCH_TASK_COMPLETE event with the same timestamp.
# - Removes extra space from the VIEW_PERFORMANCE log entry.

EXAMINED_TOPICS = ['341', '347', '367', '408', '435']  # What topics are expected?

def main(log_file_path):
    """
    Does the magic!
    Puts each log line into a data structure, does some pre-processing, then spits log lines out user by user to stdout.
    """
    f = open(log_file_path, 'r')
    entries = {} # By userid, then topic in the nested dictionary. Values in the nested dictionary are lists of log entries.

    for line in f:
        line = line.strip()
        line_split = line.split(' ')
        
        # Remove the extra blank space (from VIEW_PERFORMANCE)
        while '' in line_split:
            line_split.remove('')

        userid = line_split[3]
        topic = '0'
        topic_index = 8
        add_extra_column = False

        # Work out the topic -- we need to do this because the log file is inconsistent in columns...
        while topic not in EXAMINED_TOPICS:
            topic = line_split[topic_index]
            topic_index = topic_index - 1

            if topic not in EXAMINED_TOPICS:
                add_extra_column = True

            # Should never get here.
            if topic_index == len(line_split) - 1:
                break
        
        # Add an extra column before the topic to ensure that everything checks out.
        if add_extra_column:
            line_split.insert(7, '-')
        
        if userid not in entries.keys():
            entries[userid] = {}
        
        if topic not in entries[userid]:
            entries[userid][topic] = []
        
        entries[userid][topic].append(line_split)
    
    f.close()

    # Now we should have a nice data structure of entries on a per-user and topic basis.
    # Now we can work out what the last search event is in the log, and append a further log entry.
    for userid in entries.keys():
        for topic in entries[userid].keys():
            last_line = None
            end_time = None

            for line in entries[userid][topic]:
                action = line[9]
                
                # If the user completes to a time limit, this is the session end time.
                if action in ['SESSION_COMPLETED', 'EXPERIMENT_TIMEOUT']:
                    end_time = line[0:2]
                    break
                
                # If the user ends the session before time is up, take the last search interaction date/time as the session end time.
                if action in ['VIEW_PERFORMANCE', 'CONCEPT_LISTING_COMPLETED'] and not end_time:
                    end_time = last_line[0:2]
                    break
                
                last_line = line
            
            # Copy the first entry in the log, and rename the copy's action to SEARCH_TASK_COMPLETE.
            # Also set the date and time to the end date and time from above.
            new_entry = entries[userid][topic][0].copy()
            new_entry[-1] = 'SEARCH_TASK_COMPLETE'
            new_entry[0] = end_time[0]
            new_entry[1] = end_time[1]

            # Append the SEARCH_TASK_COMPLETE event to the end of the user's log entries.
            entries[userid][topic].append(new_entry)
    
    # Now spit everything out, per user, per topic.
    for userid in entries.keys():
        for topic in entries[userid].keys():
            for line in entries[userid][topic]:
                print(' '.join(line))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Pre-processes the log file for use with log processing scripts.")
        print("Assumes the input log IS in chronological order!")
        print("Note that the events may no longer appear to be in chronological order; this is okay -- we order by user instead. Later scripts don't care about this.")
        print(f"Usage: {sys.argv[0]} <log_file>")
        sys.exit(1)
    
    main(sys.argv[1])