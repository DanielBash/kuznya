"""
Приложение Кузня. Создание приложения prompt_toolkit.
"""

# -- импорт модулей
# - глобальные модули
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.widgets import MenuContainer, MenuItem, TextArea
from pygments.lexers.markup import MarkdownLexer
from pygments.lexers.python import PythonLexer
from settings import *
from easy_gui_prompt import EasyGUI

# - локальные модули
from keybindings import kb
from widgets import TabContainer, Tab, SettingsContainer


# -- создание виджета приложения
class KuznyaApp:
    def __init__(self):
        self.tab_container = None
        self.root_container = None

        self.construct()

    def construct(self):
        self.tab_container = TabContainer(tabs=[])

        self.root_container = MenuContainer(
            body=self.tab_container,
            menu_items=[
                MenuItem(
                    "Вкладки",
                    children=[
                        MenuItem("Мир", handler=self.do_project_tab),
                        MenuItem("Шаблоны", handler=self.do_prefabs_tab),
                        MenuItem("Скрипты", handler=self.do_scripts_tab),
                        MenuItem("Объекты", handler=self.do_objects_tab),
                        MenuItem("Настройки", handler=self.do_settings_tab),
                    ]
                )
            ],
        )

    # -- функции меню
    def do_project_tab(self):
        pass

    def do_prefabs_tab(self):
        pass

    def do_scripts_tab(self):
        pass

    def do_objects_tab(self):
        pass

    def do_settings_tab(self):
        self.tab_container.tabs.append(Tab(SettingsContainer(), title='Настройки'))

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
    min_redraw_interval=MIN_REDRAW_INTERVAL,
)