#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

# TODO: python library cookiecutter?

BASE_URL = "https://boardgamearena.com"

all_games_url = f"{BASE_URL}/gamelist?section=all"
all_games_page = requests.get(all_games_url)

all_games_soup = BeautifulSoup(all_games_page.text, 'html.parser')

for game in all_games_soup.find_all("a", class_="gamelist_link_to_game"):
    game_href = game.get("href")

    game_url = f"{BASE_URL}{game_href}"

    game_page = requests.get(game_url)
    game_soup = BeautifulSoup(game_page.text, 'html.parser')

    is_premium = bool(game_soup.find(id="game_emblempremium", style=lambda value: value and 'display:inline-block' in value))

    game_text = game_soup.find("div", class_="icon16_nbrplayer").parent.find_all(text=True)

    number_of_players = game_text[2]
    average_duration = game_text[4]
    complexity = game_text[6]

    print(f"{game_href=}")
    print(f"{is_premium=}")
    print(f"{number_of_players=}")
    print(f"{average_duration=}")
    print(f"{complexity=}")
