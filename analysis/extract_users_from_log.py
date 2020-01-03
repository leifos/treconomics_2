import os
import sys



def readUserids( ufile ):
    udict = {}
    f = open(ufile,"r")
    for line in f.readlines():
        tmp = line.strip()
        #tmp = tmp.decode("utf-8")
        udict[tmp] = 1

    f.close()
    return udict



def main():
    if len(sys.argv) == 3:
        log_file = sys.argv[1]
        user_file = sys.argv[2]

        ud = readUserids(user_file)

        f = open(log_file,"r")
        for line in f.readlines():
            parts = line.split()
            if parts[3].strip() in ud:
                print(line.strip())

    else:
        print(f"{sys.argv[0]} <logfile> <userlistfile>")

if __name__ == "__main__":
    sys.exit(main())
