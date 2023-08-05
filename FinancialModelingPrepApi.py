from aiohttp import ClientSession
import asyncio
import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path
import os

class FinancialModelingPrepApi:
    def __init__(self, api_key, cache='./data.csv', ttl=300):
        self._api_key = api_key
        self._base_url = 'https://financialmodelingprep.com'
        self._params = {
            'apikey': self._api_key
        }
        self._cache = cache
        self._ttl = ttl
        self._first_call = True

        # attempt to create the cache file if it doesn't exist
        if not os.path.exists(self._cache):
            Path(self._cache).touch()

    async def get_stock_price(self, symbol):
        now = datetime.now(timezone.utc)

        # first try to get it from the csv file
        if (self._first_call):
            with open(self._cache, 'r') as cache_file:
                stock_reader = csv.reader(cache_file)
                for row in stock_reader:
                    if self.convert(row[3]) >= now - timedelta(seconds=self._ttl):
                        self._first_call = False
                        return row[1]

        # last data in cache is stale, hit api endpoint and write down the cache
        async with ClientSession() as session:
            async with session.get(self._base_url + f'/api/v3/quote-short/{symbol.upper()}', params=self._params) as resp:
                response = await resp.json()
                with open(self._cache, 'w') as cache_file:
                    stock_writer = csv.writer(cache_file)
                    response[0]['timestamp'] = now
                    stock_writer.writerow(response[0].values())
                    self._first_call = False
                return response[0]['price']
            
    def convert(self, date_time):
        format = '%Y-%m-%d %H:%M:%S.%f%z'
        datetime_str = datetime.strptime(date_time, format)
        return datetime_str