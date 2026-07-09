"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление окна просмотра отдельного скрипта.
"""

# -- импортирование модулей
# - глобальные
from prompt_toolkit.layout import HSplit, Dimension, WindowAlign, ScrollablePane, VSplit, FormattedTextControl, Window
from prompt_toolkit.widgets import Frame, TextArea, Box, Button, Label

# - локальные
import settings


# -- объявление виджетов
# - редактор скрипта
class ScriptInspectorContainer:
    def __init__(self, identity):
        self.identity = identity
        self.script = settings.app_state.world.do_get_script_by_identity(self.identity)

        self.name_area = TextArea(
            text=str(self.script.name),
            multiline=False,
            focusable=True,
            focus_on_click=True,
        )
        self.edit_button = Button(
            text='Редактор',
            width=34,
            handler=self.on_edit
        )
        self.submit_button = Button(
            text='Подтвердить',
            width=34,
            handler=self.on_submit
        )
        self.frame = Frame(
            HSplit([
                Frame(body=self.name_area, title="Название скрипта", height=3),
                self.edit_button,
                self.submit_button,
            ]),
            title=f'{self.script.name[:24]}')
        self.container = Box(self.frame, height=Dimension())

    def __pt_container__(self):
        return self.container

    def on_submit(self):
        try:
            script_name = self.name_area.text

            if len(script_name) > 19 or len(script_name) < 3: raise Exception

            self.script.name = script_name

            self.frame.title = f'{self.script.name[:19]} (Изменено)'
        except Exception:
            self.frame.title = f'{self.script.name[:19]} (Ошибка)'
            self.on_update()

    def on_edit(self):
        settings.app_state.app.do_script_code_inspector_tab(self.script.identity)

    def on_update(self):
        self.name_area.text = str(self.script.name)
