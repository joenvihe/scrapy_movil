# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import urlparse
from lxml import html

class SpclaroSpider(CrawlSpider):
    name = 'spclaro'
    allowed_domains = ['catalogo.claro.com.pe']
    start_urls = ['http://catalogo.claro.com.pe/catalogo/personas/renovacion/acuerdo-18/celulares/todos/todos']

    #rules = (
    #    Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    #)

    def parse(self,response):
        meta = response.xpath('//div[@class="box-producto-in"]/a/@href')
        for m in meta:
            url = urlparse.urljoin(response.url, m.extract())
            # Seleccionamos la direccion
            yield scrapy.Request(url,
                                 self.parse_plan
                                 )

    def parse_plan(self, response):
        marca = response.xpath('//div[@class="box-eq-txt"]/h3/text()').extract()
        nombre = response.xpath('//div[@class="box-eq-txt"]/h2/text()').extract()
        descripcion = response.xpath('//div[@class="box-eq-txt"]/p[2]/text()').extract()
        list_esp = response.xpath('//ul[@class="info-espec"]/li')
        arr_esp=[]
        for i in list_esp:
            r = html.fromstring(i.extract())
            nomb=r.xpath("//p").pop().text
            val=r.xpath("//span").pop().text
            arr_esp.append({"nombre":nomb,"valor":val})


    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
