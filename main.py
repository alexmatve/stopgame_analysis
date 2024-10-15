from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd

import logging

import requests
import datetime

logging.basicConfig(level=logging.INFO, filename='stopgame.log',
                    format='%(levelname)s (%(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w')


# URL_TEMPLATE = "https://stopgame.ru/games/best?year_start=2000"


class Game:
    def __init__(self):
        self.title = str()
        self.rating = float()
        self.release = str()
        self.sites = list()
        self.developer = list()
        self.publisher = list()
        self.platforms = list()
        self.href = str()
        self.editorial_rating = str()


def connection_to_URL(URL_TEMPLATE: str):
    r = requests.get(URL_TEMPLATE)
    logging.info("Подключение к сайту прошло успешно")
    src = r.text
    soup = bs(src, "html.parser")
    return soup


def expand_list_of_games(page_number_start: int, page_number_end: int, list_games: list[Game]):
    for page_number in range(page_number_start, page_number_end + 1):
        URL_TEMPLATE = f"https://stopgame.ru/topgames?year_start=2000&p={page_number}"

        soup = connection_to_URL(URL_TEMPLATE)

        items = soup.find("div", {"class": "_games-grid_198ms_320"})
        games = items.find_all("a", {"class": "_card_1u499_4"})

        for game in games:
            obj = Game()
            obj.title = game['title']
            obj.href = game['href']
            list_games.append(obj)
    print(list_games[0].href)
    return list_games


def gain_info_about_games(list_games: list[Game]):
    for game in list_games:

        URL_TEMPLATE = "https://stopgame.ru" + game.href
        soup = connection_to_URL(URL_TEMPLATE)

        rating = soup.find("span", {"class": "_game-rating_11lgr_160 _game-rating--green_11lgr_1"}).text

        game.rating = float(rating)

        game_info = soup.find("dl", {"class": "_game-info__grid_1nyy2_969"})

        data = game_info.find_all("dd")
        headers = game_info.find_all("dt")

        for i in range(len(headers)):
            if headers[i].text == 'Дата выхода':
                game.release = data[i].text
            if headers[i].text == 'Сайт игры':
                for site in data[i].find_all('a'):
                    site = site.get('class')
                    if site is not None:
                        game.sites.extend(site)
            if headers[i].text == 'Разработчик':
                game.developer.append(data[2].find('a').text)
            if headers[i].text == 'Издатель':
                game.publisher.append(data[i].find("a").text)
            if headers[i].text == 'Платформы':
                for platform in data[i].find_all("a"):
                    game.platforms.append(platform.text)

        editorial_rating = soup.find('svg',
                                     {'class': '_stopgame-rating__icon_1nyy2_1 _stopgame-rating__icon--active_1nyy2_1'})
        if editorial_rating is not None:
            editorial_rating = editorial_rating.find('use')['href']
            game.editorial_rating = editorial_rating
        print(game.__dict__)


if __name__ == '__main__':
    list_games = expand_list_of_games(page_number_start=1, page_number_end=3, list_games=[])
    gain_info_about_games(list_games=list_games)
