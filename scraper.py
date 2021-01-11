from lxml import html

import requests


def get_tree_from_url(url):
    response = requests.get(url)
    return html.fromstring(response.content)


class Movie(object):

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.magnet = None

    def fetch_magnet(self):
        tree = get_tree_from_url(self.url)
        try:
            magnet_anchor = [a for a in tree.xpath('//a') if "Magnet Download" in str().join(a.itertext())][0]
        except IndexError:
            raise Exception("Magnet URL not found.")
        self.magnet = magnet_anchor.attrib['href']
        return self.magnet

    def __repr__(self):
        return f"<Movie name='{self.name}'>"


class Scrape133x(object):

    BASE_URL = "https://www.1377x.to"
    PAGE_URL = "https://www.1377x.to/popular-movies"

    def get_page(self):
        tree = get_tree_from_url(self.PAGE_URL)
        return self.extract_recent_popular_movies(tree)

    def extract_recent_popular_movies(self, tree):
        movies = []
        try:
            table = tree.xpath('//table')[0]
        except IndexError:
            raise Exception("Most popular movies table doesn't exists.")
        for td in table.xpath('.//td[contains(@class, "name")]'):
            anchor = html.make_links_absolute(td.getchildren()[-1], self.BASE_URL)
            movie = Movie(anchor.text, anchor.attrib.get("href"))
            movies.append(movie)
        return movies

    def extract_data(self):
        return self.get_page()
