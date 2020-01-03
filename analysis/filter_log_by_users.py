import sys

def read_user_list(user_list_path):
    """
    Reads the user list file, and creates a list out of it.
    """
    f = open(user_list_path, 'r')
    user_list = []

    for line in f:
        line = line.strip()
        user_list.append(line)

    f.close()
    return user_list

def main(log_path, user_list_path):
    """
    Does the magic.
    """
    user_list = read_user_list(user_list_path)

    f = open(log_path, 'r')

    for line in f:
        line = line.strip()
        line_split = line.split(' ')

        userid = line_split[3]

        if userid in user_list:
            print(line)

    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <log_file> <user_list_file>")
        print("<log_file> is the log file to filter")
        print("<user_list_file> is a list of user IDs (one per line) that you want to KEEP")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2])
