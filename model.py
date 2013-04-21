class Network(db.Model):
    name = db.StringProperty()
    # some form of token

class User(db.Model):
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    # fb_id_token

    def fullName(self):
        return self.first_name + " " + self.last_name

class Item(db.Model):
    name = db.StringProperty()
    description = db.StringProperty(multiline=True)
    # photo?