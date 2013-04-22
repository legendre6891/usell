# File used to define the entity types within the data store.
# Data is stored hierarchically: all items belong to a user,
# all users belong to a network.

from google.appengine.ext import db

# An object representing a network (a college/university/other
# community group if we include non-colleges)
class Network(db.Model):
    name = db.StringProperty()
    # some form of token

# An object representing a user of our application
class User(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    # fb_id_token

    def fullName(self):
        return self.first_name + " " + self.last_name

# An object representing an item within the marketplace
class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty(multiline=True)
    # photo?