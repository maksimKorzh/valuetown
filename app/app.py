from flask import Flask
from flask_pymongo import PyMongo
from flask import render_template
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
    
    ''' tagator
    cities = request.args.get('cities').split(',')
    
    for each in mongo.db.active.find({'city': {'$in': cities}}):
        each['_id'] = str(each['_id'])
        results.append(each)
    '''
    
    city = request.args.get('city')
    distance = int(request.args.get('distance').split()[1])
    
    if 'land' in request.args.get('property'):
        prop = '.*' + request.args.get('property') + '.*'
    else:
        prop = '.*^' + request.args.get('bedrooms') + ' ' + request.args.get('property') + '.*'
    
    if distance:
        cities = [city, 'Slough']
    else:
        cities = [city]
    
    for each in mongo.db.active.find({
            'city': {'$in': cities}, 
            'title': re.compile(prop, re.IGNORECASE)
        }):
        
        each['_id'] = str(each['_id'])
        results.append(each)
    
    return jsonify({'data': results})

@app.route('/api/sold')
def sold():
    results = []
    query = request.args.get('q')
    city = request.args.get('city') 
    print('sold city:', city)
    
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





