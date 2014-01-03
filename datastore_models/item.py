
from google.appengine.ext import ndb
from google.appengine.api import search
from endpoints_proto_datastore.ndb import EndpointsModel

# In this model definition, we have included _message_fields_schema to define
# a custom ProtoRPC message schema for this model. To see a similar but
# different way to use custom fields, check out the samples in
# custom_api_response_messages/main.py and paging/main.py.
class Item(EndpointsModel):
  # This results in a ProtoRPC message definition with four fields, in the exact
  # order specified here: id, attr1, attr2, and created.
  # The fields corresponding to properties (attr1, attr2 and created) are string
  # fields as in basic/main.py. The field "id" will be an integer field
  # representing the ID of the entity in the datastore. For example if
  # my_entity.key is equal to ndb.Key(MyModel, 1), the id is the integer 1.

  # The property "id" is one of five helper properties provided by default to
  # help you perform common operations like this (retrieving by ID). In addition
  # there is an "entityKey" property which provides a base64 encoded version of
  # a datastore key and can be used in a similar fashion as "id", and three
  # properties used for queries -- limit, order, pageToken -- which are
  # described in more detail in paging/main.py.
  # _message_fields_schema = ('id', 'attr1', 'attr2', 'created')
  _message_fields_schema = ('id', 'item_title', 'item_link', 'item_price', 'item_description_strip', 'datetime')

  item_title = ndb.StringProperty(indexed=False)
  item_author_name = ndb.StringProperty(indexed=False)
  item_link = ndb.StringProperty(indexed=True)
  item_description_strip = ndb.StringProperty(indexed=False)
  item_price = ndb.StringProperty(indexed=False)
  datetime = ndb.DateTimeProperty(auto_now_add=True)
