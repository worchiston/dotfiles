import csv


print('timestamp;ip;context;data')

with open('blah.csv', 'r') as f:
    reader = csv.reader(f)
    
    for row in reader:
        timestamp = row[0]
        ip = row[1]
        context = row[2]
        data = row[3]
        
        print('"{}","{}","{}","{}"'.format(timestamp, ip, context, data))
        

