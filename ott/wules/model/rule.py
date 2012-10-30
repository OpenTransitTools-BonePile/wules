'''
    The @class Rule() is ...
'''
import os
from ott.wules.utils.logger import *


class Rule():
    AGENCY       = 'agency'
    MODE         = 'mode'
    ROUTES       = 'route'
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

        # step 2: assign the csv values to this class as new attributes
        self.__dict__.update(self.rule_csv)

        # step 3: fix certain values (if they exist
        self.fix_time()
        self.fix_dates()

        # step 4: validate this Rule object
        self.check_rule()


    def fix_time(self):
        ''' 
        '''
        pass


    def fix_dates(self):
        ''' 
        '''
        pass


    def check_rule(self):
        ''' check the rule for valid data (like content_url values), and then assign a validity flag to the Rule object
        '''
        # step 1: make sure we have a valid content_url parameter (flexible to be named url in .csv file)
        url = self.get_value(Rule.CONTENT_URL)
        if url is None:
            url = self.get_value('url')
            self.__dict__[Rule.CONTENT_URL] = url

        # step 2: if no url to our content, then our rule is invalid
        if url is not None:
            self.is_valid = True

        return self.is_valid


    def get_value(self, key):
        ''' return value of class element key
        '''
        ret_val = None
        try:
            #ret_val = getattr(self, key)
            ret_val = self.__dict__[key]
            log.info("{0} == getattr({1}) ?".format(ret_val, key))
        except:
            log.info("get_value: class doesn't have an element named '{0}'".format(key))

        return ret_val


    def has_value(self, key, search_value, regexp=None):
        ''' 
            return true if the key exists in this class,  
            and it's a string, and it's value matches
        '''
        ret_val = False
        val = None
        try:
            val = self.get_value(key)

            if (
                val is None
                or type(val) is not str 
                or search_value in val
            ):
                ret_val = True

            # log explicit rule matching 
            msg = "has_value: match is {ret_val} given key '{key}' has search value of '{search_value}', and Rule value of '{val}'"
            if regexp != None:
                msg = msg + ", considering regexp '{regexp}'"
            log.info(msg.format(**locals()))

        except:
            log.info("has_value: class doesn't have an element named '{0}'".format(key))
            ret_val = True # don't filter if the class lacks the element (only limit on value)


        return ret_val


    def get_attribute(self, key):
        return ret_val

