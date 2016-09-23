import ConfigParser
import binascii


def create_default_config():
    config = ConfigParser.SafeConfigParser(allow_no_value=True)

    config.add_section('General')
    config.set(
        'General', '# Null character must be a hex byte with no prefix eg. 00, a0, ff')
    config.set('General', 'null_char', binascii.hexlify('\x00'))
    config.set(
        'General', '# When true, all subdirectories are scanned by default')
    config.set('General', 'recursive', 'False')
    config.set(
        'General', '# Prepends all results with percent null')
    config.set('General', 'verbose', 'False')
    config.set('General', 'category_1_name', 'GOOD')
    config.set('General', 'category_2_name', 'DAMAGED')
    config.set('General', 'category_3_name', 'BAD')

    config.add_section('Categories')
    config.set('Categories', 'cat1', '5')
    config.set('Categories', 'cat2', '20')
    config.set('Categories', 'cat3', '85')

    config.add_section('txt')
    config.set('txt', 'cat1', '5')
    config.set('txt', 'cat2', '20')
    config.set('txt', 'cat3', '85')

    with open('null.cfg', 'wb') as configfile:
        config.write(configfile)


def read_config():

    config = ConfigParser.SafeConfigParser()

    options = config.read('null.cfg')

    # check that config file exists
    if len(options) <= 0:
        print('Config file not found, generating default config file.')
        create_default_config()

    config_dict = {}

    try:
        config_dict['verbose'] = config.getboolean('General', 'verbose')
    except ConfigParser.NoOptionError:
        print("NoOptionError: 'verbose' option missing, assuming False "
              "unless set by command line")
        config_dict['verbose'] = False

    try:
        config_dict['null_char'] = binascii.unhexlify(
            config.get('General', 'null_char'))
    except ConfigParser.NoOptionError:
        print("NoOptionError: 'null_char' option missing, assuming '\\x00' "
              "unless set by command line")
        config_dict['null_char'] = b'\x00'
    except TypeError:
        print("TypeError: 'null_char' option invalid, assuming '\\x00' "
              "unless set by command line")
        config_dict['null_char'] = b'\x00'

    try:
        config_dict['recursive'] = config.getboolean('General', 'recursive')
    except ConfigParser.NoOptionError:
        print("NoOptionError: 'recursive' option missing, assuming False "
              "unless set by command line")
        config_dict['recursive'] = False

    config_dict['category_1_name'] = config.get('General', 'category_1_name')
    config_dict['category_2_name'] = config.get('General', 'category_2_name')
    config_dict['category_3_name'] = config.get('General', 'category_3_name')

    for key in config._sections:
        if key == 'General':
            continue
        config_dict[key] = {}
        for subkey in config._sections[key]:
            if subkey == '__name__':
                continue
            try:
                config_dict[key][subkey] = int(config._sections[key][subkey])
            except ValueError:
                config_dict[key][subkey] = config._sections[key][subkey]

    return config_dict