from google.appengine.ext import db

class Item(db.Model):
  item_title = db.StringProperty(multiline=False)
  item_author_name = db.StringProperty(multiline=False)
  item_link = db.StringProperty(multiline=False)
  item_description_strip = db.TextProperty()
  item_price = db.TextProperty()
  datetime = db.DateTimeProperty(auto_now_add=True)

# class User(db.Model):
  

