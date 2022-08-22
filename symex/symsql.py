## This module wraps SQLalchemy's methods to be friendly to
## symbolic / concolic execution.

import fuzzy
import sqlalchemy.orm

oldget = sqlalchemy.orm.query.Query.get
def newget(query, primary_key):
  ## Exercise 5: your code here.
  ##
  ## Find the object with the primary key "primary_key" in SQLalchemy
  ## query object "query", and do so in a symbolic-friendly way.
  ##
  ## Hint: given a SQLalchemy row object r, you can find the name of
  ## its primary key using r.__table__.primary_key.columns.keys()[0]
  print "query:", query, "primary_key: ", primary_key, ","
  rows = query.all()
  #rows1 = sqlalchemy.orm.query.Query.all()
  for row in rows:
    print "row table", row.__table__.primary_key
    pk = row.__table__.primary_key.columns.keys()[0]
    pkval = row.__dict__[pk]
    if primary_key.__eq__(pkval):
        return row
  return None

sqlalchemy.orm.query.Query.get = newget
