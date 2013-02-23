import logging
log = logging.getLogger(__file__)

import ott.wules.utils.config as config
from ott.wules.model.rule_list import RuleList
from ott.wules.model.rule import Rule

m_rl = None
def rule_list():
    global m_rl
    if m_rl is None:
        log.info('Creating a new RulesList object')
        url = config.get('url')
        if url:
            m_rl = RuleList(url)
        else:
            m_rl = RuleList()
    else:
        m_rl.timed_refresh_check()

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
    f = find(agency='TriMet',language='en', mode='RAIL')
    print f
    #for z in r.find(5, agency='TriMet', mode='RAIL', language='en', time='5:30pm'):
    #for z in r.find(
    #    print "RESULT: {0}".format(z.__dict__)

if __name__ == '__main__':
    main()
