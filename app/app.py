from flask import Flask
from flask_pymongo import PyMongo
from flask import render_template
from datetime import datetime
from datetime import timedelta
from flask import jsonify
from flask import request
import re


######################################################
# 
# App instance & config
#
######################################################

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://alex:342124@cluster0-equas.mongodb.net/properties?retryWrites=true&w=majority"
mongo = PyMongo(app)


######################################################
# 
# Routes
#
######################################################

@app.route('/')
def home():
    return render_template('view.html')


######################################################
# 
# API
#
######################################################

@app.route('/api/active')
def active():
    results = []

    city = request.args.get('city')
    distance = request.args.get('distance')
    proptype = request.args.get('property')
    bedrooms = request.args.get('bedrooms')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    max_price = request.args.get('max_price')
    min_price = request.args.get('min_price')
    poa_check = request.args.get('poa')
    
    title = '.*'
    price_min = 0
    price_max = 999999999
    date_from = datetime.today() - timedelta(5000)
    date_to = datetime.today()
    
    if distance != 'Not specified':
        cities = [city, 'Slough']
    else:
        cities = [city]
    
    if bedrooms != 'Any number':
        title += '^' + bedrooms + ' '
    
    if proptype != 'Any type':
        title += proptype

    if from_date != '':
        date_from = datetime.strptime(from_date, '%Y-%m-%d')
    
    if to_date != '':
        date_to = datetime.strptime(to_date, '%Y-%m-%d')

    if min_price != '':
        price_min = int(min_price)
    
    if max_price != '':
        price_max = int(max_price)
    
    if poa_check == 'true':
        poa = 'POA'
    else:
        poa = ''
    
    if 'land' in proptype:
        title = '.*' + proptype

    for each in mongo.db.active.find({
            'city': {'$in': cities}, 
            #'title': re.compile(title, re.IGNORECASE),
            '$or': [{'price': {'$gte': price_min, '$lte': price_max}}, {'price': poa}],
            'date': {'$gte': date_from, '$lte': date_to}
        }):
        
        each['_id'] = str(each['_id'])
        results.append(each)
    
    return jsonify({'data': results})

@app.route('/api/sold')
def sold():
    results = []
    query = request.args.get('q')
    city = request.args.get('city')
    
    for each in mongo.db.sold.find({'$text': {'$search': query}, 'city': city}):
        each['_id'] = str(each['_id'])
        results.append(each)
    
    return jsonify({'data': results})


######################################################
# 
# Main driver
#
######################################################

if __name__ == '__main__':
    app.run(debug=True, threaded=True)





