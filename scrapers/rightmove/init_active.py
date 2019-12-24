from datetime import datetime
#from datetime import date
from datetime import timedelta
import csv
import pymongo
import json
import sys


class InitMongo:
    client = pymongo.MongoClient('mongodb+srv://alex:342124@cluster0-equas.mongodb.net/properties?retryWrites=true&w=majority')    
    db = client.properties
    
    def upload(self, filename):
        data = []
        
        with open('./data/' + filename, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                entry = dict(row)
                entry['city'] = filename.split('.')[0]
                entry['evaluation'] = {
                    'average': None,
                    'percentage': None
                }
                
                try:
                    entry['bedrooms'] = int(''.join([s for s in entry['title'] if s.isdigit()]))
                except:
                    entry['bedrooms'] = 'N/A'

                if 'flat' in entry['title'] or 'apartment' in entry['title']:
                    entry['type'] = 'flat'
                elif 'terraced' in entry['title']:
                    entry['type'] = 'terraced'
                elif 'semi detached' in entry['title']:
                    entry['type'] = 'semi detached'
                elif 'detached' in entry['title']:
                    entry['type'] = 'detached'
                elif 'bungalow' in entry['title']:
                    entry['type'] = 'bungalow'
                elif 'house' in entry['title']:
                    entry['type'] = 'house'
                else:
                    entry['type'] = 'other'
                
                if entry['price'] != 'POA':
                    entry['price'] = int(entry['price'].split('£')[1].replace(',', ''))
                
                if entry['date'] != 'yesterday' and entry['date'] != '':
                    entry['date'] = datetime.strptime(entry['date'], '%d/%m/%Y')
                else:
                    entry['date'] = datetime.today() - timedelta(1)

                data.append(entry)

            active = self.db.active
            active.insert_many(data)
            
            print('Uploaded "%s" data to MongoDb' % sys.argv[1])

    def run(self):
        #try:
        self.upload(sys.argv[1])
        self.client.close()
        #except:
        #    print('usage: python3 init_active.py <filename>')

if __name__ == '__main__':
    uploader = InitMongo()
    uploader.run()
