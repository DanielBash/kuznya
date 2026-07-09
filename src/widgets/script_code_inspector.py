"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление окна просмотра кода отдельного скрипта.
"""
from prompt_toolkit.layout import HSplit, Window, FormattedTextControl
# -- импортирование модулей
# - глобальные
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.widgets import TextArea
from pygments.lexers.python import PythonLexer

# - локальные
import settings


# -- объявление виджетов
# - редактор кода скрипта
class ScriptCodeInspectorContainer:
    def __init__(self, identity):
        self.identity = identity
        self.script = settings.app_state.world.do_get_script_by_identity(self.identity)

        self.editor = TextArea(text=self.script.code,
                               lexer=PygmentsLexer(PythonLexer),
                               multiline=True,
                               focusable=True,
                               line_numbers=True
                               )
        self.container = HSplit([
            Window(
                FormattedTextControl(
                    [('bg:#000000 fg:#00ff00', 'Сохранить', self.on_save)]),
                height=1,
                style='bg:#000000',
            ),
            self.editor
        ])

    def __pt_container__(self):
        return self.container

    def on_update(self):
        self.container.text = self.script.code

    def on_save(self, mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            self.script.code = self.editor.text
