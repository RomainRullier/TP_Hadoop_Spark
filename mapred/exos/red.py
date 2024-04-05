import sys
import json

data = {}
def calculate_amplitude(records):
    return max(record['magnitude'] for record in records)

def detect_important_events(records, threshold=5.0):
    important_events = [record for record in records if record['magnitude'] >= threshold]
    return important_events

def reducer_by_city(row):
    if row['secousse']:
        if row['ville'] not in data:
            data[row['ville']] = []
        data[row['ville']].append(row)
def reducer_evenements_importants(city, values):
    important_events = detect_important_events(values)
    amplitude = calculate_amplitude(values)
    return json.dumps({
        'ville': city,
        'amplitude': amplitude,
        'evenements_importants': important_events
    })

def correlations_between_evenements(city, values):
    for record in values['evenements_importants']:
        for record2 in values['evenements_importants']:
            if record != record2:
                if record['magnitude'] == record2['magnitude']:
                    return {
                        'ville': city,
                        'evenement1': record,
                        'evenement2': record2,
                        'correlation': 'Les deux événements ont la même magnitude'
                    }
                else:
                    return {
                        'ville': city,
                        'evenement1': record,
                        'evenement2': record2,
                        'correlation': 'Les deux événements n\'ont pas la même magnitude',
                        'difference': record['magnitude'] - record2['magnitude']
                    }
def aggregate_by_time(records):
    aggregation = {}
    for record in records:
        # Extraction de la tranche horaire depuis le timestamp
        time_slot = record['time'].split(':')[0]
        if time_slot not in aggregation:
            aggregation[time_slot] = {
                'count': 0,
                'total_magnitude': 0,
                'max_magnitude': 0
            }
        aggregation[time_slot]['count'] += 1
        aggregation[time_slot]['total_magnitude'] += record['magnitude']
        if record['magnitude'] > aggregation[time_slot]['max_magnitude']:
            aggregation[time_slot]['max_magnitude'] = record['magnitude']
    # Calcul de la magnitude moyenne par tranche horaire
    for time_slot, values in aggregation.items():
        values['average_magnitude'] = values['total_magnitude'] / values['count']
    return aggregation

for line in sys.stdin:
    reducer_by_city(json.loads(line))

for city in data:
    row_data = reducer_evenements_importants(city, data[city])
    with open('events.json', 'w') as f:
        json.dump(data, f, indent=4)
    data[city] = json.loads(row_data)
    corr_data = correlations_between_evenements(city, data[city])
    with open('corr.json', 'w') as f:
        json.dump(corr_data, f, indent=4)

def aggregate_by_time(records):
    aggregation = {}
    for record in records:
        time_slot = record['time'].split(':')[0]
        if time_slot not in aggregation:
            aggregation[time_slot] = {
                'count': 0,
                'total_magnitude': 0,
                'max_magnitude': 0
            }
        aggregation[time_slot]['count'] += 1
        aggregation[time_slot]['total_magnitude'] += record['magnitude']
        if record['magnitude'] > aggregation[time_slot]['max_magnitude']:
            aggregation[time_slot]['max_magnitude'] = record['magnitude']
    for time_slot, values in aggregation.items():
        values['average_magnitude'] = values['total_magnitude'] / values['count']
    return aggregation

for city, records in data.items():
    data[city]['aggregated_by_time'] = aggregate_by_time(data[city]['evenements_importants'])

with open('aggregated_data.json', 'w') as f:
    json.dump(data, f, indent=4)