import simplejson as json

from ott.wules.model.rule_list import RuleList
from ott.wules.model.rule import Rule

m_rl = RuleList()

def find(**kwargs):
    ret_val = []

    rules = m_rl.find(kwargs)
    if rules:
        for r in rules:
            cnt = r.get_content_dict()
            ret_val.append(cnt)

    return ret_val


def find_rules(**kwargs):
    r = m_rl.find(kwargs)
    j = features_to_json(r[0])
    return j


def features_to_json(obj):
    ''' convert obj to json string
    '''
    json_string = json.dumps(obj, sort_keys=True)
    return json_string


def main():
    f = find(agency='TriMet')
    print f
    #for z in r.find(5, agency='TriMet', mode='RAIL', language='en', time='5:30pm'):
    #for z in r.find(
    #    print "RESULT: {0}".format(z.__dict__)


if __name__ == '__main__':
    main()
