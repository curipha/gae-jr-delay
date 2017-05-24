#!/usr/bin/env python
# coding: utf-8

from google.appengine.ext import ndb

class AreaDetail(ndb.Model):
  line    = ndb.StringProperty(indexed=False)
  station = ndb.StringProperty(indexed=False)

class DelayDetail(ndb.Model):
  title       = ndb.StringProperty(indexed=False)
  description = ndb.StringProperty(indexed=False)
  areas       = ndb.LocalStructuredProperty(AreaDetail, repeated=True)

class Delay(ndb.Model):
  isdelay   = ndb.BooleanProperty(required=True)
  timestamp = ndb.DateTimeProperty(auto_now_add=True)
  image     = ndb.StringProperty(indexed=False)
  details   = ndb.LocalStructuredProperty(DelayDetail, repeated=True)

  def get_latest(self):
    return self.query().order(-self.__class__.timestamp).get()

  def get_delays(self, count = 10):
    return self.query().filter(self.__class__.isdelay == True).order(-self.__class__.timestamp).fetch(count)
