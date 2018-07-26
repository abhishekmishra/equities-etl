import sys
from datetime import datetime
from datetime import date
from datetime import timedelta
import os.path
import urllib.request
import zipfile
import os

BHAVCOPY_EQUITIES_ISIN_URL = 'http://www.bseindia.com/download/BhavCopy/Equity/{}'
NUM_DAYS_TO_DOWNLOAD = 600


def get_equity_file(file_date, folder):
    if file_date.weekday() >= 5:
        print(file_date, 'is for a weekend, will not download.')
        return None, None

    fname = 'EQ_ISINCODE_{}.CSV'.format(file_date.strftime('%d%m%y'))
    zip_fname = 'EQ_ISINCODE_{}.ZIP'.format(file_date.strftime('%d%m%y'))
    file_url = BHAVCOPY_EQUITIES_ISIN_URL.format(zip_fname)
    file_location = folder + '/' + fname
    zip_file_location = folder + '/' + zip_fname

    print(file_url, '->', file_location)
    if os.path.isfile(file_location):
        print('File', file_location, 'already exists. Will not download!')
    else:
        try:
            # Download the file from `file_url` and save it locally under `file_location`:
            urllib.request.urlretrieve(file_url, zip_file_location)
            print('Downloaded file', file_url, 'at', zip_file_location)
            zip_ref = zipfile.ZipFile(zip_file_location, 'r')
            zip_ref.extractall(folder)
            zip_ref.close()
            os.remove(zip_file_location)
            print('Extracted Zip file, and then deleted it.')
        except urllib.error.HTTPError as e:
            print('Unable to download file', file_url, 'due to error -', e)

    return file_url, file_location


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Download folder is required (first argument).')
        exit()

    download_folder = sys.argv[1]
    print('Download folder ->', download_folder)

    numdays = NUM_DAYS_TO_DOWNLOAD
    base = datetime.today()
    date_list = [(base - timedelta(days=x)).date() for x in range(0, numdays)]
    file_url_list = [get_equity_file(d, download_folder) for d in date_list]
