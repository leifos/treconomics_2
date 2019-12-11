
import os


f = open('awords.csv', 'r')
i = 0

for line in f:
    line = line.strip().split(',')
    row = '<tr>'
    for element in line:
        row = row + '<td>'+element+'</td>'
    row = row + '</tr>'
    print(row)
    i = i + 1
    if divmod(i,20)[1]==0:
        print(os.linesep)

