import csv
import os.path
import logging
from db.dbutil import *
from datetime import datetime

BSE_DOWNLOAD_FOLDER = "C:\\Users\\abhis\\OneDrive\\Data\\MarketData\\BSE"


def read_and_load(input_file):
    input_path = os.path.join(BSE_DOWNLOAD_FOLDER, input_file)
    logging.info('Loading from file ' + input_file)

    with open(input_path, newline='') as csvfile:
        quote_reader = csv.DictReader(csvfile, delimiter=',')
        for row in quote_reader:
            pass



if __name__ == "__main__":
    read_and_load("EQ_ISINCODE_081216.CSV")