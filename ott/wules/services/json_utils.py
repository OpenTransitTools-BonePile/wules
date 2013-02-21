import simplejson as json


def json_message(msg="Something's wrong...sorry!"):
    return {'error':True, 'msg':msg}


def objects_to_json_string(obj):
    ''' convert obj to json string
    '''
    json_string = json.dumps(obj, sort_keys=True)
    return json_string

