import csv
import pymongo
import json

class InitMongo:
    data = []
    client = pymongo.MongoClient('mongodb+srv://cmk:342124@todolist-c483l.gcp.mongodb.net/properties?retryWrites=true&w=majority')    
    db = client.properties
    
    def upload(self):
        with open('property.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            
            for row in reader:
                self.data.append(dict(row))
            
            houses = self.db.houses
            houses.insert_many(self.data)
            houses.create_index([
                ('title', pymongo.TEXT),
                ('address', pymongo.TEXT),
                ('description', pymongo.TEXT),
                ('date', pymongo.TEXT),
                ('seller', pymongo.TEXT),
                ('price', pymongo.TEXT)
            ], name='search_houses', default_language='english')
            
            print('Uploaded data to MongoDb')

    def run(self):
        self.upload()


if __name__ == '__main__':
    uploader = InitMongo()
    uploader.run()
