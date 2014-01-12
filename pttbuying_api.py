
"""PTTBuying API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""
#http://localhost:8080/_ah/api/explorer

import endpoints

from protorpc import messages
from protorpc import message_types

from protorpc import remote
# from datastore_models.item import Item

from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsModel


WEB_CLIENT_ID = 'turtle_poku_web'
ANDROID_CLIENT_ID = 'turtle_poku_andorid'
IOS_CLIENT_ID = 'turtle_poku_ios'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'pttbuying'

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

  # item_id = ndb.StringProperty(indexed=False)
  item_title = ndb.StringProperty(indexed=False)
  item_author_name = ndb.StringProperty(indexed=False)
  item_link = ndb.StringProperty(indexed=True)
  item_description_strip = ndb.StringProperty(indexed=False)
  item_price = ndb.StringProperty(indexed=False)
  datetime = ndb.DateTimeProperty(auto_now_add=True)
  
  # # This is a setter which will be used by the helper property "id", which we
  # # are overriding here. The setter used for that helper property is also named
  # # IdSet. This method will be called when id is set from a ProtoRPC query
  # # request.
  # def Item_idSet(self, value):
  #   # By default, the property "id" assumes the "id" will be an integer in a
  #   # simple key -- e.g. ndb.Key(MyModel, 10) -- which is the default behavior
  #   # if no key is set. Instead, we wish to use a string value as the "id" here,
  #   # so first check if the value being set is a string.
  #   if not isinstance(value, basestring):
  #     raise TypeError('ID must be a string.')
  #   # We call UpdateFromKey, which each of EndpointsModel.IdSet and
  #   # EndpointsModel.EntityKeySet use, to update the current entity using a
  #   # datastore key. This method sets the key on the current entity, attempts to
  #   # retrieve a corresponding entity from the datastore and then patch in any
  #   # missing values if an entity is found in the datastore.
  #   self.UpdateFromKey(ndb.Key(Item, value))

  # # This EndpointsAliasProperty is our own helper property and overrides the
  # # original "id". We specify the setter as the function IdSet which we just
  # # defined. We also set required=True in the EndpointsAliasProperty decorator
  # # to signal that an "id" must always have a value if it is included in a
  # # ProtoRPC message schema.

  # # Since no property_type is specified, the default value of
  # # messages.StringField is used.

  # # See matching_queries_to_indexes/main.py for more information on
  # # EndpointsAliasProperty.
  # @EndpointsAliasProperty(setter=Item_idSet, required=True)
  # def item_id(self):
  #   # First check if the entity has a key.
  #   if self.key is not None:
  #     # If the entity has a key, return only the string_id. The method id()
  #     # would return any value, string, integer or otherwise, but we have a
  #     # specific type we wish to use for the entity "id" and that is string.
  #     return self.key.string_id()

@endpoints.api(name='pttbuying', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])

class PttBuyingApi(remote.Service):
    """PttBuying API v1."""
    @Item.method(request_fields=('id',),
                  path='items/{id}', http_method='GET', name='item.MyModelGet')
    def MyModelGet(self, my_item):
      # Since the field "id" is included, when it is set from the ProtoRPC
      # message, the decorator attempts to retrieve the entity by its ID. If the
      # entity was retrieved, the boolean from_datastore on the entity will be
      # True, otherwise it will be False. In this case, if the entity we attempted
      # to retrieve was not found, we return an HTTP 404 Not Found.

      # For more details on the behavior of setting "id", see the sample
      # custom_alias_properties/main.py.
      if not my_item.from_datastore:
        raise endpoints.NotFoundException('Item not found.')
      return my_item

      
      # http://stackoverflow.com/questions/15508970/query-endpoint-user-by-email
      # query = Item.query(Item.id == my_item.id)
      # # We fetch 2 to make sure we have
      # matched_items = query.fetch(2)
      # if len(matched_items == 0):
      #   raise endpoints.NotFoundException('Item not found.')
      # elif len(matched_items == 2):
      #   raise endpoints.BadRequestException('Item not unique.')
      # else:
      #   return str(matched_items[0])

      # This is identical to the example in basic/main.py, however since the
      # ProtoRPC schema for the model now includes "id", all the values in "items"
      # will also contain an "id".

    @Item.query_method(query_fields=('limit', 'order', 'pageToken'), path='items', name='item.list')
    def MyModelList(self, query):
      return query


APPLICATION = endpoints.api_server([PttBuyingApi])