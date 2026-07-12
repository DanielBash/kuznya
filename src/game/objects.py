"""
Объявление всех объектов
"""

import gzip
import json
# -- импорт библиотек
import pathlib
import secrets
from pathlib import Path


# -- объявление классов
class Object:
    def __init__(self, identity=None, scripts=None, children=None):
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
        self.children = [Object().load(child) for child in saved['children']]
        self.attributes = saved['attributes']
        return self

    def add_child(self):
        self.children.append(Object())

    def delete_child(self, identity):
        for child_indx in range(len(self.children)):
            if self.children[child_indx].identity == identity:
                del self.children[child_indx]
                return

    def get_name(self):
        if 'name' in self.attributes:
            try:
                return str(self.attributes['name'])
            except Exception as e:
                return self.identity
        else:
            return self.identity


class Prefab(Object):
    def __init__(self):
        super().__init__()


class Script:
    def __init__(self, code=None, name=None, identity=None):
        if identity is None:
            identity = secrets.token_urlsafe(16)
        if code is None:
            code = f'# Скрипт с идентификатором {identity} \n'
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

    def compile(self):
        pass


class World:
    def __init__(self):
        self._data = {}

        self.filename = None
        self.root_object = None
        self.prefabs = None
        self.scripts = None
        self.port_ssh = None
        self.port_telnet = None
        self.port_web = None
        self.connection_prefab_identity = None

        self.load_new()

    # - функции загрузки
    def load_filename(self, filename: Path):
        self.filename = filename

        with gzip.open(filename, 'rt', encoding='UTF-8') as file:
            self._data = json.load(file)

        self.root_object = Object().load(self._data['root'])
        self.prefabs = [Prefab().load(prefab) for prefab in self._data['prefabs']]
        self.scripts = [Script().load(script) for script in self._data['scripts']]
        self.port_ssh = self._data['server']['port_ssh']
        self.port_telnet = self._data['server']['port_telnet']
        self.port_web = self._data['server']['port_web']
        self.filename = filename
        self.connection_prefab_identity = self._data['connection_prefab_identity']

        return self

    def load_new(self):
        self.filename = pathlib.Path(__file__).parent.absolute() / 'world.wrld'
        self.root_object = Object()
        self.prefabs = []
        self.scripts = []
        self.port_ssh = 1337
        self.port_telnet = 1338
        self.port_web = 1339
        self.connection_prefab_identity = ''

        return self

    # - функции сохранения
    def save_filename(self, filename: Path):
        self._data = {
            'root': self.root_object.save(),
            'prefabs': [prefab.save() for prefab in self.prefabs],
            'scripts': [script.save() for script in self.scripts],
            'connection_prefab_identity': self.connection_prefab_identity,
            'server': {
                'port_ssh': self.port_ssh,
                'port_telnet': self.port_telnet,
                'port_web': self.port_web
            },
        }

        with gzip.open(filename, 'wt', encoding='UTF-8', compresslevel=9) as file:
            json.dump(self._data, file)

    # - быстрые макросы
    def do_new_script(self):
        self.scripts.append(Script())

    def do_delete_script(self, identity):
        for script_indx in range(len(self.scripts)):
            if self.scripts[script_indx].identity == identity:
                del self.scripts[script_indx]
                break

    def do_get_script_by_identity(self, identity):
        for script in self.scripts:
            if script.identity == identity:
                return script

    def do_get_prefab_by_identity(self, identity):
        for prefab in self.prefabs:
            found = self.find_in_children(prefab, identity)
            if found is not None:
                return found
        return None

    def do_get_object_by_identity(self, identity):
        return self.find_in_children(self.root_object, identity)

    def find_in_children(self, obj, target_identity):
        if obj.identity == target_identity:
            return obj
        for child in obj.children:
            found = self.find_in_children(child, target_identity)
            if found is not None:
                return found
        return None

    def get_objects_from_root(self, object):
        found = [object]
        for child in object.children:
            found += self.get_objects_from_root(child)
        return found

    def get_objects(self):
        return self.get_objects_from_root(self.root_object)

    def run(self):
        pass
