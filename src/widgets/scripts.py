"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление окна просмотра скриптов.
"""

# -- импортирование модулей
# - глобальные
from prompt_toolkit.layout import HSplit, Dimension, WindowAlign, ScrollablePane, VSplit, FormattedTextControl, Window
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.widgets import Frame, TextArea, Box, Button, Label
from prompt_toolkit.application.current import get_app

# - локальные
import settings


# -- объявление виджетов
# - список скриптов
class ScriptsContainer:
    def __init__(self):
        self.buttons = []
        self.new_script_button = None
        self.frame = None
        self.container = None

        self.refresh_ui()

    def refresh_ui(self):
        self.buttons = []

        for script in settings.app_state.world.scripts:
            self.buttons.append(
                VSplit(
                    [
                        Button(text=f'{script.name}', width=len(script.name) + 2, left_symbol='', right_symbol='',
                               handler=lambda identity=script.identity: self.on_edit_script(identity),
                               ),

                        Window(
                            FormattedTextControl(
                                text=[('class:tab-close', '[x]',
                                       lambda me, identity=script.identity: self.on_delete_script(me, identity))]
                            ), width=3)

                    ]

                ))

        self.new_script_button = Button(
            text='Новый скрипт',
            handler=self.on_new_script
        )

        if len(self.buttons) > 0:
            self.frame = Frame(
                ScrollablePane(
                    HSplit([
                        *self.buttons,
                        self.new_script_button,
                    ], style='class:tab-content'),
                    height=10,
                ), title='Скрипты', style='class:tab-content')
        else:
            self.frame = Frame(
                HSplit([
                    Label('В данном мире еще нет скриптов', align=WindowAlign.CENTER),
                    self.new_script_button,
                ]),
                title='Скрипты', style='class:tab-content')

        self.container = Box(self.frame, height=Dimension())

    def on_new_script(self):
        settings.app_state.world.do_new_script()
        self.refresh_ui()
        get_app().layout.focus(self.buttons[-1])

    def on_delete_script(self, mouse_event, identity):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            settings.app_state.world.do_delete_script(identity)
            self.refresh_ui()
            get_app().layout.focus(self.new_script_button)

    def on_edit_script(self, identity):
        settings.app_state.app.do_script_inspector_tab(identity)

    def on_update(self):
        self.refresh_ui()
        get_app().layout.focus(self.new_script_button)

    def __pt_container__(self):
        return self.container
