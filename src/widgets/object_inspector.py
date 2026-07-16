"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление вкладки просмотра св-в объекта.
"""

# -- импорт модулей
# - глобальные
from prompt_toolkit.layout import Window, FormattedTextControl, HSplit, Dimension, \
    WindowAlign, VSplit
from prompt_toolkit.layout.containers import FloatContainer, Float
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.widgets import Frame, Box, TextArea, Label, Button, RadioList
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.application import get_app
from prompt_toolkit.completion import WordCompleter
from pygments.lexers.python import PythonLexer

# - локальные
import settings


# -- вкладка дерева объектов
class ObjectInspectorContainer:
    def __init__(self, identity, prefab=False):
        self.object = settings.app_state.world.do_get_object_by_identity(identity)
        self.identity = identity
        self.prefab = prefab
        if self.prefab:
            self.object = settings.app_state.world.do_get_prefab_by_identity(identity)
        else:
            self.object = settings.app_state.world.do_get_object_by_identity(identity)

        self.script_area = TextArea(
            completer=WordCompleter([script.name for script in settings.app_state.world.scripts]),
            complete_while_typing=True,
            multiline=False,
            height=1,
        )
        self.button_add_script = Button(
            text='Добавить скрипт',
            width=30,
            handler=self.on_add_script
        )

        self.button_add_attribute = Button(
            text='Добавить/Изменить атрибут',
            width=30,
            handler=self.on_add_attribute
        )

        self.attribute_name_area = TextArea(
            completer=WordCompleter(
                ['name', 'state', 'type', 'hp', 'idx'] + [key for obj in settings.app_state.world.get_objects() for key
                                                          in obj.attributes.keys()]),
            complete_while_typing=True,
            multiline=False,
            height=1,
        )
        self.attribute_area = TextArea(
            completer=WordCompleter([script.name for script in settings.app_state.world.scripts] +
                                    [script.identity for script in settings.app_state.world.scripts] +
                                    [object.identity for object in settings.app_state.world.get_objects()]),
            complete_while_typing=True,
            multiline=True,
            height=5,
            line_numbers=True,
            lexer=PygmentsLexer(PythonLexer)
        )

        self.container = None
        self.on_update()

    def __pt_container__(self):
        return self.container

    def refresh_ui(self):
        scripts_ui = []

        if hasattr(self.object, 'scripts') and self.object.scripts:
            for script in self.object.scripts:
                scripts_ui.append(
                    VSplit([
                        Button(
                            text=f'{script.name}',
                            width=len(script.name) + 2,
                            left_symbol='', right_symbol='',
                            handler=lambda identity=script.identity: self.on_edit_script(identity)
                        ),
                        Window(
                            FormattedTextControl(
                                text=[('class:red-button', '[x]',
                                       lambda me, identity=script.identity: self.on_remove_script(me, identity))]
                            ), width=3
                        )
                    ], style="class:tab-content")
                )
        else:
            scripts_ui.append(Label('Нет прикрепленных скриптов', align=WindowAlign.CENTER))

        attributes_ui = []
        if hasattr(self.object, 'attributes') and self.object.attributes:
            for name in self.object.attributes.keys():
                attributes_ui.append(
                    VSplit([
                        Button(
                            text=f'{name}',
                            width=len(name) + 2,
                            left_symbol='', right_symbol='',
                            handler=lambda n=name: self.on_edit_attribute(n)
                        ),
                        Window(
                            FormattedTextControl(
                                text=[('class:red-button', '[x]',
                                       lambda me, n=name: self.on_remove_attribute(me, n))]
                            ), width=3
                        )
                    ], style="class:tab-content")
                )
        else:
            attributes_ui.append(Label('Нет атрибутов', align=WindowAlign.CENTER))

        self.frame = Frame(
            HSplit([
                Label(text=f'Объект {self.object.identity[:10]}...', align=WindowAlign.CENTER),

                Label(text='Скрипты:', align=WindowAlign.LEFT),
                *scripts_ui,
                self.script_area,
                self.button_add_script,

                Label(text='Атрибуты:', align=WindowAlign.LEFT),
                *attributes_ui,
                Label(text='Имя атрибута:', align=WindowAlign.LEFT),
                self.attribute_name_area,
                Label(text='Значение:', align=WindowAlign.LEFT),
                self.attribute_area,
                self.button_add_attribute,
            ]),
            title='Объект' if not self.prefab else 'Шаблон')

        self.container = FloatContainer(
            content=Box(self.frame, height=Dimension()),
            floats=[
                Float(
                    xcursor=True,
                    ycursor=True,
                    content=CompletionsMenu(max_height=16, scroll_offset=1),
                )
            ]
        )

        get_app().layout.focus(self.container)

    def on_add_script(self):
        script_names = [script.name for script in settings.app_state.world.scripts]
        if self.script_area.text in script_names:
            script_to_add = settings.app_state.world.scripts[script_names.index(self.script_area.text)]
            if script_to_add not in self.object.scripts:
                self.object.scripts.append(script_to_add)
                self.script_area.text = ''
                self.on_update()
                get_app().layout.focus(self.button_add_script)

    def on_remove_script(self, mouse_event: MouseEvent, identity: str):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            self.object.scripts = [s for s in self.object.scripts if s.identity != identity]
            self.on_update()
            get_app().layout.focus(self.button_add_script)

    def on_edit_script(self, identity: str):
        settings.app_state.app.do_script_inspector_tab(identity)

    def on_add_attribute(self):
        name = self.attribute_name_area.text.strip()
        if not name:
            return

        raw_value = self.attribute_area.text
        expected_types = [list, dict, int, str, type(None), bool, float]

        try:
            eval_value = eval(raw_value, {"__builtins__": __builtins__}, {})
        except Exception as e:
            return

        if type(eval_value) not in expected_types:
            return

        self.object.attributes[name] = eval_value

        self.attribute_name_area.text = ''
        self.attribute_area.text = ''
        self.on_update()

    def on_edit_attribute(self, name: str):
        val = self.object.attributes[name]
        self.attribute_name_area.text = name
        self.attribute_area.text = repr(val)

        get_app().layout.focus(self.attribute_name_area)

    def on_remove_attribute(self, mouse_event: MouseEvent, name: str):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            if name in self.object.attributes:
                del self.object.attributes[name]
            self.on_update()
            get_app().layout.focus(self.button_add_attribute)

    def on_update(self):
        self.script_area.completer = WordCompleter([script.name for script in settings.app_state.world.scripts])
        self.attribute_area.completer = WordCompleter([script.name for script in settings.app_state.world.scripts] +
                                                      [script.identity for script in settings.app_state.world.scripts] +
                                                      [object.identity for object in
                                                       settings.app_state.world.get_objects()])
        self.attribute_name_area.completer = WordCompleter(
            ['name', 'state', 'type', 'hp', 'idx'] + [key for obj in settings.app_state.world.get_objects() for key
                                                      in obj.attributes.keys()])
        self.refresh_ui()
