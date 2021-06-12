import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import sqlite3
from sqlite3 import Error

import time

"""
Database
"""

sql_lookup = {

    'meta': """CREATE TABLE IF NOT EXISTS meta (
                                    if integer PRIMARY KEY AUTOINCREMENT,
                                    iterations integer DEFAULT 0,
                                    holders_number integer DEFAULT 0,
                                    coins_number integer DEFAULT 0
    )""",

    'holders': """ CREATE TABLE IF NOT EXISTS holders (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    address text NOT NULL UNIQUE,
                                    refresh integer NOT NULL DEFAULT 1
                                ); """,

    'coins': """CREATE TABLE IF NOT EXISTS coins (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                address text NOT NULL UNIQUE,
                                name text,
                                symbol text,
                                refresh integer NOT NULL DEFAULT 1
                            );""",

    'data': f"""CREATE TABLE IF NOT EXISTS data (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                holder_id integer,
                                coin_id integer,
                                amount integer,
                                percent real,
                                timestamp integer DEFAULT 0,
                                FOREIGN KEY(holder_id) REFERENCES holders(id),
                                FOREIGN KEY(coin_id) REFERENCES coins(id)
                            );"""
}


class Database:
    """database"""

    def __init__(self, db_file):

        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
            """c"""
            self.cur = self.conn.cursor()
            """c"""
            self.conn.execute("PRAGMA foreign_keys = 1")
            """x"""
            self.database_check()
            """c"""
        except Error as e:
            print(e)

    def database_check(self):
        """Check if database is setup"""

        def table_check(cur, name, sql):
            """check table"""

            # get the count of tables with the name
            cur.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}' ''')

            # if the count is 1, then table exists
            if cur.fetchone()[0] == 1:
                print(f'Table <{name}> exists.')
            else:
                print(f'Table <{name}> does not exist.')

                self.create_table(name, sql)

        for k, v in sql_lookup.items():
            table_check(self.cur, k, v)

    def create_table(self, name, create_table_sql):
        """ create a table from the create_table_sql statement
        :param name: Name of table
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        print(f'Creating table <{name}>...')
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            print(f'Created table <{name}>')
        except Error as e:
            print(e)

    def add_data(self, table, data):
        """s"""

        cols_query = ' AND '.join([col + '=?' for col in data.keys()])
        cols = tuple(data.keys()) if len(data.keys()) > 1 else f'("{list(data.keys())[0]}")'
        vals = tuple(data.values()) if len(data.values()) > 1 else f'("{list(data.values())[0]}")'
        print(f'SELECT * FROM {table} WHERE ({cols_query})', vals)

        print(cols, vals)

        self.cur.execute(f'SELECT * FROM {table} WHERE ({cols_query})', tuple(data.values()))
        entry = self.cur.fetchone()

        if entry is None:
            print(f'INSERT INTO {table} {cols} VALUES {vals}')
            self.cur.execute(f'INSERT INTO {table} {cols} VALUES {vals}')
            print('New entry added')
            self.conn.commit()
        else:
            print('Entry found')

    def seed(self):
        """seed"""
        coin = {'address': '0x2a0f5257f4bfe6c75cd58a14a0e7c4651e2160de'}
        self.add_data('coins', coin)


class Crawler:
    """crawler class"""

    def __init__(self, db):

        self.db = db
        """database"""

        self.percent_threshold = 0.40
        """x"""

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome('C:\\Program Files\\chromedriver_win32\\chromedriver.exe',
                                       options=chrome_options)
        """c"""

        self.driver.set_window_size(1440, 900)
        """c"""

        self.wait_time = 1   # TODO call this rate_limit and make it dynamic
        """c"""

        self.base_url = 'https://bscscan.com'
        """c"""

        self.df = pd.DataFrame()
        """c"""

    def get_top_coins(self, holder_address):
        """Get the top coins"""

        self.driver.get(f'{self.base_url}/address/{holder_address}')

        time.sleep(self.wait_time)

        element = self.driver.find_element_by_id("availableBalanceDropdown")

        element.click()

        html = self.driver.page_source

        soup = BeautifulSoup(html, 'html5lib')

        coin_list = soup.find_all('li', class_="list-custom list-custom-BEP-20")

        for item in coin_list:
            print(item.text)
            for a in item.find_all('a', href=True):
                print("Found the URL:", a['href'])
                coin_address = a['href'].replace('/token/', '').split('?a=')[0]
                print(coin_address, '!!!!!!!!!!!')
                self.db.add_data('coins', {'address': coin_address})

    def get_top_holders(self, coin_address):
        """Get the top holders"""

        # get coin id
        print(coin_address)
        self.db.cur.execute(f'''SELECT id FROM coins WHERE (address="{coin_address}")''')
        coin_id = self.db.cur.fetchone()[0]
        print(coin_id)

        print(f'{self.base_url}/{coin_address}#balances')

        self.driver.get(f'{self.base_url}/token/{coin_address}#balances')

        time.sleep(self.wait_time)

        iframe = self.driver.find_element(By.ID, 'tokeholdersiframe')

        self.driver.switch_to.frame(iframe)

        html = self.driver.page_source

        soup = BeautifulSoup(html, 'html5lib')

        tbody = soup.find('tbody')

        tr_tags = tbody.find_all('tr')

        for tr in tr_tags:
            td_tags = tr.find_all('td')

            address = td_tags[1].text
            percent = td_tags[3].text
            percent = float(percent.replace('%', ''))

            # percentage threshold
            if int(percent) > self.percent_threshold:
                continue

            self.db.add_data('holders', {'address': address})

            # get holder id
            print(address, '00000000')
            self.db.cur.execute(f'''SELECT id FROM holders WHERE (address="{address}")''')
            holder_id = self.db.cur.fetchone()[0]
            print(holder_id)

            self.db.add_data('data', {'coin_id': coin_id,
                                      'holder_id': holder_id,
                                      'amount': 100,
                                      'percent': percent,
                                      'timestamp': time.time()})

            # address.append(td_tags[1].text)
            # percent.append(td_tags[3].text)
            # value.append(td_tags[4].text)
            # self.add_data('data')

    def run(self):
        """x"""

        # get next coin
        self.db.cur.execute(f'SELECT address FROM coins WHERE (refresh=1)')
        entry = self.db.cur.fetchall()
        if entry is not None:
            for each in entry:
                print('=', each)
                self.get_top_holders(each[0])
                self.db.cur.execute(f""" Update coins set refresh=0 where address='{each[0]}' """)
        else:
            print('No coins')

        # get next holder
        self.db.cur.execute(f'SELECT address FROM holders WHERE (refresh=1)')
        entry = self.db.cur.fetchall()
        if entry is not None:
            for each in entry:
                print(each)
                self.get_top_coins(each[0])
                self.db.cur.execute(f""" Update holders set refresh=0 where address='{each[0]}' """)
        else:
            print('No holders')

        self.db.conn.commit()

    def url_holder(self, address):
        """c"""
        return f'{self.base_url}/address/{address}'

    def url_coin(self, address):
        """c"""
        return f'{self.base_url}/token/{address}'


def main():
    """main"""

    database = Database("crypto_kings.db")

    # seed
    database.seed()

    crawler = Crawler(database)

    crawler.run()


if __name__ == "__main__":
    """Main check"""
    main()
