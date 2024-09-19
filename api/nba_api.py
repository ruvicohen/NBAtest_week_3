import requests

from utils.urls import get_nba_url


def get_data_nba_from_api(url):
    response = requests.get(url)
    return response.json()
