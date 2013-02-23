''' RuleList contains the logic to load a set of rules from CSV
    @see: Rule() for more
'''

from threading import Thread
import datetime
import time
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
        self.raw_data = 'EMPTY RAW DATA'
        self.last_update = datetime.datetime.now()
        self.last_check = None
        self.refresh_rules_check()


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


    def refresh_rules_check(self, n_minutes=15):
        ''' will check for new rules every N minutes (via the 'update_rules()' method), and
            trigger reloading of those rules if we've exceeded the n_minute time slice
            @todo: might we thread the rule refresh if we're pulling rules via the web???
        '''
        ret_val = False

        n_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=n_minutes)
        if self.last_check is None or self.last_check < n_minutes_ago:
            self.last_check = datetime.datetime.now()
            thread = Thread(target=self.rules_update_check)
            thread.start()
            time.sleep(0.2)
            ret_val = True

        return ret_val


    def rules_update_check(self):
        ''' open/download CSV of rules, and compare it existing rules 
            @return: True indicating that new data was reloaded...
        import pdb
        #pdb.set_trace()
        '''
        ret_val = False

        # step 1: grab new CSV ruleset...
        new_data = self.read()
        self.last_check = datetime.datetime.now()
        log.debug('checking for new rule set')

        # step 2: ...and compare whether the data changed from the last load of the rules 
        if new_data and len(new_data) > 0 and new_data != self.raw_data:

            # step 3: if the data did change, update the rules...
            self._update_rules(new_data)
            ret_val = True

        return ret_val


    def _update_rules(self, raw_data):
        ''' update the rules
        '''
        self.last_update = datetime.datetime.now()
        self.raw_data = raw_data

        # create new rules object list
        self.rules = []
        for i, r in enumerate(raw_data):
            rule = Rule(r, i+2)        # i+2 is the line number in the .csv file, accounting for the header
            self.rules.append(rule)

