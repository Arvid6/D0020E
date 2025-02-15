from idlelib import query

import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
import json
from datetime import datetime
API_KEY = 'cfb7b20b5a119d264e14128c9508b7e2'


def get_url(url):
    payload = {'api_key': API_KEY, 'url': url, 'autoparse': 'true', 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url


def create_google_url(query, site=''):
    google_dict = {'q': query, 'num': 100, }
    if site:
        web = urlparse(site).netloc
        google_dict['as_sitesearch'] = web
        return 'http://www.google.com/search?' + urlencode(google_dict)
    return 'http://www.google.com/search?' + urlencode(google_dict)


class GoogleSpider(scrapy.Spider):
    name = 'findweb'
    allowed_domains = ['api.scraperapi.com']
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 10,
        'RETRY_TIMES': 5}


def start_requests(self):
    queries = ['asana+reviews', 'clickup+reviews', 'best+project+management+software',
               'best+project+management+software+for+small+teams']
    for query in queries:
        url = create_google_url(query)
        yield scrapy.Request(get_url(url), callback=self.parse, meta={'pos': 0})


def parse(self, response):
    di = json.loads(response.text)
    pos = response.meta['pos']
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for result in di['organic_results']:
        title = result['title']
        snippet = result['snippet']
        link = result['link']
        item = {'title': title, 'snippet': snippet, 'link': link, 'position': pos, 'date': dt}
        pos += 1
        yield item
    next_page = di['pagination']['nextPageUrl']
    if next_page:
        yield scrapy.Request(get_url(next_page), callback=self.parse, meta={'pos': pos})