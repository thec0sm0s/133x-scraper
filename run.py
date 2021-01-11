from scraper import Scrape133x

import json


if __name__ == "__main__":
    scraper = Scrape133x()
    ret = scraper.extract_data()
    movies = []
    for movie in ret:
        movie.fetch_magnet()
        movies.append(dict(name=movie.name, magnet=movie.magnet))
        print("Fetched: ", movie.name)
    with open("movies.json", "w") as file:
        json.dump(movies, file)
