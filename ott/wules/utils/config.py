from ConfigParser import SafeConfigParser
import glob
import logging
log = logging.getLogger()



parser = None
def get_parser():
    ''' make the config parser
    '''
    global parser

    candidates = ['app.ini', 'project.ini', 'wules.ini']
    try:
        if parser is None:
            parser = SafeConfigParser()
            found = parser.read(candidates)
            logging.config.fileConfig(found)
    except:
        log.info("Couldn't find an acceptable ini file from {0}...".format(candidates))

    return parser


def get(id, section='wules', def_val=None):
    ''' get config value
    '''
    ret_val = def_val
    try:
        if get_parser():
            ret_val = get_parser().get('wules', id)
            if ret_val is None:
                ret_val = def_val
    except:
        log.info("Couldn't find '{0}' in config under section '{1}'".format(id, section))

    return ret_val


def get_int(id, section='wules', def_val=None):
    ''' get config value as int (or go with def_val)
    '''
    ret_val = def_val
    try:
        v = get(id, section, def_val)
        if v:
            ret_val = int(v)
    except:
        log.info("Couldn't find '{0}' in config under section '{1}'".format(id, section))

    return ret_val

