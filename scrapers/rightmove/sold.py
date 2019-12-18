#https://www.rightmove.co.uk/house-prices/detail.html?
#country=england
#locationIdentifier=REGION%5E162&searchLocation=Birmingham&referrer=landingPage&index=25

import requests
from bs4 import BeautifulSoup
import os.path
import json
import time


class PropertyScraper:
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'cdUserType=none; permuserid=191215NQ6J5S7CLR27YGUPB2XVXCIK0F; _gaRM=GA1.3.221836134.1576410548; _gaRM_gid=GA1.3.1867305274.1576410548; __utmz=6980913.1576410549.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _gcl_au=1.3.1118436496.1576436784; OptanonAlertBoxClosed=2019-12-15T19:06:24.092Z; _fbp=fb.2.1576436785578.270522113; __gads=ID=dab09b0af44b09df:T=1576437062:S=ALNI_Mb4nnxMMC-cvgnwe4i1psUHb05b-g; _hjid=be75a7d1-864c-4c31-bdba-7d20ead3af2a; _ga=GA1.3.1932403474.1576410549; _gid=GA1.3.435917068.1576508420; TPCmaxPrice=50000; __utma=6980913.1932403474.1576410549.1576508410.1576586183.5; __utmc=6980913; cdUserType=none; rmsessionid=8fa0076c-a232-45e0-8503-1419fdeee800; TS01826437=012f990cd3e5265e9a3667f7b8c1b8d5c53670e00d0100fe98ff1929dbefb515f8cdcd8da8ef2b49086324ed97968c7772a83dfe0bbd7a3c8fc0bdaf1270c65d2f51a7f0aa706368e64e5168f0ef651b89306aed65198bcbbb5d961ae66ab4dc0f56bc57fa6cbbbdf2d1c4530581a1d3ebe6744d61; TS016a0c54=012f990cd35d9325041caac7af26ac2338f2c94b65aae17b16a9ea744af7f9f32e8326efd5ac68e2a3f6a4b20670386adf82bc1503; __utmv=6980913.|1=source=direct-none=1^3=user=sell=1^33=Login%20Register%20Modal%20Test=T=1; __utmt=1; JSESSIONID=267CE36C8A55149D494B033A1C97DFE8; svr=3101; TS019c0ed0=012f990cd3d82ce84ae5dda5346ae458029b3acde7df7281d3109b10bceec9f104a540a78aaa096a94ada5f17286e9b6f4ff652d4a8433ef452a47311435837f7891c693111d850879cd619adc8bbcc7fd254168c2; TS01ec61d1=012f990cd38e9bd96d1166a895d2af687676d37e400100fe98ff1929dbefb515f8cdcd8da88d7e9aa629586873eda85fd4cd910e6fac099d856194947ffabdb01da9104e58ed9ff8b586fab40817f1890a4c8fde70; __utmb=6980913.87.8.1576588476313; OptanonConsent=landingPath=NotLandingPage&datestamp=Tue+Dec+17+2019+15%3A18%3A01+GMT%2B0200+(Eastern+European+Standard+Time)&version=5.1.0&EU=false&groups=1%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false&consentId=92d15acb-c017-4cbd-b7f4-1ac4e5ce160c; eupubconsent=BOruFdhOruFdhAcABBENCb-AAAAo17__f__3_8_v1_9_NuzvOv_j_ef93VW8fvIvcEtzhY5d_uvUzxc4m_0vRc9ycgx85eprGsoxQ7qCsG-VOgd_5t__3ziXNohAAAAAAAAAAAAAAAA',
        'Host': 'www.rightmove.co.uk',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36'
    }
    
    base_url = 'https://www.rightmove.co.uk/house-prices/detail.html?country=england&locationIdentifier=REGION%5E162&searchLocation=Birmingham&referrer=landingPage'
    
    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url, headers=self.headers)
        print(' | Status code: %s' % response.status_code)
        
        return response
        
    def parse(self, html):
        #text = ''
        
        #with open('res.html', 'r') as html_file:
        #    for line in html_file.read():
        #        text += line
        
        content = BeautifulSoup(html, 'lxml')
        cards = content.findAll('div', {'class': 'soldDetails'})
        
        for card in cards:
            try:
                address = card.find('a').text
            except:
                address = card.find('div', {'class': 'soldAddress'}).text
            
            history = [[item.text for item in row.findAll('td')] for row in card.findAll('tr')]
            data = []
            
            for index in range(0, len(history)):
                data.append(    
                    {
                        'price': history[index][0],
                        'type': history[index][1],
                        'date': history[index][2],
                        'bedrooms': history[index][3]
                    }
                )
                
            self.to_json({
                'address': address,
                'history': data
            })

    def to_json(self, row):
        with open('sold.json', 'a') as json_file:
            json_file.write(json.dumps(row, indent=2) + ',\n')
    
    def run(self):        
        response = self.fetch(self.base_url)
        self.parse(response.text)
        time.sleep(2)
        
        for page in range(1, 40):
            index = str(page * 25)
            
            response = self.fetch(self.base_url + '&index=' + str(index))
            try:
                self.parse(response.text)
            except:
                print('skipped page %s' % page)

            time.sleep(2)


if __name__ == '__main__':
    scraper = PropertyScraper()
    scraper.run()
        
        
        
        
