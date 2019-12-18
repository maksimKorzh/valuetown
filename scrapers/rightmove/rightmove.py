import requests
from bs4 import BeautifulSoup
import os.path
import csv
import time


class PropertyScraper:
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'cdUserType=none; permuserid=191215NQ6J5S7CLR27YGUPB2XVXCIK0F; _gaRM=GA1.3.221836134.1576410548; _gaRM_gid=GA1.3.1867305274.1576410548; __utmz=6980913.1576410549.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=6980913.|1=source=direct-none=1^33=Login%20Register%20Modal%20Test=T=1; _gcl_au=1.3.1118436496.1576436784; OptanonAlertBoxClosed=2019-12-15T19:06:24.092Z; _fbp=fb.2.1576436785578.270522113; __gads=ID=dab09b0af44b09df:T=1576437062:S=ALNI_Mb4nnxMMC-cvgnwe4i1psUHb05b-g; __utmc=6980913; cdUserType=none; _hjid=be75a7d1-864c-4c31-bdba-7d20ead3af2a; rmsessionid=6e65507f-aa5f-437a-8291-043df414df90; TS01826437=012f990cd38a9a287c8e494be6e82a21fde33ad3ba7f750e30fd354e978106727d12d70d8c6a7835c218fff8f62a161768e03afdd62feb40a757fe75355a80ea10f0962c83844260401e2aeaaf44b105bb2a44113c01250e040b547b0c1278319af6785da8e018329aa5b9672ba52640ae38c34623; __utma=6980913.1932403474.1576410549.1576503006.1576508410.4; __utmt=1; TS016a0c54=012f990cd37cdc85eace6b45785e12a06d2af1550d404170ab5577a4e76781b8104c4548fa717978274772900cd94600657dcfab2d; _ga=GA1.3.1932403474.1576410549; _gid=GA1.3.435917068.1576508420; __utmt_RESPONSIVE-TRACKER=1; __utmt_ALL_SITE-TRACKER=1; __utmt_MAIN_SITE_ONLY-TRACKER=1; TPCmaxPrice=50000; JSESSIONID=4F8235DE968A845E4B97A8261E0EA29D; svr=2705; TS01ec61d1=012f990cd3109268e7cfdfdecf9f935aa7722a8e967f750e30fd354e978106727d12d70d8c0ad29df0a94888d0eaa0f9ec80c237f22a95e1f85e270216ed7434d9b6bb044fe336c15e97da3053286f6afecdf5066be07aaed016c4a30d492bec49bc694ac7; TS019c0ed0=012f990cd3b1966ef753fcad7b8915b87246def80590f753979c363179305cd1c7d4513e45fb61a0fdf065891607f6f7fe2bde82d52f4bfb10a2700bf59d5b0246c354afc9fbd5a43d96c18ac68522f5fdbb9075db; _dc_gtm_UA-3350334-63=1; _gat_UA-3350334-63=1; __utmb=6980913.40.7.1576508855947; OptanonConsent=landingPath=NotLandingPage&datestamp=Mon+Dec+16+2019+17%3A08%3A17+GMT%2B0200+(Eastern+European+Standard+Time)&version=5.1.0&EU=false&groups=1%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false&consentId=92d15acb-c017-4cbd-b7f4-1ac4e5ce160c; eupubconsent=BOrrCrQOrrCrQAcABBENCb-AAAAo17__f__3_8_v1_9_NuzvOv_j_ef93VW8fvIvcEtzhY5d_uvUzxc4m_0vRc9ycgx85eprGsoxQ7qCsG-VOgd_5t__3ziXNohAAAAAAAAAAAAAAAA',
        'Host': 'www.rightmove.co.uk',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36'
    }
    
    base_url = 'https://www.rightmove.co.uk/property-for-sale/Birmingham.html'
    
    def fetch(self, url, params):
        print('HTTP GET request to URL: %s' % url, end='')        
        response = requests.get(url, params=params, headers = self.headers)
        print(' | Status code: %s' % response.status_code)
        
        return response
        
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        
        titles = [title.text.strip() for title in content.findAll('h2', {'class': 'propertyCard-title'})]
        addresses = [address.text for address in content.findAll('span', {'data-bind': 'text: displayAddress'})]
        descriptions = [description.text for description in content.findAll('span', {'data-test': 'property-description'})]
        dates = [date.text.split(' ')[-1] for date in content.findAll('span', {'class': 'propertyCard-branchSummary-addedOrReduced'})]
        sellers = [''.join(seller.text.split('by ')).strip() for seller in content.findAll('span', {'class': 'propertyCard-branchSummary-branchName'})]
        prices = [price.text.strip() for price in content.findAll('div', {'class': 'propertyCard-priceValue'})]
        images = [image['src'] for image in content.findAll('img', {'data-bind': 'attr: { src: propertyImages.mainImageSrc}'})]
        
        for index in range(0, len(titles)):
            self.to_csv({
                'title': titles[index],
                'address': addresses[index],
                'description': descriptions[index],
                'date': dates[index],
                'seller': sellers[index],
                'price': prices[index],
                'image': images[index],
            })

    def to_csv(self, row):
        if os.path.isfile('property.csv'):
            file_exists = True
        else:
            file_exists = False
        
        with open('property.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=row.keys())
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
    
    def run(self):
        params = {
            'locationIdentifier': 'REGION^162',
            'index': '0',
            'propertyTypes': '', 
            'mustHave': '',
            'dontShow': '',
            'furnishTypes': '', 
            'keywords': ''
        }
        
        response = self.fetch(self.base_url, params)
        self.parse(response.text)
        time.sleep(2)
        
        for page in range(1, 42):
            params['index'] = str(page * 24)
            
            response = self.fetch(self.base_url, params)
            self.parse(response.text)
            time.sleep(2)


if __name__ == '__main__':
    scraper = PropertyScraper()
    scraper.run()
        
        
        
        
