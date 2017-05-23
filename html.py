#!/usr/bin/env python
# coding: utf-8

import jinja2
import os
import webapp2

from datetime import timedelta

from datastore import Delay

JINJA_ENV = jinja2.Environment(
  loader     = jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions = ['jinja2.ext.autoescape'],
  autoescape = True
)


class MainPage(webapp2.RequestHandler):
  def get(self):
    key = self.request.get('id')

    if len(key) > 0:

      if not key.isdigit():
        self.error(400)
        self.response.write('400 Bad request')
        return

      entity = Delay().get_by_id(int(key))

      if entity == None:
        self.error(404)
        self.response.write('404 Not found')
        return

    else:

      entity = Delay().get_latest()

      if entity == None:
        self.error(503)
        self.response.write('503 Service unavailable')
        return


    self.response.write(
        JINJA_ENV.get_template('template.html').render(
          {
            'image':     entity.image,
            'timestamp': ( entity.timestamp + timedelta(hours=9) ).strftime('%Y-%-m-%-d %-H:%M JST'),
            'details':   entity.details
          }
        )
      )

    return

class AtomFeed(webapp2.RequestHandler):
  def get(self):
    entities = Delay().get_delays()

    if entities == None:
      self.error(503)
      self.response.write('503 Service unavailable')
      return

    self.response.headers['Content-Type'] = 'application/atom+xml; charset=utf-8'

    self.response.write(
        JINJA_ENV.get_template('template.xml').render(
          {
            'base':     'https://jr-delay.appspot.com/',
            'update':   entities[0].timestamp,
            'entities': entities
          }
        )
      )

    return


app = webapp2.WSGIApplication(
        [
          ('/', MainPage),
          ('/feed', AtomFeed)
        ]
      )
