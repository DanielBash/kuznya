"""
Приложение Кузня. Создание приложения prompt_toolkit.
"""
from pathlib import Path

# -- импорт модулей
# - глобальные модули
from prompt_toolkit.application import Application, get_app
from prompt_toolkit.clipboard.pyperclip import PyperclipClipboard
from prompt_toolkit.layout import Layout
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.widgets import MenuContainer, MenuItem, TextArea
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.python import PythonLexer
from settings import *
from easy_gui_prompt import EasyGUI

# - локальные модули
from keybindings import kb
from widgets import TabContainer, Tab, ServerContainer, ScriptsContainer, ScriptInspectorContainer, \
    ScriptCodeInspectorContainer, ObjectInspectorContainer, ExportContainer, WebClientCodeContainer
from widgets.launch import LaunchContainer
from widgets.objects import ObjectsContainer
from widgets.prefabs import PrefabsContainer


# -- создание виджета приложения
class KuznyaApp:
    def __init__(self):
        self.tab_container = None
        self.root_container = None

        self.construct()

        app_state.app = self
        self.launched = False

    def construct(self):
        self.tab_container = TabContainer(tabs=[])

        self.root_container = MenuContainer(
            body=self.tab_container,
            menu_items=[
                MenuItem(
                    "Вкладки",
                    children=[
                        MenuItem("Запуск", handler=self.do_launch_tab),
                        MenuItem("Экспорт", handler=self.do_export_tab),
                        MenuItem("Шаблоны", handler=self.do_prefabs_tab),
                        MenuItem("Скрипты", handler=self.do_scripts_tab),
                        MenuItem("Объекты", handler=self.do_objects_tab),
                        MenuItem("Сервер", handler=self.do_settings_tab),
                    ]
                )
            ],
        )

    # -- функции меню
    # - открытие вкладки мира
    def do_export_tab(self):
        self.tab_container.tabs.append(Tab(ExportContainer(), title='Экспорт'))
        self.focus_last_tab()

    def do_launch_tab(self):
        self.tab_container.tabs.append(Tab(LaunchContainer(), title='Запуск'))
        self.focus_last_tab()

    # - открытие вкладки шаблонов
    def do_prefabs_tab(self):
        self.tab_container.tabs.append(Tab(PrefabsContainer(), title='Шаблоны'))
        self.focus_last_tab()

    # - открытие вкладки скриптов
    def do_scripts_tab(self):
        self.tab_container.tabs.append(Tab(ScriptsContainer(), title='Скрипты'))
        self.focus_last_tab()

    # - открытие вкладки инспектора скрипта
    def do_script_inspector_tab(self, identity):
        script = app_state.world.do_get_script_by_identity(identity)
        self.tab_container.tabs.append(Tab(ScriptInspectorContainer(identity), title=f'Скрипт: {script.identity[:5]}'))
        self.focus_last_tab()

    # - открытие вкладки инспектора скрипта
    def do_script_code_inspector_tab(self, identity):
        script = app_state.world.do_get_script_by_identity(identity)
        self.tab_container.tabs.append(
            Tab(ScriptCodeInspectorContainer(identity), title=f'Код Скрипта: {script.identity[:5]}'))
        self.focus_last_tab()

    # - открытие вкладки списка объектов
    def do_objects_tab(self):
        self.tab_container.tabs.append(Tab(ObjectsContainer(), title='Объекты'))
        self.focus_last_tab()

    # - открытие вкладки редактора объекта
    def do_object_inspector_tab(self, object_identity, prefab=False):
        if prefab:
            self.tab_container.tabs.append(Tab(ObjectInspectorContainer(object_identity, prefab), title=f'Шаблон {object_identity[:5]}'))
        else:
            self.tab_container.tabs.append(Tab(ObjectInspectorContainer(object_identity, prefab), title=f'Объект {object_identity[:5]}'))
        self.focus_last_tab()

    def on_web_client_code(self):
        self.tab_container.tabs.append(Tab(WebClientCodeContainer(), title='Веб-клиент'))
        self.focus_last_tab()

    # - открытие вкладки настроек
    def do_settings_tab(self):
        self.tab_container.tabs.append(Tab(ServerContainer(), title='Сервер'))
        self.focus_last_tab()

    def focus_last_tab(self):
        self.tab_container.switch_tab(len(self.tab_container.tabs) - 1)

    def __pt_container__(self):
        return self.root_container


# -- создание экземпляра приложения
kuznya = KuznyaApp()
app = Application(
    layout=Layout(kuznya, focused_element=kuznya.tab_container),
    full_screen=FULLSCREEN,
    mouse_support=MOUSE_SUPPORT,
    key_bindings=kb,
    style=STYLE,
    clipboard=PyperclipClipboard(),
)
