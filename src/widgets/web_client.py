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
from pygments.lexers.html import HtmlLexer

# - локальные
import settings


# -- объявление виджетов
# - редактор кода скрипта
class WebClientCodeContainer:
    def __init__(self):
        self.editor = TextArea(text=settings.app_state.world.web_client_code,
                               lexer=PygmentsLexer(HtmlLexer),
                               multiline=True,
                               focusable=True,
                               line_numbers=True
                               )
        self.container = HSplit([
            Window(
                FormattedTextControl(
                    [('class:green-button', 'Сохранить', self.on_save)]),
                height=1,
                style='class:tab-content',
            ),
            self.editor
        ])

    def __pt_container__(self):
        return self.container

    def on_update(self):
        self.container.text = settings.app_state.world.web_client_code

    def on_save(self, mouse_event):
        if mouse_event.event_type == MouseEventType.MOUSE_UP:
            settings.app_state.world.web_client_code = self.editor.text
