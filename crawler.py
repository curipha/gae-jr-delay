#!/usr/bin/env python
# coding: utf-8

import logging
import urllib2
import webapp2

from lxml import html

from datastore import Delay, DelayDetail, AreaDetail

class JrWest():
  URI = 'https://trafficinfo.westjr.co.jp/kinki.html'

  def __init__(self):
    delay = Delay()
    delay.isdelay = False

    self.delay = delay

  def update(self):
    if self.parse() >= 0:
      self.delay.put()
      logging.info('Commit to Google Cloud Datastore')
    else:
      logging.error('Failed to fetch and/or parse the HTML')
      logging.info('No record is committed to Google Cloud Datastore')

  def parse(self):
    XPATH_BASE = '//div[@id="syosai_1"][1]'
    XPATH_IMG  = '//div[@class="map"]/img'

    try:
      fp = urllib2.urlopen(self.URI)
    except:
      logging.error('HTTP fetch failed')
      return -1
    else:
      parser = html.fromstring(fp.read())


    dom = parser.xpath(XPATH_BASE + '/strong[1]/text()')

    if len(dom) > 0 and u'列車の遅れなどの情報はありません' in dom[0]:
      logging.info('Train operating normally')
      return 0


    dom = parser.xpath(XPATH_IMG)

    if len(dom) > 0:
      base = fp.geturl()[0:base.rfind('/') + 1]
      self.delay.image = ( dom[0].base or base ) + dom[0].attrib.get('src')


    dom = parser.xpath(XPATH_BASE + '/div[@class="jisyo"]')

    if len(dom) < 1:
      logging.error('Possibly DOM structure has been changed')
      return -1


    details = []

    for detail in dom:
      areas    = []
      area_dom = detail.findall('div[@class="jisyo_contents"]/p')

      for area in area_dom:
        if area.find('span[@class="line"]') is not None:
          areas.append(
            AreaDetail(
              line    = area.findtext('span[@class="line"]'),
              station = area.findtext('span[@class="station"]').replace(u'　', ' ')
            )
          )

      details.append(
        DelayDetail(
          title       = detail.findtext('div[@class="jisyo_hdr"]/h2[@class="jisyo_title"]/a[@id]'),
          description = detail.findtext('div[@class="jisyo_contents"]/p[@class="gaiyo"]'),
          areas       = areas
        )
      )

    self.delay.isdelay = True
    self.delay.details = details
    logging.info('Delay!')
    return 1

class ExecuteCrawler(webapp2.RequestHandler):
  def get(self):
    JrWest().update()


app = webapp2.WSGIApplication(
        [
          ('/cron/crawl', ExecuteCrawler)
        ]
      )

