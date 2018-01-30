# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
#from scrapy_webdriver.http import WebdriverRequest
from scrapy_splash import SplashRequest
import scrapy_splash

import logging

import socket
import requests


meta={
    'splash': {
        'args': {
            # set rendering arguments here
            'html': 1,
            'png': 1,

            # 'url' is prefilled from request url
            # 'http_method' is set to 'POST' for POST requests
            # 'body' is set to request body for POST requests
            #'proxy': 'http://127.0.0.1:8888'
        },

        # optional parameters
        #'endpoint': 'render.json',  # optional; default is render.json
        'endpoint' : 'execute',
        #'splash_url': '<url>',      # optional; overrides SPLASH_URL
        'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
        'splash_headers': {},       # optional; a dict with headers sent to Splash
        'dont_process_response': True, # optional, default is False
        'dont_send_headers': True,  # optional, default is False
        'magic_response': False,    # optional, default is True
    }
}

class DefaultExecuteSplashRequest(SplashRequest):
    '''
    This is a SplashRequest subclass that uses minimal default script
    for the execute endpoint with support for POST requests and cookies.
    '''
    SPLASH_SCRIPT = '''
    function last_response_headers(splash)
        local entries = splash:history()
        local last_entry = entries[#entries]
        return last_entry.response.headers
    end

    function main(splash)
        splash:init_cookies(splash.args.cookies)
        assert(splash:go{
            splash.args.url,
            headers=splash.args.headers,
            http_method=splash.args.http_method,
            body=splash.args.body,
            })
        assert(splash:wait(0.5))

        return {
            headers=last_response_headers(splash),
            cookies=splash:get_cookies(),
            html=splash:html(),
        }
    end
    '''

    def __init__(self, *args, **kwargs):
        kwargs['endpoint'] = 'execute'
        splash_args = kwargs.setdefault('args', {})
        splash_args['lua_source'] = self.SPLASH_SCRIPT
        splash_args['html'] = 1
        #splash_args['png'] = 1

        super(DefaultExecuteSplashRequest, self).__init__(*args, **kwargs)


class SplashRequest_Second_ListPage_Click(SplashRequest):
    '''
    This is a SplashRequest subclass that uses minimal default script
    for the execute endpoint with support for POST requests and cookies.
    '''
    SPLASH_SCRIPT = '''
    function last_response_headers(splash)
        local entries = splash:history()
        local last_entry = entries[#entries]
        return last_entry.response.headers
    end

    function main(splash)
        splash:init_cookies(splash.args.cookies)
        assert(splash:go{
            splash.args.url,
            headers=splash.args.headers,
            http_method=splash.args.http_method,
            body=splash.args.body,
            })
            
        assert(splash:wait(1))    
        
        --assert(splash:evaljs("function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};getElementByXpath('//*[@id=\\"content\\"]/table[2]/tbody/tr[1]/td/p/a').click();"))

        -- assert(splash:evaljs("function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};getElementByXpath('//*[@id=\\"content\\"]/table[2]/tbody/tr[1]/td/p/a').click();"))

        --assert(splash:evaljs("document.evaluate('//div[@id=\\"content\\"]//a[1]', document, null, XPathResult.ANY_TYPE, null).iterateNext().innerHTML"))
       
       
       --assert(splash:evaljs("document.evaluate('//div[@id=\\"content\\"]//a[1]', document, null, XPathResult.ANY_TYPE, null).iterateNext().click();"))
       
       assert(splash:evaljs("href = document.evaluate('//div[@id=\\"content\\"]//a[1]', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['href'].value;location.href=href"))
       
       
       
       
       assert(splash:wait(1)) 
       
        return {
            headers=last_response_headers(splash),
            cookies=splash:get_cookies(),
        html=splash:html(),
        --  html=splash:evaljs("function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};getElementByXpath('/html/head/title/text()')")
        --    html=splash:evaljs("document.evaluate('/html/body/meta[1]', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['content'].value")
            
        --    html=splash:evaljs("document.evaluate('//table[2]/tbody/tr[1]/td/p/a', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['href'].value")
        
        -- get the first drug link
        
        -- html=splash:evaljs("document.evaluate('//div[@id=\\"content\\"]', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['id'].value")
        
        -- html=splash:evaljs("document.evaluate('/html/body/center/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/div', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['id'].value")
       
        -- html=splash:evaljs("document.evaluate('/html/body/center/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/div[@id=\\"content\\"]/table[2]/tbody/tr[1]/td/p/a', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['href'].value")
       
       
        --html=splash:evaljs("document.evaluate('/html/body/center/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/div[@id=\\"content\\"]/table[2]//tr[1]/td/p/a', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['href'].value")
       
       -- only half
       
       --innerHTML 
       
       --html=splash:evaljs("document.evaluate('//div[@id=\\"content\\"]', document, null, XPathResult.ANY_TYPE, null).iterateNext().innerHTML")
       
        --html=splash:evaljs("document.evaluate('//div[@id=\\"content\\"]//a[1]', document, null, XPathResult.ANY_TYPE, null).iterateNext().innerHTML")
       
   
        -- SUCCESS
        -- html=splash:evaljs("document.evaluate('/html/body/center/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/div[@id=\\"content\\"]', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['id'].value")
        
        
        --document.evaluate('/html/body/center/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table[3]/tbody/tr/td[2]/div', document, null, XPathResult.ANY_TYPE, null).iterateNext().attributes['id'].value
        
        --    html=splash:evaljs("'Hello'.stringValue")
        --    html=splash:evaljs("'Hello'.stringValue")

        --  html="function getElementByXpath(path) {return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;};getElementByXpath('//*[@id=\\"content\\"]/table[2]/tbody/tr[1]/td/p/a').click();"
        }
    end
    '''

    def __init__(self, *args, **kwargs):
        kwargs['endpoint'] = 'execute'
        splash_args = kwargs.setdefault('args', {})
        splash_args['lua_source'] = self.SPLASH_SCRIPT
        splash_args['html'] = 1
        #splash_args['png'] = 1

        super(SplashRequest_Second_ListPage_Click, self).__init__(*args, **kwargs)

import codecs

class SfdaSpider(CrawlSpider):

    name = 'sfda'

    allowed_domains = ['sfda.gov.cn']
    #allowed_domains = ['igreatagain.com']

    start_urls = ['http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=124356560303886909015737447882']
    rules = (
        #详情页
        Rule(LinkExtractor(allow=r'.+', restrict_xpaths="/html/body/center/table[1]/tbody/tr[2]/td/table/tbody/tr/td[3]/table/tbody/tr[2]/td/table[3]"),
             callback='parse_item', follow=False),
    )

    #start_urls = ['http://www.igreatagain.com']

    #headers = {

    #    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    #    'Referer': 'http://app1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=25&tableName=TABLE25&title=%B9%FA%B2%FA%D2%A9%C6%B7&bcId=124356560303886909015737447882'

    #}

    def start_requests(self):

        #request = scrapy.Request(url=self.start_urls[0], callback=self.second_start)
        request = DefaultExecuteSplashRequest(
            url=self.start_urls[0], callback=self.second_start)

        #request.meta['proxy'] = "127.0.0.1:8888"

        yield request

        #return scrapy.Request

    def second_start(self, reponse):

        logging.debug('$$$$$$$$$$$$$$\nsecond_start')

        #request = scrapy.Request(reponse.url, dont_filter=True)

        request = SplashRequest_Second_ListPage_Click(
            reponse.url,
            dont_filter=True,
            callback=self.parse_item)

        proxies_urls = []

        # = random.choice(proxies_urls)

        #request.meta['proxy'] = "127.0.0.1:8888"

        yield request

    def parse_item(self, response):

        #//*[@id="content"]/div/div/table[1]/tbody/tr[3]/td[2]

        logging.debug("$$$$$$$$$$$$$$\nparse_item: " + response.url + '\n$$$$$$$$$$$$$$\n')

        #logging.debug("$$$$$$$$$$$$$$\nparse_item: " + response.body  + '\n$$$$$$$$$$$$$$\n')


        result = response.xpath('//*[@id="content"]/div/div/table[1]/tbody/tr[10]/td[2]//text()').extract_first()

        #file = codecs.open("parse_item.txt", "w", "utf-8")
        #file.write(result.decode('gbk'))

        with open('inner.html', 'wb') as file:

            file.write(result.encode('utf-8'))


        #file.close()

        logging.debug("$$$$$$$$$$$$$$\nparse_item: " + result + '\n$$$$$$$$$$$$$$\n')

        #logging.debug("parse_item: " + result.extract_first())


    def parse_list(self, response):

        logging.debug("parse_item: " + response.url)

        result = response.xpath('//*[@id="content"]/div/table[1]/tbody/tr/td/table/tbody/tr/td[2]/div//text()')

        logging.debug("parse_item: " + result.extract_first())

        #with open('1.html',"w") as file:

        #    file.write(response.body)

        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))

        self.myip = s.getsockname()[0]

        print("myip :" + self.myip)

        s.close()

        logging.debug("parse_item : " + response.url)

        item = {}

        item['title'] =  response.xpath('//*[@id="sharetitle"]/text()').extract_first()



        yield item

        #logging.debug('parse_item - number : ' + item['category'])
        #link = scrapy.Field()
        #location = scrapy.Field()
        #catagory = scrapy.Field()
        #snumber = scrapy.Field()

        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()

        #positions = response.xpath('//*[@id="position"]/div/table//tr')

        #positions = response.xpath('//*[@id="position"]/div/table/tr')[1:11]
        #response.xpath('//*[@id="position"]/div/table/tr[12]/td[1]//text()')

        #positions = response.xpath('//*[@id="position"]/div[1]/table/tbody/tr/td[1]/a')

        for position in positions:

            position_title = positions.xpath('./td[1]//text()').extract_first()

            logging.info("parse_item + " + position_title)

        return position_title

        """
