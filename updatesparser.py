from bs4 import BeautifulSoup
from utilities.fetchinfo import fetch_info

class UpdateParser:
    def __init__(self, url):
        self.html_content = fetch_info(url)["content"]["rendered"]
        self.soup = BeautifulSoup(self.html_content, 'html.parser')
        self.divs = self.parse_divs()
        self.divinfo_list = [DivInfo(div).jsonify() for div in self.divs]

    
    def parse_html(self):
        divs = self.soup.select("html > body > div:nth-of-type(1) > div > div > div > div:nth-of-type(2) > div")
        if divs:
            return divs
        else:
            print('Target div not found')
            return []

    def parse_old_html(self):
        divs = self.soup.select("html > body > div:nth-of-type(1) > div > div > div > div")
        if divs:
            return divs[2:-1]
        else:
            print('Target div not found')
            return []

    def parse_divs(self):
        divs = self.soup.select("div:nth-of-type(2) > div")
        print(divs)
        return divs

        

class DivInfo:
    def __init__(self, div):
        self.div = div
        self.text = self.get_text()
        self.links = self.get_links()
        self.images = self.get_images()
        self.ytvideos = self.get_ytvideos()

    def get_text(self):
        return self.div.text.replace("<<<Download file>>>", "")

    def get_links(self):
        return [link.get('href') for link in self.div.find_all('a')]

    def get_images(self):
        return [img.get('src') for img in self.div.find_all('img')]

    def get_ytvideos(self):
        return [video.get('src') for video in self.div.find_all('iframe')]
    
    def jsonify(self):
        return {
            "text": self.text.strip().split("\n"),
            "links": self.links,
            "images": self.images,
            "ytvideos": self.ytvideos
        }