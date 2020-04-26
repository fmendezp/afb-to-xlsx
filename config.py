import configparser
from pathlib import Path
from os.path import join
from os.path import exists

def get_section(section):
    global _config
    if not section in _config.keys():
        _config[section] = {}
    return _config[section]

def get_with_default(section, entry, default):
    section_config = get_section(section)
    if not entry in section_config.keys():
        section_config[entry] = default
    return section_config[entry]

def default_separator():
    return ','

def default_delimiter():
    return '"'

def default_source_path():
    return '.'

def default_target_path():
    return '.'

def get_separator():
    return get_with_default('csvformat', 'separator', default_separator())

def get_delimiter():
    return get_with_default('csvformat', 'delimiter', default_delimiter())

def get_source_path():
    return get_with_default('paths', 'source', default_source_path())

def get_target_path():
    return get_with_default('paths', 'target', default_target_path())

def set_separator(val):
    get_section('csvformat')['separator'] = val

def set_delimiter(val):
    get_section('csvformat')['delimiter'] = val

def set_source_path(val):
    get_section('paths')['source'] = val

def set_target_path(val):
    get_section('paths')['target'] = val

def config_file_name():
    home = str(Path.home())
    return join(home, 'afb-converter.ini')

def default_config():
        global _config
        _config = configparser.ConfigParser()
        set_separator(default_separator())
        set_delimiter(default_delimiter())
        set_source_path(default_source_path())
        set_target_path(default_target_path())
        return _config

def load_config():
    if not exists(config_file_name()):
        write_default_config()
    global _config
    _config = configparser.ConfigParser()
    _config.read(config_file_name())
    source_path = get_source_path()
    if not exists(source_path):
        source_path = default_source_path()
    target_path = get_target_path()
    if not exists(target_path):
        target_path = default_target_path()

def write_default_config():
    with open(config_file_name(), 'w') as configfile:
        default_config().write(configfile)
        configfile.flush()

def save():
    with open(config_file_name(), 'w') as configfile:
        global _config
        _config.write(configfile)
        configfile.flush()

load_config()
