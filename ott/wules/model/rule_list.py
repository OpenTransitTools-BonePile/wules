'''
'''
from ott.wules.model.csv_reader import Csv
from ott.wules.model.rule import Rule

import logging
log = logging.getLogger(__file__)

class RuleList(Csv):

    def __init__(self, uri="rules.csv"):
        '''
        '''
        super(Csv,self).__init__()
        self.assign_uri(uri)
        self.rules = []
        self.update_rules()

    def update_rules(self):
        '''
        '''
        self.rules = []
        raw = self.read()
        for i, r in enumerate(raw):
            rule = Rule(r, i+2)      # i+2 is the line number in the .csv file, accounting for the header
            self.rules.append(rule)


    def find(self, **kwargs):
        ''' agency=None, mode=None, routes=None, date=None, time=None, max_hits=3
        '''
        max_hits = kwargs.get('max_hits', 3)

        # filter 1: 
        hits = self.rules
        for k,v in kwargs.iteritems():
            log.debug("%s = %s" % (k, v))
            if k == 'time':
                hits = self.filter_time(hits, v)
            elif k == 'date':
                hits = self.filter_date(hits, v)
            else:
                hits = self.filter(hits, k, v)

        # max filter
        # (note ... might do a rule priority sort here)
        ret_rules = []
        log.debug("num of hits {0}".format(len(hits)))
        for h in hits:
            if len(ret_rules) >= max_hits: 
                break
            ret_rules.append(h)

        return ret_rules


    def filter(cls, rules, key, value):
        '''
        '''
        hits = []
        for r in rules:
            if not r.is_valid: continue
            if r.has_value(key, value):
                hits.append(r)
        return hits


    def filter_date(cls, rules, date):
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
