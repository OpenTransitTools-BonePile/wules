'''
'''
from ott.wules.utils.logger import *
from ott.wules.model.csv_reader import Csv
from ott.wules.model.rule import Rule

class RuleList(Csv):

    def __init__(self, uri="rules.csv"):
        '''
        '''
        super(Csv,self).__init__()
        self.assign_uri(uri)
        self.rules = []


    def update_rules(self):
        '''
        '''
        self.rules = []
        raw = self.read()
        for i, r in enumerate(raw):
            rule = Rule(r, i+2)      # i+2 is the line number in the .csv file, accounting for the header
            self.rules.append(rule)


    def find(self, max_hits=3, **kwargs):
        ''' agency=None, mode=None, routes=None, date=None, time=None, max_hits=3
        '''
        # filter 1: 
        hits = self.rules
        for k,v in kwargs.iteritems():
            log.info ("%s = %s" % (k, v))
            if k == 'time':
                hits = self.filter_time(hits, v)
            elif k == 'date':
                hits = self.filter_date(hits, v)
            else:
                hits = self.filter(hits, k, v)

        # max filter
        # (note ... might do a rule priority sort here)
        ret_rules = []
        log.info("num of hits {0}".format(len(hits)))
        for h in hits:
            if len(ret_rules) >= max_hits: 
                break
            ret_rules.append(h)

        return ret_rules


    def filter(self, rules, key, value):
        '''
        '''
        hits = []
        for r in rules:
            if not r.is_valid: continue
            if r.has_value(key, value):
                hits.append(r)
        return hits


    def filter_date(self, rules, date):
        '''
        '''
        hits = []
        hits = rules
        return hits


    def filter_time(self, rules, time):
        '''
        '''
        hits = []
        hits = rules
        return hits


def main():
    r = RuleList()
    r.update_rules()
    #for z in r.find(Rule.agency='TriMet', Rule.mode='RAIL'):
    for z in r.find(5, agency='TriMet', mode='RAIL', language='en', time='5:30pm'):
        print "RESULT: {0}".format(z.__dict__)


if __name__ == '__main__':
    main()
