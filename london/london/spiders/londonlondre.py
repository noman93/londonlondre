# -*- coding: utf-8 -*-
import scrapy


class LondonlondreSpider(scrapy.Spider):
    name = 'londonlondre'
    allowed_domains = ["londonrelocation.com"]

    def start_requests(self):
        yield scrapy.Request(url='https://londonrelocation.com/properties-to-rent/', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        })

    def parse(self, response):
        products = response.xpath("//div[@class='wd-25 pd-8']/a")
        for product in products:
            product_link = product.xpath(".//@href").get()

            yield response.follow(url=product_link, callback=self.parse_product)

    def parse_product(self, response):
        
        property_title = response.xpath(
            "normalize-space(//div[@class='right-cont']/div/h4/a/text())").get()
        price_per_month = response.xpath(
            "normalize-space(//div[@class='bottom-ic']/h5/text())").get()
        property_URL = response.urljoin(response.xpath(
            "//div[@class='right-cont']/div/h4/a/@href").get())
        yield {
            'Property': property_title.strip(),
            'Price Per Month': price_per_month.strip(),
            'Link': property_URL,
        }

        next_page = response.xpath(
            "(//div[@class='pagination']/ul/li/a)[2]/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_product, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
            })
            
        
