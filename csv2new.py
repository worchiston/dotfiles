import csv
from datetime import datetime, timezone
from dateutil import tz


print('timestamp;ip;context;data')

with open('old_log.csv', 'r') as fd:
    reader = csv.reader(fd)
    
    for row in reader:
        timestamp = row[1]
        ip = row[0]
        context = 'pet'
        data = ''
        
        # String to datetime object
        new_timestamp = datetime.strptime(
            timestamp,
            '%Y-%m-%d %H:%M:%S' # Old format
        )
        
        # Identify current timestamp/datetime object as UTC
        new_timestamp = new_timestamp.replace(tzinfo=timezone.utc)
        
        # UTC -> AEST
        new_timestamp = new_timestamp.astimezone(tz.gettz('Australia/Sydney'))
        
        print('{},{},{},{}'.format(new_timestamp.isoformat(), ip, context, data))
        

