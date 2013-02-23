''' RuleList contains the logic to load a set of rules from CSV
    @see: Rule() for more
'''
import logging
log = logging.getLogger(__file__)

from ott.wules.model.csv_reader import Csv
from ott.wules.model.rule import Rule

class RuleList(Csv):

    def __init__(self, uri="rules.csv"):
        '''
        '''
        super(Csv,self).__init__()
        self.assign_uri(uri)
        self.rules = []
        self.timed_refresh_check()


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
        log.info("num of hits {0}".format(len(hits)))
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
        ''' TODO
        '''
        hits = []
        hits = rules
        return hits


    def filter_time(self, rules, time):
        ''' TODO
        '''
        hits = []
        hits = rules
        return hits


    def update_data(self, raw_data):
        ''' update the rules ... overrides Csv.update_data() 
        '''
        super(RuleList, self).update_data(raw_data)

        # create new rules object list
        self.rules = []
        for i, r in enumerate(raw_data):
            rule = Rule(r, i+2)        # i+2 is the line number in the .csv file, accounting for the header
            self.rules.append(rule)

