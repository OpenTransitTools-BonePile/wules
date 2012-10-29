'''
'''
from ott.wules.utils.logger import *
from ott.wules.model.csv_reader import Csv
from ott.wules.model.rule import Rule

class RuleList(Csv):

    def __init__(self, uri="rules.csv"):
        super(Csv,self).__init__()
        self.assign_uri(uri)
        self.rules = []

    def update_rules(self):
        self.rules = []
        raw = self.read()
        for i, r in enumerate(raw):
            rule = Rule(r, i+2)      # i+2 is the line number in the .csv file, accounting for the header
            self.rules.append(rule)

    def find(self, agency=None, mode=None, routes=None, date=None, time=None, max_hits=3):
        '''
        '''
        ret_rules = []

        # filter 1: find agency rules...
        hits = self.rules
        hits = self.filter(hits, Rule.AGENCY, 'TriMet')
        ret_rules = hits

        return ret_rules


    def filter(self, rules, key, value):
        hits = []
        for r in rules:
            if r.has_value(key, value):
                hits.append(r)
        return hits


def main():
    r = RuleList()
    r.update_rules()
    for z in r.find():
        print z.__dict__


if __name__ == '__main__':
    main()
