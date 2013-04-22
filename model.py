# File used to define the entity types within the data store.
# Data is stored hierarchically: all items belong to a user,
# all users belong to a network.

from google.appengine.ext import db

# An object representing a network (a college/university/other
# community group if we include non-colleges)
class Network(db.Model):
    name = db.StringProperty()
    # some form of token

    def exists(self):
        ex = False
        q = Network.all()
        q.filter("name =", self.name)            
        q.run(limit=1)
        for entity in q:
            return entity
        return None

# An object representing a user of our application
class User(db.Model):
    firstName = db.StringProperty()
    lastName = db.StringProperty()
    # fb_id_token

    def fullName(self):
        return self.firstName + " " + self.lastName

    def exists(self):
        ex = False
        q = User.all()
        q.filter("firstName =", self.firstName)
        q.filter("lastName =", self.lastName)
        q.run(limit=1)
        for entity in q:
            return entity
        return None

# An object representing an item within the marketplace
class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty(multiline=True)
    # photo?

    def exists(self):
        ex = False
        q = Item.all()
        q.filter("name =", self.name)            
        q.run(limit=1)
        for entity in q:
            return entity
        return None


