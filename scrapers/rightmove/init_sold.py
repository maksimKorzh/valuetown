import csv
import pymongo
import json
import sys


class InitMongo:
    client = pymongo.MongoClient('mongodb+srv://alex:342124@cluster0-equas.mongodb.net/properties?retryWrites=true&w=majority')    
    db = client.properties
    
    def upload(self, filename):
        data = ''
        
        with open('./data/' + filename, 'r') as json_file:
            for line in json_file.read():
                data += line
            
            data = json.loads(data)
            
            for entry in data:
                entry['city'] = filename.split('.')[0]

            sold = self.db.sold
            sold.insert_many(data)
            sold.create_index([
                ('address', pymongo.TEXT),
                ('history.price', pymongo.TEXT),
                ('history.type', pymongo.TEXT),
                ('history.date', pymongo.TEXT),
                ('history.bedrooms', pymongo.TEXT)
            ], name='sold_houses', default_language='english')
            
            print('Uploaded data to MongoDb')

    def run(self):
        try:
            self.upload(sys.argv[1])
        except:
            print('usage: python3 init_sold.py <filename>')

if __name__ == '__main__':
    uploader = InitMongo()
    uploader.run()
