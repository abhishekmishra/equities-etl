import pandas as pd
import requests
from io import StringIO
from etl_task import *


class NiftyConstituents(ETLTask):
    def __init__(self, taskName):
        super().__init__(taskName)
        print('Running task : ' + self.taskName)
        self.headers = {
            'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101'
        }

    def before(self):
        print('do nothing')

    def after(self):
        print('downloaded NIFTY constituents')

    def execute(self):
        nifty100csv = requests.get('https://www.nseindia.com/content/indices/ind_nifty100list.csv',
                     params = None,
                     headers = self.headers)
        n100 = pd.read_csv(StringIO(nifty100csv.text))
        print(n100.head())


if __name__ == "__main__":
    nc = NiftyConstituents('yo')
    nc.execute()