import os
import csv
import datetime
import time
from threading import Thread

import logging
log = logging.getLogger(__file__)


class Csv(object):
    csv_file = None
    reader = None
    file = None
    raw_data = []
    last_update = None
    last_check = None

    def __init__(self, uri="rules.csv"):
        log.info('Reading CSV {0}'.format(uri))
        self.assign_uri(uri)


    def assign_uri(self, uri):
        '''
        '''
        if '/' in uri or '\\' in uri:
            self.csv_file = uri
        else:
            here = os.path.dirname(os.path.abspath(__file__))
            self.csv_file = os.path.join(here, uri) 


    def open(self):
        '''
        '''
        log.debug("open rules {0}".format(self.csv_file))
        if 'http' in self.csv_file:
            log.warn('TODO read url for rules...')
            pass
        else:
            self.file = open(self.csv_file, 'rb')
            self.reader = csv.DictReader(self.file, delimiter='^')


    def close(self):
        '''
        '''
        if file is not None:
            self.file.close()
            self.file = None


    def read(self):
        ret_val = []
        self.open()
        for row in self.reader:
            ret_val.append(row)
        self.close()
        return ret_val


    def timed_refresh_check(self, n_minutes=15):
        ''' will check for new rules every N minutes (via the 'update_rules()' method), and
            trigger reloading of those rules if we've exceeded the n_minute time slice
            @todo: might we thread the rule refresh if we're pulling rules via the web???
        '''
        ret_val = False

        n_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=n_minutes)
        if self.last_check is None or self.last_check < n_minutes_ago:
            self.last_check = datetime.datetime.now()
            thread = Thread(target=self.new_data_check)
            thread.start()
            time.sleep(0.2)
            ret_val = True

        return ret_val


    def new_data_check(self):
        ''' open/download CSV of rules, and compare it existing rules 
            @return: True indicating that new data was reloaded...
        import pdb
        #pdb.set_trace()
        '''
        ret_val = False

        # step 1: grab new CSV data...
        new_data = self.read()
        self.last_check = datetime.datetime.now()
        log.debug('checking for new CSV data')

        # step 2: ...and compare whether the data changed from the last load of the rules 
        if new_data and len(new_data) > 0 and new_data != self.raw_data:

            # step 3: if the data did change, update the rules...
            self.update_data(new_data)
            ret_val = True

        return ret_val


    def update_data(self, new_data):
        ''' I'm probably overridden in sub classes
        '''
        self.raw_data = new_data
        self.last_update = datetime.datetime.now()


def main():
    c = Csv()
    c.open()
    fn = c.reader.fieldnames 
    for i in fn:
        print i

    for row in c.reader:
        print row;

    c.close()


if __name__ == '__main__':
    main()
