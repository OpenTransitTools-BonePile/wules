'''
    The @class Rule() is ...
'''
import os
from ott.wules.utils.logger import *


class Rule():
    AGENCY       = 'agency'
    MODE         = 'mode'
    DOW          = 'dow'
    DOM          = 'dom'
    MOY          = 'moy'
    START_TIME   = 'start_time'
    END_TIME     = 'end_time'
    CONTENT_URL  = 'content_url'
    PRIORITY     = 'priority'
    NOTE         = 'note'

    def __init__(self, rule_csv, line_number):
        ''' {
            RULE parmas:
              ''
              AGENCY,MODE,DOW,DOM,MOY,START_TIME,END_TIME,CONTENT_URL,PRIORITY,NOTE
            }
        '''

        # step 1: initialize rule meta data
        self.csv_line_number = line_number
        self.rule_csv        = dict((k.lower().strip(), v.strip()) for k,v in rule_csv.iteritems()) #lowercase dict keys
        self.url             = None
        self.is_valid        = False
        self.content_url()

        # step 2: find rule elements
        self.agency          = self.get_param(Rule.AGENCY)
        self.start_time      = self.get_param(Rule.START_TIME)
        if self.start_time is not None and self.start_time.find(' ') > 0:
            self.start_time = self.time.replace(' ', '')

        self.note = None
        if Rule.NOTE in rule_csv:
            self.note = self.get_param(Rule.NOTE)


    def content_url(self):
        '''
           find url or content url from rule
        '''
        url = self.get_param(Rule.CONTENT_URL)
        if url is None:
            url = self.get_param('url')
        if url is not None:
            self.is_valid = True
            self.url = url


    def get_param(self, name, def_val=None):
        ''' 
        '''
        ret_val = def_val
        try:
            p = self.rule_csv[name]
            if p is not None and len(p) > 0:
                ret_val = p.strip()
        except:
            log.info("'{0}' was not found as an index in record {1}".format(name, self.rule_csv))

        return ret_val


    def has_value(self, key, value, regexp=''):
        ''' 
            return true if the key exists in this class,  
            and it's a string, and it's value matches
        '''
        ret_val = False
        a = getattr(self, key)
        log.info("{0} = getattr({1})".format(a, key))
        if (
            a is None 
            or type(a) is not str 
            or value in a
        ):
            ret_val = True
            log.info("key '{0}' has value '{1}' (and might matche via this regexp '{2}')".format(key, value, regexp))

        return ret_val


