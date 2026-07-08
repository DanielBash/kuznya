"""
Объявление всех объектов
"""

# -- импорт библиотек
import pathlib
import random
from pathlib import Path
import gzip
import json
import secrets


# -- объявление классов
class ObjectFile:
    def __init__(self, identity = None, scripts = None, children = None):
        if identity is None:
            identity = secrets.token_urlsafe(16)
        if scripts is None:
            scripts = []
        if children is None:
            children = []

        self.identity = identity
        self.scripts = scripts
        self.children = children
        self.attributes = {}

    def save(self):
        return {
            'identity': self.identity,
            'scripts': [script for script in self.scripts],
            'children': [child.save() for child in self.children],
            'attributes': self.attributes
        }

    def load(self, saved):
        self.identity = saved['identity']
        self.scripts = saved['scripts']
        self.children = [ObjectFile().load(child) for child in saved['children']]
        self.attributes = saved['attributes']
        return self


class PrefabFile(ObjectFile):
    def __init__(self):
        super().__init__()


class ScriptFile:
    def __init__(self, code = None, name = None, identity = None):
        if identity is None:
            identity = secrets.token_urlsafe(16)
        if code is None:
            code = f'# Скрипт с идентификатором {identity}'
        if name is None:
            name = f'Скрипт {identity[:4]}...'

        self.code = code
        self.name = name
        self.identity = identity

    def save(self):
        return {
            'code': self.code,
            'name': self.name,
            'identity': self.identity
        }

    def load(self, saved):
        self.code = saved['code']
        self.name = saved['name']
        self.identity = saved['identity']

        return self


class WorldFile:
    def __init__(self):
        self._data = {}

        self.filename = None
        self.root_object = None
        self.prefabs = None
        self.scripts = None
        self.port_ssh = None
        self.port_telnet = None
        self.port_web = None

        self.load_new()

    # - loading functions
    def load_filename(self, filename: Path):
        self.filename = filename

        with gzip.open(filename, 'r', encoding='UTF-8') as file:
            self._data = json.load(file)

        self.load_new()

        self.root_object = ObjectFile().load(self._data['root'])
        self.prefabs = [PrefabFile().load(prefab) for prefab in self._data['prefabs']]
        self.scripts = [ScriptFile().load(script) for script in self._data['scripts']]
        self.port_ssh = self._data['server']['port_ssh']
        self.port_telnet = self._data['server']['port_telnet']
        self.port_web = self._data['server']['port_web']

        return self

    def load_new(self):
        self.filename = pathlib.Path(__file__).parent.absolute()
        self.root_object = ObjectFile()
        self.prefabs = []
        self.scripts = []
        self.port_ssh = 1337
        self.port_telnet = 1338
        self.port_web = 1339

        return self

    # - saving functions
    def save_filename(self, filename: Path):
        self._data = {
            'root': self.root_object.save(),
            'prefabs': [prefab.save() for prefab in self.prefabs],
            'scripts': [script.save() for script in self.scripts],
            'server': {
                'port_ssh': self.port_ssh,
                'port_telnet': self.port_telnet,
                'port_web': self.port_web
            },
        }

        with gzip.open(filename, 'wt', encoding='UTF-8', compresslevel=9) as file:
            json.dump(self._data, file)

    # - quick macros
    def do_new_script(self):
        self.scripts.append(ScriptFile())

    def do_delete_script(self, identity):
        for script_indx in range(len(self.scripts)):
            if self.scripts[script_indx].identity == identity:
                del self.scripts[script_indx]
                break
