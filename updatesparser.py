from bs4 import BeautifulSoup
from utilities.fetchinfo import fetch_info, fetch_info_html
import re

DATE_REGEX = re.compile(r"\b\d{4}[-/]\d{2}[-/]\d{2}\b")


class UpdateParser:
    def __init__(self, url):
        #html = fetch_info(url)["content"]["rendered"]
        html = fetch_info_html(url)
        self.soup = BeautifulSoup(html, "html.parser")

        self._clean_html()
        self.divinfo_list = self._extract_announcements()


    def _clean_html(self):
        for tag in self.soup([
            "script", "style", "nav", "footer", "header", "noscript"
        ]):
            tag.decompose()

    def _find_announcements_root(self):
        anchor = self.soup.find(
            lambda tag: tag.name in ("strong")
            and "الإعلانات العامة للبرامج التخصصية" in tag.get_text(strip=True)
        )

        if not anchor:
            # Fallback: use body
            return self.soup.body

        return anchor.find_next("div")

    def _extract_announcements(self):
        root = self._find_announcements_root()
        if not root:
            return []

        nodes = list(root.descendants)

        announcements = []
        current_nodes = []

        for node in nodes:
            if not hasattr(node, "name"):
                continue

            # Detect start of a new announcement via date
            if node.name == "p":
                text = node.get_text(strip=True)
                if DATE_REGEX.search(text):
                    if current_nodes:
                        ann = self._parse_nodes(current_nodes)
                        announcements.append(ann)
                        current_nodes = []

            if node.name in ("p", "a", "img", "iframe"):
                current_nodes.append(node)

        # Append last announcement
        if current_nodes:
            ann = self._parse_nodes(current_nodes)
            announcements.append(ann)

        return announcements

    def _parse_nodes(self, nodes):
        text = []
        links = []
        images = []
        ytvideos = []

        for node in nodes:
            if node.name == "p":
                t = node.get_text(strip=True)
                if t and "Download file" not in t and "<<<" not in t:
                    text.append(t)

            elif node.name == "a":
                href = node.get("href")
                if href:
                    links.append(href)

            elif node.name == "img":
                src = node.get("src")
                if src:
                    images.append(src)

            elif node.name == "iframe":
                src = node.get("src")
                if src:
                    ytvideos.append(src)

        return {
            "text": text,
            "links": list(dict.fromkeys(links)),
            "images": list(dict.fromkeys(images)),
            "ytvideos": list(dict.fromkeys(ytvideos)),
        }

    

        

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