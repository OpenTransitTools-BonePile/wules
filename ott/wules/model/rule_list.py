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

def main():
    r = RuleList()
    r.update_rules()
    for z in r.rules:
        print z.__dict__


if __name__ == '__main__':
    main()
