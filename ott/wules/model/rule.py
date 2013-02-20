'''
    The @class Rule() is ...
'''
import os
from ott.wules.utils.logger import *
from ott.wules.utils.parse_datetime import *


class Rule():
    AGENCY       = 'agency'
    MODE         = 'mode'
    ROUTES       = 'route'
    DOW          = 'dow'
    DOM          = 'dom'
    MOY          = 'moy'
    START_TIME   = 'start_time'
    END_TIME     = 'end_time'
    PRIORITY     = 'priority'
    URL          = 'url'
    TITLE        = 'title'
    CONTENT      = 'contetnt'

    def __init__(self, rule_csv, line_number):
        ''' {
            RULE parmas:
              ''
            }
        '''

        # step 1: initialize rule meta data
        self.csv_line_number = line_number
        self.rule_csv        = self.process_csv(rule_csv)
        self.is_valid        = False

        if self.rule_csv is not None:
            # step 2: fix certain values (if they exist
            self.parse_time()
            self.parse_dates()

            # step 3: validate this Rule object
            self.check_rule()


    def process_csv(self, csv):
        '''
        '''
        ret_val = None
        try:
            #step 1: lowercase dict keys
            ret_val = dict((k.lower().strip(), v.strip()) for k,v in csv.iteritems())

            # step 2: assign the csv values to this class as new attributes
            log.info ("before {0}".format(self.__dict__))
            self.__dict__.update(ret_val)
            log.info ("after {0}".format(self.__dict__))

        except:
            log.info("EXCEPTION: process_csv: csv '{0}' lacks key/values".format(csv))

        return ret_val


    def parse_time(self):
        ''' 
        '''
        try:
            if self.start_time is not None:
                self.start_time = parse_time(self.start_time)
            if self.end_time is not None:
                self.end_time = parse_time(self.end_time)

            log.info("fix_time(): start = '{0}' end = {1}".format(self.start_time, self.end_time))
        except:
            log.info("EXCEPTION: fix_time() ...")


    def parse_dates(self):
        ''' various date input / parsing

            days_of_week bit-mask ... where dow[0] = Monday and dow[6] = Sunday, and True means show on those days
            valid specs for dow are M-F;M-S;M-U;M;T;W;TH;F;S;U 

            days_of_month is for a 31 day month, with true, false
        '''
        self.days_of_week=[False]*7
        if self.dow is not None:
            if 'M-'  in self.dow: self.days_of_week[0:5] = [True]*5
            if 'M'  in self.dow: self.days_of_week[0] = True
            if 'T'  in self.dow: self.days_of_week[1] = True
            if 'W'  in self.dow: self.days_of_week[2] = True
            if 'TH' in self.dow: self.days_of_week[3] = True
            if 'F'  in self.dow: self.days_of_week[4] = True
            if 'S'  in self.dow: self.days_of_week[5] = True
            if '-U' in self.dow: self.days_of_week[5] = True
            if 'U'  in self.dow: self.days_of_week[6] = True


        # we get a range of days of the month, and then 
        # (e.g., 22-7 means the last 9 days of the month, and the first week of the next month)
        self.days_of_month=[False]*32
        rngs=self.parse_range(self.dom, len(self.days_of_month))
        self.process_ranges(rngs, self.days_of_month, True)

        # we get a range of days of the month, and then 
        # (e.g., 22-7 means the last 9 days of the month, and the first week of the next month)
        self.months_of_year=[False]*13
        rngs=self.parse_range(self.moy, len(self.months_of_year))
        self.process_ranges(rngs, self.months_of_year, True)

        log.info("day of week {0}; days of month {1}; months of year {2}".format(self.days_of_week, self.days_of_month, self.months_of_year))


    # TODO: move to int_utility
    def process_ranges(self, ranges, value_list, value):
        ''' given a list of ranges, each of which are ranges of indexes into the value_list, assign the value
        '''
        try:
            max = len(value_list)
            for r in ranges:
                for i in r:
                    if i < max:
                        value_list[i] = value
        except:
            log.info("EXCEPTION: process_ranges({0},{1},{2})".format(ranges, value_list, value))


    # TODO: move to int_utility
    def parse_range(self, r, max):
        ''' @return: array of ranges (either one or two ranges), based on string inputs like: 15, 1-4, or 22-5
                     where 15 would be single value range [15], 1-4 would be [1,2,3,4] and 22-5 (given max 31)
                     would be two ranges ala [22,23,24...31] and [0,1,2,3,4,5]
            @see: processes_ranges()  
        '''
        ret1 = None
        ret2 = None
        try:
            i = r.split('-')
            t = max
            f = int(i[0])
            if f > max or f < 0:
                f = max
            if len(i) is 2:
                t = int(i[1])
                if t > max or t < 0:
                    t = max
                if f > t:
                    ret1 = range(f, max)
                    ret2 = range(0, t+1)
                else:
                    ret1 = range(f, t+1)
            else:
                ret1 = range(f, f+1)
        except:
            log.info("EXCEPTION: parse_range: {0}".format(r))

        log.info("range: {0} = {1} ... {2}".format(r, ret1, ret2))
        return ret1, ret2


    def check_rule(self):
        ''' check the rule for valid data (like url values), and then assign a validity flag to the Rule object
        '''
        # step 1: make sure we have a valid url parameter (flexible to be named content_url in .csv file)
        url = self.get_value(Rule.URL)
        if url is None:
            url = self.get_value('content_url')
            self.__dict__[Rule.URL] = url

        # step 2: if no url to our content, then our rule is invalid
        if url is not None:
            self.is_valid = True
        else:
            log.info("check_rules() self.__dict__ = {0}".format(self.__dict__))

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
            log.info("EXCEPTION: get_value: class doesn't have an element named '{0}'".format(key))

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
                or len(val)  is 0
                or search_value in val
            ):
                ret_val = True

            # log explicit rule matching 
            msg = "has_value: match is {ret_val} given key '{key}' has search value of '{search_value}', and Rule value of '{val}'"
            if regexp != None:
                msg = msg + ", considering regexp '{regexp}'"
            log.info(msg.format(**locals()))

        except:
            log.info("EXCEPTION: has_value: class doesn't have an element named '{0}'".format(key))
            ret_val = True # don't filter if the class lacks the element (only limit on value)

        return ret_val


    def within_rule_dates(self, date):
        '''
        '''
        explain=''
        fail=False

        # rule for day of week
        dow=True
        if self.dow != None:
             i = 1
             dow = self.days_of_week[i]
             if dow is False:
                 fail=True
                 explain += '\nDay of week failed for rule={0}, input dow={1} (for date {3}'.format(dow, i, date)
        
        moy=True
        #self.months_of_year

        dom=True
        #self.days_of_month

        if fail:
             log.info("check date")

        return ret_val


    def within_rule_times(self, time):
        '''
        '''
        ret_val = True
        return ret_val

    def get_attribute(self, key):
        return ret_val

    def get_content_dict(self, cnt_keys=None):
        ''' return dict of printable rule content
        '''
        ret_val = {}

        if cnt_keys == None:
            cnt_keys = [self.URL, self.TITLE, self.CONTENT]
        
        for k in cnt_keys:
            v = self.get_value(k)
            if v:
                ret_val[k] = v
        return ret_val

