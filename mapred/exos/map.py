import sys
import csv
import json

data = csv.DictReader(sys.stdin, delimiter=',')


def mapper(row):
    row['time'] = row['date'].split(' ')[1]
    row['magnitude'] = round(float(row['magnitude']), 1)
    row['tension entre plaque'] = round(float(row['tension entre plaque']), 1)
    row['secousse'] = True if row['secousse'] == 'True' else False
    del row['date']
    return row

for line in data:
    row_data = mapper(line)
    json_data = json.dumps(row_data)
    print(json_data)
