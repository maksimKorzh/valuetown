import csv
import pymongo
import json

class InitMongo:
    client = pymongo.MongoClient('mongodb+srv://cmk:342124@todolist-c483l.gcp.mongodb.net/properties?retryWrites=true&w=majority')    
    db = client.properties
    
    def upload(self):
        data = ''
        
        with open('sold.json', 'r') as json_file:
            for line in json_file.read():
                data += line
            
            data = json.loads(data)
            
            sold_houses = self.db.sold_houses
            sold_houses.insert_many(data)
            sold_houses.create_index([
                ('address', pymongo.TEXT),
                ('history.price', pymongo.TEXT),
                ('history.type', pymongo.TEXT),
                ('history.date', pymongo.TEXT),
                ('history.bedrooms', pymongo.TEXT)
            ], name='sold_houses', default_language='english')
            
            print('Uploaded data to MongoDb')

    def run(self):
        self.upload()


if __name__ == '__main__':
    uploader = InitMongo()
    uploader.run()
