import json
import requests
from lxml import html

URL = 'https://www.yelp.com/search?find_desc=Shopping&find_loc=Nanaimo%2C+BC&start={}'

class Scraper():
    def __init__(self) -> None:
        self.session = requests.Session()
        self.total_counts = 0
    def start(self):
        self.get_setting()

    def get_reponse(self,url):
        response = self.session.get(url=url)
        return response
    
    def get_setting(self):
        response = self.get_reponse(URL.format(0))
        tree = html.fromstring(response.text)

        json_element = tree.cssselect('script[data-hypernova-key=yelpfrontend__69115__yelpfrontend__GondolaSearch__dynamic]')
        if json_element:
            json_data = json.loads(json_element[0].text_content().replace('<!--', '').replace('-->', '').strip())

        else:
            pass

    
def main():
    scraper = Scraper()
    scraper.start()

if __name__ == "__main__":
    main()

