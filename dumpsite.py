# import requests
# import pandas as pd
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from time import sleep
#
# from pprint import pprint
# import urllib.request
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.action_chains import ActionChains
#
#
# class Crawler:
#     """crawler class"""
#
#     def __init__(self):
#
#         self.iterations = 0
#         """c"""
#
#         chrome_options = Options()
#         chrome_options.add_argument("--headless")
#
#         self.driver = webdriver.Chrome('C:\\Program Files\\chromedriver_win32\\chromedriver.exe',
#                                        options=chrome_options)
#         """c"""
#
#         self.driver.set_window_size(1440, 900)
#         """c"""
#
#         self.wait_time = 3
#         """c"""
#
#         self.base_url = 'https://bscscan.com'
#         """c"""
#
#         # start_url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'
#
#         self.coins = []
#         """c"""
#
#         self.holders = []
#         """c"""
#
#         self.queue_holder = []
#         """c"""
#
#         self.queue_coin = []
#         """c"""
#
#         self.df = pd.DataFrame()
#         """c"""
#
#     def get_top_coins(self, holders):
#         """Get the top coins"""
#
#         for holder in holders:
#
#             self.driver.get(holder.url)
#
#             sleep(3)
#
#             element = self.driver.find_element_by_id("availableBalanceDropdown")
#
#             element.click()
#
#             html = self.driver.page_source
#
#             # self.driver.close()
#
#             soup = BeautifulSoup(html, 'html5lib')
#
#             coin_list = soup.find_all('li', class_="list-custom list-custom-BEP-20")
#
#             for item in coin_list:
#                 print(item.text)
#                 for a in item.find_all('a', href=True):
#                     print("Found the URL:", a['href'])
#
#     def get_top_holders(self, coins):
#         """Get the top holders"""
#
#         # c
#         for coin in coins:
#             # temp_driver = self.driver.copy()
#
#             self.driver.get(f'{coin.url}#balances')
#
#             sleep(self.wait_time)
#
#             iframe = self.driver.find_element(By.ID, 'tokeholdersiframe')
#
#             self.driver.switch_to.frame(iframe)
#
#             html = self.driver.page_source
#
#             # driver.quit()
#             soup = BeautifulSoup(html, 'html5lib')
#
#             tbody = soup.find('tbody')
#
#             tr_tags = tbody.find_all('tr')
#
#             address = []
#             percent = []
#             value = []
#
#             for tr in tr_tags:
#                 td_tags = tr.find_all('td')
#                 address.append(td_tags[1].text)
#                 percent.append(td_tags[3].text)
#                 value.append(td_tags[4].text)
#
#             df = pd.DataFrame((address, percent, value))
#
#             df = df.T
#
#             df.columns = ['address', 'percent', 'value']
#
#             print(df)
#
#
# class Coin:
#     """coin"""
#
#     def __init__(self, parent, address, name=None, symbol=None):
#         self.parent = parent
#         """c"""
#
#         self.name = name
#         """c"""
#
#         self.symbol = symbol
#         """c"""
#
#         self.address = address
#         """c"""
#
#         self.url = f'{self.parent.base_url}/token/{self.address}'
#         """c"""
#
#         self.price = []
#         """c"""
#
#         self.top_holders = []
#         """c"""
#
#
# class Holder:
#     """c"""
#
#     def __init__(self, parent, address, name=None):
#         self.parent = parent
#         """c"""
#
#         self.address = address
#         """h"""
#
#         self.coins = []
#         """h"""
#
#         self.balance = []
#         """h"""
#
#         self.url = f'{self.parent.base_url}/address/{self.address}'
#         """c"""
#
#
# #
# # def crawl(start, depth=2):
# #     """s"""
# #     coins = [start]
# #
# #     top_holders(coins)
# #
# #     # for _ in range(10):
# #     #
# #     #     holders = []
# #     #     for coin in coins:
# #     #         holders.append(top_holders(coin))
# #
# #     # coins = []
# #     # for holder in holders:
# #     #     coins.append(top_coins(holder))
# #
# #
# # def top_holders(coin_address):
# #     """s"""
# #
# #     user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
# #
# #     url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'
# #     headers = {'User-Agent': user_agent, }
# #
# #     # request = urllib.request.Request(url, None, headers)  # The assembled request
# #     # response = urllib.request.urlopen(request)
# #     # data = response.read()  # The data u need
# #     # #pprint(data)
# #     #
# #     #
# #     # #page = requests.get(base + coin_address)
# #     # # page = requests.get('https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances')
# #     # #
# #     # soup = BeautifulSoup(data, 'html.parser')
# #     #
# #     # #table = soup.find_all("tbody")
# #     #
# #     # table = soup.find_all('div', id="maintable")
# #     #
# #     # pprint(table)
# #
# #     # url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'
# #
# #     while True:
# #         r = requests.get(url)
# #
# #         soup = BeautifulSoup(r.text, 'html.parser')
# #
# #         refresh = soup.find_all('meta', attrs={'http-equiv': 'refresh'})
# #         # print 'refresh:', refresh
# #
# #         if not refresh:
# #             break
# #
# #         # wait = int(refresh[0].get('content','0').split(';')[0])
# #         # print 'wait:', wait
# #         # time.sleep(wait)
# #
# #     # ---
# #
# #     table = soup.find_all('table')
# #
# #     if table:
# #         # table = table[-1]
# #         # data = [str(td.text.split()[0]) for td in table.select("td.tableLeft")]
# #
# #         print(table)
# #     else:
# #         print("[!] no data")
# #
# #     # rows = list()
# #     # for row in table.find_all("tr"):
# #     #     rows.append(row)
# #     #     print(row)
# #
# #     # for result in soup.findAll("table", class_="table table-md-text-normal table-hover"):
# #     #     print(result)
# #     # print('yes')
# #     # # pprint(soup)
# #
# #
# # def top_coins(holder_address):
# #     """s"""
# #     page = requests.get(base + holder_address)
# #     soup = BeautifulSoup(page.content, 'html.parser')
# #     # pprint(soup)
#
#
# def main():
#     """main"""
#
#     crawler = Crawler()
#
#     # base = 'https://bscscan.com/token/'
#     #
#     # # crawl('0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances')
#     #
#     # user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#     #
#     # url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'
#     # headers = {'User-Agent': user_agent, }
#     #
#     # request = urllib.request.Request(url, None, headers)
#     # response = urllib.request.urlopen(request)
#     # data = response.read()
#     # pprint(data)
#
#     # url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'
#
#     chrome_options = Options()
#     # chrome_options.add_argument("--disable-extensions")
#     # chrome_options.add_argument("--disable-gpu")
#     # chrome_options.add_argument("--no-sandbox") # linux only
#     chrome_options.add_argument("--headless")
#     # chrome_options.headless = True # also works
#     driver = webdriver.Chrome('C:\\Program Files\\chromedriver_win32\\chromedriver.exe', options=chrome_options)
#     start_url = 'https://bscscan.com/token/0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82#balances'
#     driver.get(start_url)
#
#     sleep(3)
#
#     iframe = driver.find_element(By.ID, 'tokeholdersiframe')
#
#     driver.switch_to.frame(iframe)
#
#     html = driver.page_source
#
#     driver.quit()
#     soup = BeautifulSoup(html, 'html5lib')
#
#     tbody = soup.find('tbody')  # , class_='table table-md-text-normal table-hover')
#
#     tr_tags = tbody.find_all('tr')
#
#     address = []
#     percent = []
#     value = []
#
#     for tr in tr_tags:
#         td_tags = tr.find_all('td')
#         address.append(td_tags[1].text)
#         percent.append(td_tags[3].text)
#         value.append(td_tags[4].text)
#
#     df = pd.DataFrame((address, percent, value))
#
#     df = df.T
#
#     df.columns = ['address', 'percent', 'value']
#
#     print(df)
#
#     driver = webdriver.Chrome('C:\\Program Files\\chromedriver_win32\\chromedriver.exe', options=chrome_options)
#     driver.set_window_size(1440, 900)
#     start_url = 'https://bscscan.com/address/0x8e8125f871eb5ba9d55361365f5391ab437f9acc'
#     driver.get(start_url)
#
#     sleep(3)
#
#     element = driver.find_element_by_id("availableBalanceDropdown")
#
#     element.click()
#
#     html = driver.page_source
#
#     driver.close()
#
#     soup = BeautifulSoup(html, 'html5lib')
#
#     coin_list = soup.find_all('li', class_="list-custom list-custom-BEP-20")
#
#     for item in coin_list:
#         print(item.text)
#         for a in item.find_all('a', href=True):
#             print("Found the URL:", a['href'])
#
#
# if __name__ == "__main__":
#     """Main check"""
#     main()


class Coin:
    """coin"""

    def __init__(self, parent, address, name=None, symbol=None):
        self.parent = parent
        """c"""

        self.name = name
        """c"""

        self.symbol = symbol
        """c"""

        self.address = address
        """c"""

        self.url = f'{self.parent.base_url}/token/{self.address}'
        """c"""

        self.price = []
        """c"""

        self.top_holders = []
        """c"""


class Holder:
    """c"""

    def __init__(self, parent, address, name=None):
        self.parent = parent
        """c"""

        self.address = address
        """h"""

        self.coins = []
        """h"""

        self.balance = []
        """h"""

        self.url = f'{self.parent.base_url}/address/{self.address}'
        """c"""

        # def run_queue_coins(self, num):
        #     """c"""
        #     if num >= len(self.queue_coins):
        #         self.get_top_coins(self.queue_coins)
        #     else:
        #         self.get_top_coins(self.queue_coins[:num])
        #
        # def run_queue_holders(self, num):
        #     """c"""
        #     if num >= len(self.queue_holders):
        #         self.get_top_coins(self.queue_holders)
        #     else:
        #         self.get_top_coins(self.queue_holders[:num])



        # df = pd.DataFrame((address, percent, value))
        #
        # df = df.T
        #
        # df.columns = ['address', 'percent', 'value']
        #
        # print(df)



        address = []
        percent = []
        value = []