import os

from ott.wules.utils.logger import *
from ott.wules.model.csv_reader import Csv

class Rule():
    def __init__(self, rule_csv, line_number):
        """ {
            RULE parmas:
              ''
              AGENCY,MODE,DOW,DOM,MOY,START_TIME,END_TIME,CONTENT_URL
            }
        """

        # step 1: initialize rule meta data
        self.csv_line_number = line_number
        self.rule_csv        = dict((k.lower().strip(), v.strip()) for k,v in rule_csv.iteritems()) #lowercase dict keys
        self.url             = None
        self.is_valid        = False
        self.content_url()

        # step 2: find rule elements
        self.agency          = self.get_param('agency')
        self.start_time      = self.get_param('start_time')
        if self.start_time is not None and self.start_time.find(' ') > 0:
            self.start_time = self.time.replace(' ', '')

        self.note = None
        if 'note' in rule_csv:
            self.note = self.get_param('note')


    def content_url(self):
        ''' find url or content url from rule
        '''
        url = self.get_param('content_url')
        if url is None:
            url = self.get_param('url')
        if url is not None:
            self.is_valid = True
            self.url = url

    def get_param(self, name, def_val=None):
        ret_val = def_val
        try:
            p = self.rule_csv[name]
            if p is not None and len(p) > 0:
                ret_val = p.strip()
        except:
            log.info("'{0}' was not found as an index in record {1}".format(name, self.rule_csv))

        return ret_val



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
