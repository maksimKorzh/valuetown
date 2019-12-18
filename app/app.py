from flask import Flask
from flask_pymongo import PyMongo
from flask import render_template
from flask import jsonify
from flask import request


######################################################
# 
# App instance & config
#
######################################################

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://cmk:342124@todolist-c483l.gcp.mongodb.net/properties?retryWrites=true&w=majority"
mongo = PyMongo(app)


######################################################
# 
# Routes
#
######################################################

@app.route('/')
def home():
    return render_template('home.html', test=test)

@app.route('/api/birnimgham_active')
def birnimgham_active():
    results = []
    
    for house in mongo.db.houses.find({}):
        house['_id'] = str(house['_id'])
        results.append(house)
    
    return jsonify({'data': results})

@app.route('/api/birnimgham_sold', methods=['GET', 'POST'])
def birnimgham_sold():
    results = []
    
    for house in mongo.db.sold_houses.find({'$text': {'$search': request.args.get('q')}}):
        house['_id'] = str(house['_id'])
        results.append(house)
    
    return jsonify({'data': results})

def test():
    return 123

######################################################
# 
# Main driver
#
######################################################

if __name__ == '__main__':
    app.run(debug=True, threaded=True)





