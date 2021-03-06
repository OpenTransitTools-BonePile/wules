import ott.wules.utils.config as config
from ott.wules.model.rule_list import RuleList
from ott.wules.model.rule import Rule

import logging
log = logging.getLogger()


m_rl = None
def rule_list():
    global m_rl
    if m_rl is None:
        log.info('Creating a new RulesList object')
        uri = config.get('csv_uri')
        if uri:
            m_rl = RuleList(uri)
        else:
            log.warn("ERROR: You don't have a csv_url defined in wules.ini pointing to a .csv file")
    else:
        min = config.get_int('rule_refresh_time')
        m_rl.timed_refresh_check(min)

    return m_rl


def all_rules(**kwargs):
    ''' get all the rules ... just content
    '''
    ret_val = []

    rules = rule_list().find(max_hits=30000)
    if rules:
        for r in rules:
            cnt = r.get_content_dict()
            ret_val.append(cnt)

    return ret_val


def all_rules_full(**kwargs):
    ''' get all the rules ... just content
    '''
    ret_val = []

    rules = rule_list().find(max_hits=30000)
    if rules:
        for r in rules:
            cnt = r.get_content_dict()
            ret_val.append(cnt)

    return ret_val


def find(**kwargs):
    ''' return 
    '''
    ret_val = []

    rules = rule_list().find(**kwargs)
    if rules:
        for r in rules:
            cnt = r.get_content_dict()
            ret_val.append(cnt)

    return ret_val


def find_rules(**kwargs):
    ret_val = rule_list().find(kwargs) | []
    return ret_val


def main():
    f = all_rules_full()
    # find(agency='TriMet',language='en', mode='RAIL')
    #for z in r.find(5, agency='TriMet', mode='RAIL', language='en', time='5:30pm'):
    #for z in r.find(
    #    print "RESULT: {0}".format(z.__dict__)
    print f
    print "NOTE: you might not see all the rules because of Thread() timing used to retrieve the rules."

if __name__ == '__main__':
    main()
