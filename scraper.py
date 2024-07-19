import json
import csv
import requests
from lxml import html
SITE_URL = 'https://www.yelp.com'
URL = 'https://www.yelp.com/search?find_desc=Shopping&find_loc=Nanaimo%2C+BC&start={}'

class Scraper():
    def __init__(self) -> None:
        self.session = requests.Session()
        self.total_counts = 1
        self.urls = []
        self.step = 10
        self.business_type = 'retail'
        



    def start(self):
        self.get_setting()

        for i in range(0, ((self.total_counts + 9) // 10) * 10, self.step):
            print(f'** Scraping page {i // 10 + 1}...')
            self.get_page_urls(i)
        
        for url in self.urls:
            print(f'**** Scraping details for {url["name"]}')
            detail_data = self.get_business_details(url)
            self.save_csv(detail_data, 'result.csv')
            

    def write_file(self,file_path, data):
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            file.write(data)

    def save_csv(self, row, file_path):
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(row)

    def get_business_details(self, url):
        response = self.get_reponse(url['url'])
        tree = html.fromstring(response.text)
        json_element = tree.cssselect('script[type="application/ld+json"]')
        temp = dict()
        if json_element:
            for item in json_element:
                json_data = json.loads(item.text_content().strip())
                try:
                    temp['name'] = url['name']
                    temp['bizid'] = url['bizId']
                    temp['url'] = url['url']
                    temp['categories'] = url['categories']
                    temp['type'] = self.business_type
                    temp['store_banner'] = json_data['image']
                    temp['phone'] = json_data['telephone']
                    temp['address'] = json_data['address']
                    hours_table = tree.cssselect('table.hours-table__09f24__KR8wh')[0]
                    if hours_table:
                        temp['opening_hours'] = dict()
                        for row in hours_table.cssselect('tr.y-css-29kerx'):
                            temp['opening_hours'][row.cssselect('th').text_content().strip()] = row.cssselect('td').text_content().strip()
                    else:
                        pass
                    break
                except:
                    continue
            return temp
        else:
            return temp

    def get_reponse(self,url):
        response = self.session.get(url=url)
        return response
    
    def get_setting(self):
        response = self.get_reponse(URL.format(0))
        tree = html.fromstring(response.text)

        json_element = tree.cssselect('script[data-hypernova-key=yelpfrontend__69115__yelpfrontend__GondolaSearch__dynamic]')
        if json_element:
            json_data = json.loads(json_element[0].text_content().replace('<!--', '').replace('-->', '').strip())
            component_props = json_data['legacyProps']['searchAppProps']['searchPageProps']['mainContentComponentsListProps']
            for item in component_props:
                try:
                    self.total_counts = item['props']['totalResults']
                    print(f"Total Results: {self.total_counts}")
                    break
                except:
                    continue
        else:
            pass
    
    def get_page_urls(self, startResult):
        response = self.get_reponse(URL.format(startResult))
        tree = html.fromstring(response.text)
        json_element = tree.cssselect('script[data-hypernova-key=yelpfrontend__69115__yelpfrontend__GondolaSearch__dynamic]')
        if json_element:
            json_data = json.loads(json_element[0].text_content().replace('<!--', '').replace('-->', '').strip())
            component_props = json_data['legacyProps']['searchAppProps']['searchPageProps']['mainContentComponentsListProps']
            for item in component_props:
                try:
                    temp = dict()
                    temp['bizId'] = item['bizId']
                    temp['name'] = item['searchResultBusiness']['name']
                    temp['url'] = SITE_URL + item['searchResultBusiness']['businessUrl']
                    temp['categories'] = item['searchResultBusiness']['categories']
                    self.urls.append(temp)
                    print('#### Read vendor url : ' + temp['bizId'])
                except:
                    continue    
    
def main():
    scraper = Scraper()
    scraper.start()

if __name__ == "__main__":
    main()

