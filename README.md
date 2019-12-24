# Name
Value Town


# Credentials

heroku: asamila00@gmail.com | Valuetown99!
mongo: asamila00@gmail.com | Valuetown99
mongo_user: alex | 342124

# Snippets

css disable: {pointer-events: none; opacity: 0.4;}

<!-- City selector -->
<!--div class="text-left mb-4" hidden=true>
<input
  id="city-selector"
  name="cities"
  value="London, Slough"
  placeholder="Add cities..."
  class="form-control"
  style="width: 100%;"
/>
</div-->

''' tagator
cities = request.args.get('cities').split(',')

for each in mongo.db.active.find({'city': {'$in': cities}}):
    each['_id'] = str(each['_id'])
    results.append(each)
'''

db.collection.distinct('x') - unique values for field

/* Tagator
// Extract form data
var formData = $('#city-selector').serializeArray();

// Format form data as dictionary
$.each(formData, function(key, val) {
 args[val.name] = val.value;
});
*/

# TODO

1. select property type in bulk
 - We need 'Flats', 'Terraced' 'Semi Detached' 'Detached' and 'Bungalow' 
 - only houses
 - all
2. bedrroms 1 + to 6 +
3. I want to spend up to £X,
   I want to find X type of property,
   with a minimum of X bedrooms,
   and I would like to see results filtered to show properties potentially undervalued by X percent,
   assuming the properties shown can be purchased for X percent less than the asking price


# indexes
'''
active.create_index([
    ('title', pymongo.TEXT),
    ('address', pymongo.TEXT),
    ('description', pymongo.TEXT),
    ('date', pymongo.TEXT),
    ('seller', pymongo.TEXT),
    ('price', pymongo.TEXT)
], name=filename.split('.')[0], default_language='english')
'''
