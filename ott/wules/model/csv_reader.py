import os
import csv

from ott.wules.utils.logger import *


class Csv(object):
    csv_file = None
    reader = None
    file = None
    raw = []

    def __init__(self, uri="rules.csv"):
        log.info('CSV read')
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
        log.info("open rules " + self.csv_file)
        if 'http' in self.csv_file:
            log.warn('TODO read url for rules...')
            pass
        else:
            self.file = open(self.csv_file, 'r')
            self.reader = csv.DictReader(self.file)


    def close(self):
        '''
        '''
        if file is not None:
            self.file.close()
            self.file = None

    def read(self):
        self.raw = []
        self.open()
        for row in self.reader:
            self.raw.append(row)
        self.close()
        return self.raw


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
