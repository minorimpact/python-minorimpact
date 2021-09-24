
import configparser
import os
import os.path
import re
import sys

def getConfig(config = None, interpolation = None, script_name = None, verbose = False):
    home = os.environ['HOME'] if 'HOME' in os.environ else ''
    config_basename = None
    config_filename = None

    if script_name is None:
        script_name = re.sub('\.py$', '', os.path.basename(sys.argv[0])) 

    if script_name is None:
        raise Exception("can't get script name")

    config_basename = script_name + '.conf'
    if script_name.upper() + '_CONF' in os.environ:
        config = os.environ[script_name.upper() + '_CONF']

    if (config is not None):
        if (re.match('/', config)): 
            config_filename = config
            config_basename = os.path.basename(config_filename)
        else:
            config_basename = config

    if (config_filename is None):
        for path in [home + '/.conf/' + script_name, home, '/etc']:
            if (verbose is True): print(f"checking {path}/ ... ", end='')
            test_filename = f'{path}/{config_basename}'
            if (os.path.exists(test_filename)):
                if (verbose is True): print("found")
                config_filename = test_filename
                break
            if (verbose is True): print("not found")

    if (config_filename is None):
        if (config_basename is not None):
            raise Exception(f"{config_basename} not found")
        raise Exception(f"config file not found")
    elif (config_filename is not None and os.path.exists(config_filename) is False):
        raise Exception(f"{config_filename} not found")

    if (interpolation == 'basic'): interpolation = configparser.BasicInterpolation()
    parser = configparser.ConfigParser(interpolation=interpolation)
    parser.read(config_filename)

    return parser