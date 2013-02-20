import simplejson as json

def features_to_json(obj):
    ''' convert obj to json string
    '''
    json_string = geojson.dumps(obj, sort_keys=True)
    return json_string


def main():
    print 'empty'

if __name__ == '__main__':
    main()

