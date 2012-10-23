import os
import csv
import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

from ott.wules.model.csv_reader import Csv

class Rules(Csv):

    def __init__(self, uri="rules.csv"):
        super(Csv,self).__init__()
        self.assign_uri(uri)


def main():
    r = Rules()
    r.open()
    fn = r.reader.fieldnames 
    for i in fn:
        print i

    for row in r.reader:
        print row;

    r.close()


if __name__ == '__main__':
    main()
