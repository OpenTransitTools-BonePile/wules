import os
import csv
import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rules_file = "rules.csv"
    path = os.path.join(here, rules_file)
    log.info(here + " " + path)

    file = open(path, 'r')
    reader = csv.DictReader(file)
    fn = reader.fieldnames 
    for i in fn:
        print i

    for row in reader:
        print row;

if __name__ == '__main__':
    main()
