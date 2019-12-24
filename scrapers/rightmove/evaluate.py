import pymongo
import json
import sys
import re


class Evaluator:
    client = pymongo.MongoClient('mongodb+srv://alex:342124@cluster0-equas.mongodb.net/properties?retryWrites=true&w=majority')    
    db = client.properties
    active = []
    price_range = 5000
    
    def fetch(self, city):
        self.active = [each for each in self.db.active.find({'city': city})]
        print('successfully fetched %d active items' % len(self.active))

    def evaluate(self):
        for active in self.active:
            if active['price'] != 'POA' and active['price'] > 1000000:
                continue
                        
            if active['price'] == 'POA':
                continue
        
            if active['type'] == 'house' or active['type'] == 'other':
                proptype = ''
            else:
                proptype = active['type']

            similar = [
                each for each in self.db.sold.find({
                    'city': active['city'],
                    '$text': {'$search': active['address']},
                    'history.type': re.compile(proptype, re.IGNORECASE)
                })
            ]
            
            average = 0
            count = 0
            
            if len(similar):
                for sold in similar:
                    for item in sold['history']:
                        if (item['price'] >= active['price'] - self.price_range) and (item['price'] <= active['price'] + self.price_range):
                            average += item['price']
                            count += 1
            try:
                average = average / count 
                
                item = {
                    'average': average,
                    'percentage': ((average - active['price']) / active['price']) * 100,
                }

                print('updating: \n\n', json.dumps(item, indent=2))
                
                self.db.active.update_one(
                    {'_id': active['_id']},
                    {
                        '$set': {
                            'evaluation': item
                        }
                    }
                )
                                
            except:
                print('N/A for price', active['price'])

    def run(self):
        #try:
        self.fetch(sys.argv[1])
        self.evaluate()
        self.client.close()
        #except:
        #    print('usage: python3 init_active.py <filename>')


if __name__ == '__main__':
    evaluator = Evaluator()
    evaluator.run()
