"""
@file simpsave.py
@author WaterRun
@version 3.2
@date 2025-04-12
@description Source code of simpsave project
"""

import os
import importlib.util
import configparser
import re
import ast
import base64
from io import StringIO


def _path_parser(path: str | None) -> str:
    r"""
    Handle and convert paths
    :param path: Path to be processed
    :return: Processed path
    :raise ValueError: If the path is not a string or is invalid
    :raise ImportError: If using :ss: and not installed via pip
    """
    if path is None:
        path = '__ss__.ini'

    if not (isinstance(path, str) and path.endswith('.ini')):
        raise ValueError("Path must be a string and must be a .ini file")

    if path.startswith(':ss:'):
        spec = importlib.util.find_spec("simpsave")
        if spec is None:
            raise ImportError("When using the 'ss' directive, simpsave must be installed via pip")

        simpsave_path = os.path.join(spec.submodule_search_locations[0])
        relative_path = path[len(':ss:'):]
        return os.path.join(simpsave_path, relative_path)

    absolute_path = os.path.abspath(path)

    if not os.path.isfile(absolute_path) and not os.path.isdir(os.path.dirname(absolute_path)):
        raise ValueError(f"Invalid path in the system: {absolute_path}")

    return absolute_path


def _load_config(file: str) -> configparser.ConfigParser:
    r"""
    Load the configuration file
    :param file: Path to the configuration file
    :return: Loaded ConfigParser object
    :raise FileNotFoundError: If the file does not exist
    """
    config = configparser.ConfigParser(interpolation=None)
    if not os.path.isfile(file):
        raise FileNotFoundError(f'The specified .ini file does not exist: {file}')
    
    with open(file, 'rb') as f:
        content = f.read().decode('utf-8', errors='replace')
    
    config.read_file(StringIO(content))
    return config


def _encode_key(key: str) -> str:
    """
    Encode key to handle non-UTF8 characters
    :param key: Original key
    :return: Encoded key
    """
    return key.encode('unicode-escape').decode('utf-8').replace('\n', '\\n').replace('=', '\\=').replace(':', '\\:')


def _decode_key(encoded_key: str) -> str:
    """
    Decode key to restore original format
    :param encoded_key: Encoded key
    :return: Original key
    """
    return bytes(encoded_key.replace('\\n', '\n').replace('\\=', '=').replace('\\:', ':').encode('utf-8')).decode('unicode-escape')


def write(key: str, value: any, *, file: str | None = None) -> bool:
    r"""
    Write data to the specified .ini file. If the .ini file does not exist, it will be created.
    For lists or dictionaries, every element must also be a Python basic type.
    :param key: Key to write to
    :param value: Value to write
    :param file: Path to the .ini file
    :return: Whether the write was successful
    :raise TypeError: If the value or its elements are not basic types
    :raise FileNotFoundError: If the specified .ini file does not exist
    """

    def _validate_basic_type(value):
        """
        Helper function to validate if the value is a basic type.
        Recursively checks lists and dictionaries.
        """
        basic_types = (int, float, str, bool, bytes, complex, list, tuple, set, frozenset, dict, type(None))
        if isinstance(value, (list, tuple, set, frozenset)):
            for item in value:
                if not isinstance(item, basic_types):
                    raise TypeError(f"All elements in {type(value).__name__} must be Python basic types.")
                _validate_basic_type(item)
        elif isinstance(value, dict):
            for k, v in value.items():
                if not isinstance(k, basic_types) or not isinstance(v, basic_types):
                    raise TypeError("All keys and values in a dict must be Python basic types.")
                _validate_basic_type(v)
        elif not isinstance(value, basic_types):
            raise TypeError(f"Value must be a Python basic type, got {type(value).__name__} instead.")

    file = _path_parser(file)
    _validate_basic_type(value)

    value_type = type(value).__name__
    encoded_key = _encode_key(key)

    if not os.path.exists(file):
        with open(file, 'w', encoding='utf-8') as new_file:
            new_file.write("")

    config = configparser.ConfigParser(interpolation=None)
    
    if os.path.exists(file) and os.path.getsize(file) > 0:
        try:
            with open(file, 'rb') as f:
                content = f.read().decode('utf-8', errors='replace')
            config.read_file(StringIO(content))
        except Exception:
            pass

    try:
        if isinstance(value, bytes):
            escaped_value = base64.b64encode(value).decode('utf-8')
        else:
            escaped_value = str(value).encode('unicode-escape').decode('utf-8').replace('\n', '\\n').replace('=', '\\=').replace(':', '\\:')

        config[encoded_key] = {'value': str(escaped_value), 'type': value_type}
        
        with open(file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        return True
    except Exception:
        return False


def read(key: str, *, file: str | None = None) -> any:
    r"""
    Read data from the specified .ini file for a given key
    :param key: Key to read from
    :param file: Path to the .ini file
    :return: The value after conversion (type casted)
    :raise FileNotFoundError: If the specified .ini file does not exist
    :raise KeyError: If the key does not exist in the file
    :raise ValueError: If the key is illegal
    """
    file = _path_parser(file)
    config = _load_config(file)
    
    encoded_key = _encode_key(key)
    
    if key in config:
        section = key
    elif encoded_key in config:
        section = encoded_key
    else:
        raise KeyError(f'Key {key} does not exist in file {file}')
    
    value_str = bytes(
        config[section]['value'].replace('\\n', '\n').replace('\\=', '=').replace('\\:', ':').encode('utf-8')).decode(
        'unicode-escape')
    type_str = config[section]['type']

    try:
        if type_str == 'bytes':
            return base64.b64decode(value_str)
        return {
            'int': int,
            'float': float,
            'str': str,
            'bool': lambda x: x == 'True',
            'complex': complex,
            'list': ast.literal_eval,
            'tuple': ast.literal_eval,
            'set': ast.literal_eval,
            'frozenset': ast.literal_eval,
            'dict': ast.literal_eval,
            'NoneType': lambda _: None,
        }[type_str](value_str)
    except (KeyError, ValueError):
        raise ValueError(f'Unable to convert value {value_str} to type {type_str}')


def has(key: str, *, file: str | None = None) -> bool:
    r"""
    Check if the specified key exists in the given .ini file.
    :param key: Key to check
    :param file: Path to the .ini file
    :return: True if the key exists, False otherwise
    :raise FileNotFoundError: If the specified .ini file does not exist
    """
    file = _path_parser(file)
    config = _load_config(file)
    
    encoded_key = _encode_key(key)
    return key in config or encoded_key in config


def remove(key: str, *, file: str | None = None) -> bool:
    r"""
    Remove the specified key (entire section). Returns False if it doesn't exist
    :param key: Key to remove
    :param file: Path to the .ini file
    :return: Whether the removal was successful
    :raise FileNotFoundError: If the specified .ini file does not exist
    """
    file = _path_parser(file)
    config = _load_config(file)
    
    encoded_key = _encode_key(key)
    
    section_to_remove = None
    
    if key in config:
        section_to_remove = key
    elif encoded_key in config:
        section_to_remove = encoded_key
    
    if section_to_remove is None:
        return False
        
    config.remove_section(section_to_remove)
    
    with open(file, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    return True


def match(regex: str = "", *, file: str | None = None) -> dict[str, any]:
    r"""
    Return key-value pairs that match the regular expression from the .ini file in the format {'key':..,'value':..}
    :param regex: Regular expression string
    :param file: Path to the .ini file
    :return: Dictionary of matched results
    :raise FileNotFoundError: If the specified .ini file does not exist
    """
    file = _path_parser(file)
    config = _load_config(file)
    pattern = re.compile(regex)
    result = {}
    
    for section in config.sections():
        original_key = _decode_key(section)
            
        if pattern.match(original_key):
            result[original_key] = read(original_key, file=file)
            
    return result


def delete(*, file: str | None = None) -> bool:
    r"""
    Delete the entire .ini file. Returns False if it doesn't exist
    :param file: Path to the .ini file to delete
    :return: Whether the deletion was successful
    :raise IOError: If the delete failed
    """
    file = _path_parser(file)
    if not os.path.isfile(file):
        return False
    try:
        os.remove(file)
        return True
    except IOError:
        return False
    