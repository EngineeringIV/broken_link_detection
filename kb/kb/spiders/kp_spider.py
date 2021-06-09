import scrapy
import pandas as pd
from scrapy_splash import SplashRequest
import os
import csv
import re
cwd = os.getcwd()
#docker run -it -p 8050:8050 --rm scrapinghub/splash


class KBSpider(scrapy.Spider):
    date='0125'
    name = "kb"
    df = pd.read_excel(cwd+'/Report_'+date+'_3.xlsx')
    start_urls = []

    def start_requests(self):
        for index, row in self.df.iterrows():
            country = row['Activity Map Page (revar23)'].split('_')[0]
            language = (row['Activity Map Page (revar23)'].split(':')[0]).split('_')[1]
            ID = row['Activity Map Page (revar23)'].split(':')[-1]
            url = 'https://support.lenovo.com/'+country+'/'+language+'/solutions/'+ID
            mp = row['Activity Map Link (revar24)']
            item = {}
            item['original'] = url
            item['broken'] = ''
            item['language'] = language
            item['mp'] = mp
            item['ID'] = ID
            item['country'] = country
            item['view'] = row['Page Views']
            yield SplashRequest(url, self.parse,args={
                            'wait': 2,
                            'html': 1
                        }, meta={'item':item})


    def parse(self, response):
        item = response.meta['item'].copy()
        mp = item['mp']
        all_href = None
        if "\"" not in mp and "\'" not in mp:
            all_href_mult = response.xpath('//*[@id="detailBody"]//a[text()="'+mp+'"]/@href').getall()

        else:
            all_href_mult = ['NONE']

        if len(all_href_mult) > 1:
                for all_href_1 in all_href_mult:
                    if '.com' not in all_href_1:
                        all_href_1 = response.urljoin(all_href_1)
                    elif 'https://' not in all_href_1:
                        #all_href = 'https://' + all_href
                        all_href_1 = response.urljoin(all_href_1)
                    item['broken'] = all_href_1
                    yield SplashRequest(all_href_1,callback=self.next_p, args={
                                    'wait': 2,
                                    'html': 1
                                },meta={'item':item})
        else:
            if "\"" not in mp and "\'" not in mp:
                all_href = response.xpath('//*[@id="detailBody"]//a[text()="'+mp+'"]/@href').get()
            else:
                ref = response.xpath('//*[@id="detailBody"]//a').getall()
                for r in ref:
                    res = re.search('>(.+?)<', r)
                    if res:
                        if res.group(1) == mp:
                            href = re.search('href=\"(.+?)\"', r)
                            if href:
                                all_href = href.group(1)

            if all_href is not None:
                if '.com' not in all_href:
                    all_href = response.urljoin(all_href)
                elif 'https://' not in all_href:
                    #all_href = 'https://' + all_href
                    all_href = response.urljoin(all_href)
                item['broken'] = all_href
                yield SplashRequest(all_href,callback=self.next_p, args={
                                'wait': 2,
                                'html': 1
                            },meta={'item':item})
            else:
                word = mp.split(' ')
                #ref = response.xpath('//*[@id="detailBody"]//a[contains(text(),"'+word[0]+') and contains(text(),'+word[-1]+')]').getall()
                ref = response.xpath(
                    '//*[@id="detailBody"]//a').getall()
                if ref is not None:
                    for r in ref:
                        res = re.search('>(.+?)<', r,re.DOTALL)
                        if res:
                            if word[0].upper() in res.group(1).upper() and word[-1].upper() in res.group(1).upper():
                                item['mp'] = res.group(1)
                                href = re.search('href=\"(.+?)\"', r)

                                if href and 'javascript' not in href.group(1):
                                    href = href.group(1)
                                    if '.com' not in href or 'https://' not in href:
                                        href = response.urljoin(href)
                                    item['broken'] = href
                                    yield SplashRequest(href, callback=self.next_p, args={
                                            'wait': 2,
                                            'html': 1
                                        }, meta={'item': item})

    def next_p(self,response):
        date='0125'
        data = [[response.meta['item']['ID'],response.meta['item']['country'],
                                  response.meta['item']['language'],
                                  response.meta['item']['original'],
                                  response.meta['item']['mp'],
                                  response.url,response.meta['item']['view']]]
        with open('Result_'+date+'.csv', 'a', encoding='utf-8-sig',newline='') as output:
            writer = csv.writer(output)
            if response.xpath('/html/head/title/text()').get() is not None:
                if 'Page Not Found' in response.xpath('/html/head/title/text()').get():
                    writer.writerows(data)




