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

    def start_requests(self):
        # https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#cookies-debug
        # Multiple cookie sessions per spider
        for i,url in enumerate(self.start_urls):
            yield scrapy.Request(url,
                                 self.parse,
                                 method='POST',
                                 meta={'cookiejar': i}
                                 )

    def parse(self,response):
        meta = response.xpath('//div[@class="box-producto-in"]/a/@href')
        for m in meta:
            url = urlparse.urljoin(response.url, m.extract())
            # Seleccionamos la direccion
            yield scrapy.Request(url,
                                 self.parse_plan,
                                 meta={'cookiejar': response.meta['cookiejar']}
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

        data1 = response.xpath('//input[@id="item_id"]/@value').extract()
        for op1 in response.xpath('//select[@id="listas_id"]/option/@value'):
            data2 = op1.extract()
            for op2 in response.xpath('//select[@id="cuotas_id"]/option/@value'):
                data3 = op2.extract()
                #for plan in response.xpath('//label[@class="radioCustom_label"]'):
                for plan in response.xpath('//div[@class="box-planes option_radio"]'):
                    data4_body = html.fromstring(plan.extract())
                    data4 = data4_body.xpath("//input/@value")[0]
                    prec_plan = data4_body.xpath("//label/div/span").pop().text
                    nomb_plan = data4_body.xpath("//label/div/h3").pop().text
                    arr_carc = []
                    for item_plan in data4_body.xpath("//label/ul/li/span"):
                        arr_carc.append({item_plan.text:""})

                    for cont,item_plan in enumerate(data4_body.xpath("//label/ul/li/p")):
                        arr_carc[cont][arr_carc[cont].keys()[0]] = item_plan.text

                    url = urlparse.urljoin("http://catalogo.claro.com.pe", "combo-precios.php?data1="+data1[0]+
                                                         "&data2="+data2+"&data3="+data3+
                                                         "&data4="+data4)
                    yield scrapy.Request(url,
                                         self.parse_item,
                                         meta={'v_marca': marca,
                                               'v_nombre': nombre,
                                               'v_descripcion': descripcion,
                                               'v_arr_esp': arr_esp,
                                               'v_prec_plan': prec_plan,
                                               'v_nomb_plan': nomb_plan,
                                               'v_arr_carc_plan': arr_carc,
                                               'cookiejar': response.meta['cookiejar']
                                               }
                                         )

    def parse_item(self, response):
        print response._body
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
