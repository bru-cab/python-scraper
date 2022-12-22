import scrapy
import os
from scrapy.crawler import CrawlerProcess
from datetime import datetime
import pandas

date = datetime.now().strftime("%d_%m_%Y")

class misbeneficiosSpider(scrapy.Spider):
    name = 'misbeneficios'
    start_urls = ['https://productos.misbeneficios.com.uy/tv-y-audio',
                  'https://productos.misbeneficios.com.uy/grandes-electros',
                  'https://productos.misbeneficios.com.uy/peque-os-electros',
                  'https://productos.misbeneficios.com.uy/tecnologia',
                  'https://productos.misbeneficios.com.uy/cuidado-personal',
                  'https://productos.misbeneficios.com.uy/fitness',
                  'https://productos.misbeneficios.com.uy/colchones-y-sommiers',
                  'https://productos.misbeneficios.com.uy/hogar-y-deco',
                  'https://productos.misbeneficios.com.uy/relojes-y-joyas',
                  'https://productos.misbeneficios.com.uy/apple',
                  'https://productos.misbeneficios.com.uy/samsung',
                  'https://productos.misbeneficios.com.uy/sony',
                  'https://productos.misbeneficios.com.uy/lg',
                  'https://productos.misbeneficios.com.uy/bosch',
                  'https://productos.misbeneficios.com.uy/whirlpool',
                  'https://productos.misbeneficios.com.uy/ariston',
                  'https://productos.misbeneficios.com.uy/candy',
                  'https://productos.misbeneficios.com.uy/divino']

    def parse(self, response):
        for products in response.css('div.product-item-info'):
            price = products.css('span.price-wrapper span.price::text').get()
            name = products.css('a.product-item-link::text').get()
#            id = products.css('li.product_id::text')
            if price and name:
                yield {'name': name.strip(),
                       'price': price.strip('U$S\xa0').strip()}
        next_page = response.css('a.next')
        if next_page:
            yield response.follow(next_page.attrib['href'], callback=self.parse)

os.chdir('C:\\Users\\cabre\\Desktop\\scraping\\misbeneficios\\data\\raw')
process = CrawlerProcess(
     settings={"FEEDS": {f"misbeneficios_{date}.csv": {"format": "csv"}}}
)
process.crawl(misbeneficiosSpider)
process.start()
