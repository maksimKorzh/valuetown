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

/* Tagator
// Extract form data
var formData = $('#city-selector').serializeArray();

// Format form data as dictionary
$.each(formData, function(key, val) {
 args[val.name] = val.value;
});
*/

# TODO

1. Add distance selector


# In a perfect world

Create our own valuation estimate based, not only properties that have sold in the immediate surrounding streets,
but to specifically find properties that share the same features such as number of bedrooms & property type
e.g. flat, detached house, semi-detached house etc within the area providing a much more accurate estimation

So currently we have:
6. Potentially we could have price reduction to show if properties have had price reductions? It helps a buyer determine if a seller might be desperate to sell. Reducing the price can be a sign of desperation.
7. Then we can apply our estimates as to the true values.
   Perhaps we can call this the ValueTown Estimate.
   Potentially subdivide into 3 categories.
       1 lowest estimate, 
       1 average estimate,
       1 highest estimate and 
       state the number of samples the estimates are based on to indicate their accuracy.


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
