# -*- coding: utf-8 -*-
import scrapy
from ..items import GlobaltradeItem

class TradeSpider(scrapy.Spider):
    name = 'trade'
    
    start_urls = ['https://www.globaltrade.net/expert-service-provider.html']
    download_delay = .5
    item=GlobaltradeItem()
    cur_page=''
    page_number= 2
    
    def parse(self, response):
        
        next_page="https://www.globaltrade.net/United-States/expert-service-provider.html"
        
        yield response.follow(next_page, callback = self.page2)


    def page2(self,response):
        d=[]
        
        b=response.css('p.sp-name').css('a::attr(href)').extract()
        
        for i in b:
            
            s='https://www.globaltrade.net'
            news=''
            news=s+i

            yield response.follow(news,callback=self.output)
            
        pages='https://www.globaltrade.net/United-States/expert-service-provider.html?pageSize=10&orderBy=1&filterByPost=false&filterByRef=false&topicClear=false&industryClear=false&currentPage='+ str(TradeSpider.page_number) 
        if TradeSpider.page_number <= 401:
          TradeSpider.page_number+=1
          yield response.follow(pages, callback=self.page2)
    def output(self,response):
        sec=response.css('div.section.details tr')
        
        for sect in sec:
            table2=sect.css('td')[0].css('td ::text').extract()
            TradeSpider.item['page_url']=response.url

            if table2[0]=='About:':
                about=sect.css('td')[1].css('p ::text').extract()
                TradeSpider.item['about']=about
            if table2[0]=='Website:':
                website=sect.css('td')[1].css('a ::text').extract()
                TradeSpider.item['website']=website[0]
            if table2[0]=='Languages spoken:':
                language_spoken=sect.css('td')[1].css('td ::text').extract()
                TradeSpider.item['language_spoken']=language_spoken
        
        rows=response.css('div.profile-details  tr')
        for row in rows:
            primary_locations=[]
            primary_locations.append(response.css('td').css('td ::text').extract())
            k=response.css('td')[0].css('td ::text').extract()
            m=response.css('td').css('td.color-1F4862 ::text').extract()

            

            if k[0]=='Primary location:':
                y=response.css('td')[1].css('span ::text').extract()
                TradeSpider.item['primary_location']=y[1]
                
            if m[0]=='Main Area of Expertise:':
                z=response.css('td').css('a.mainExp ::text').extract()
                TradeSpider.item['area_of_expertise']=z        
        image=response.css('div.image').css('img ::attr(data-original)').extract()
        
        TradeSpider.item['logo']=image
        titles=response.css('h1.sp-title').css('h1 ::text').extract()
        
        TradeSpider.item['title']=titles
        
        sub_titles=response.css('span.sub').css('span ::text').extract()
        
        TradeSpider.item['sub_title']=sub_titles
        
        
        filename = 'results4.json' 
        with open(filename, 'a+') as f:
            f.writelines(str(TradeSpider.item))
            f.write('\n')
        self.log('Saved file %s' % filename)