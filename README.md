pttbuying_parser
================

PTT Buyng GAE Parser

Metadata browsing:
==================

* GET http://fleebuy.appspot.com/rest/metadata
** (gets all known types)

* GET http://fleebuy.appspot.com/rest/metadata/Item
** (gets the Greeting type profile)

Object Retrieval:
=================

* GET http://fleebuy.appspot.com/rest/Item
** (gets the first N Item instances)

* GET http://fleebuy.appspot.com/rest/Item?offset=10
** (gets the next N Item instances, starting at offset 10.  Note
   the returned list element contains an "offset" attribute.  If it has a
   value, that is the next offset to use to retrieve more results.  If it is
   empty, there are no more results).

* GET http://fleebuy.appspot.com/rest/Item?feq_datetime=2014-01-12T08:07:09.200150
** (gets the Item instances, starting with a date property "equal to" 2014-01-12T08:07:09.200150.
   Available operators:
     - "feq_" -> "equal to"
     - "flt_" -> "less than"
     - "fgt_" -> "greater than"
     - "fle_" -> "less than or equal to"
     - "fge_" -> "greater than or equal to"
     - "fne_" -> "not equal to"
     - "fin_" -> "in <comma_separated_list>"
   Multiple operators may be provided, they are AND'ed together).

* GET http://fleebuy.appspot.com/rest/Item/aglzfmZsZWVidXlyEQsSBEl0ZW0YgICAgMD6kwsM
** (gets a single WholeEnchilada instance)

