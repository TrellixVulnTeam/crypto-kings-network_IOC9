import requests
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
import urllib.request


def crawl(start, depth=2):
    """s"""
    coins = [start]

    for _ in range(10):

        holders = []
        for coin in coins:
            holders.append(top_holders(coin))

        coins = []
        for holder in holders:
            coins.append(top_coins(holder))


def top_holders(coin_address):
    """s"""

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'
    headers = {'User-Agent': user_agent, }

    request = urllib.request.Request(url, None, headers)  # The assembled request
    response = urllib.request.urlopen(request)
    data = response.read()  # The data u need
    pprint(data)


    #page = requests.get(base + coin_address)
    # page = requests.get('https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances')
    #
    soup = BeautifulSoup(data, 'html.parser')

    table = soup.find_all("tbody")

    pprint(table)

    # url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'


    # rows = list()
    # for row in table.find_all("tr"):
    #     rows.append(row)
    #     print(row)

    # for result in soup.findAll("table", class_="table table-md-text-normal table-hover"):
    #     print(result)
    # print('yes')
    # # pprint(soup)


def top_coins(holder_address):
    """s"""
    page = requests.get(base + holder_address)
    soup = BeautifulSoup(page.content, 'html.parser')
    # pprint(soup)


base = 'https://bscscan.com/token/'

crawl('0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances')
