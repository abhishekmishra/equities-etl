import csv
import os.path
import logging
from job import *
from db.dbutil import *

BSE_DOWNLOAD_FOLDER = "C:\\Users\\abhis\\OneDrive\\Data\\MarketData\\BSE"


def read_and_load(input_file):
    dtstr = input_file.replace('.CSV', '').split('_')[2]
    date_of_file = datetime.strptime(dtstr, '%d%m%y')
    input_path = os.path.join(BSE_DOWNLOAD_FOLDER, input_file)
    j = Job('BSE_BHAVCOPY_LOAD', input_path)
    j.start()
    logging.info('Loading from file ' + input_file)

    row_count = 0.0
    with open(input_path, newline='') as csvfile:
        quote_reader = csv.DictReader(csvfile, delimiter=',')
        for row in quote_reader:
            row_count += 1

    count = 0.0
    update_count = 1

    conn = get_conn()
    c = conn.cursor()

    with open(input_path, newline='') as csvfile:
        quote_reader = csv.DictReader(csvfile, delimiter=',')
        for row in quote_reader:
            if row['SC_TYPE'] == 'Q':
                count += 1
                if (count / row_count) > (update_count * 0.1):
                    conn.commit()
                    print('update at ' + str(count/row_count * 100))
                    j.update_progress(round(count/row_count * 100))
                    update_count += 1

                res = c.execute("INSERT INTO STOCK_QUOTE " +
                                "(NAME, ISIN_CODE, TRADING_DATE, OPEN, HIGH, LOW, CLOSE, LAST, PREVCLOSE, NO_TRADES, " +
                                "NO_OF_SHARES, NET_TURNOVER, TDCLOINDI, MARKET_STOCK_CODE, MARKET_ID, JOB_ID) " +
                                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                (row['SC_NAME'], row['ISIN_CODE'], date_of_file, row['OPEN'], row['HIGH'], row['LOW'],
                                 row['CLOSE'], row['LAST'], row['PREVCLOSE'], row['NO_TRADES'], row['NO_OF_SHRS'],
                                 row['NET_TURNOV'], row['TDCLOINDI'], row['SC_CODE'], 1, j.id))
    conn.commit()
    conn.close()
    j.finish('COMPLETED')


if __name__ == "__main__":
    # j.update_progress(25.0)
    # j.update_progress(75.0)
    # j.finish('COMPLETED')

    read_and_load("EQ_ISINCODE_081216.CSV")