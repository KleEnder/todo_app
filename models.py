from google.appengine.ext import ndb

class Task(ndb.Model):
    name = ndb.StringProperty()
    message = ndb.TextProperty()
    message2 = ndb.TextProperty()
    checked = ndb.BooleanProperty(default=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

