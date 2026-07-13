"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление окна настроек.
"""

# -- импортирование модулей
# - глобальные
from prompt_toolkit.layout import HSplit, Dimension, WindowAlign, FloatContainer, Float, CompletionsMenu
from prompt_toolkit.widgets import Frame, TextArea, Box, Button, Label
from prompt_toolkit.completion import WordCompleter

# - локальные
import settings


# -- объявление виджетов
# - настройки
class LaunchContainer:
    def __init__(self):
        self.logs_area = TextArea(
            text='Нам нечего отобразить.',
            multiline=True,
            focusable=False,
        )
        self.launch_button = Button(
            text='Сохранить и запустить/Остановить сервер',
            width=30,
            handler=self.on_launch,
        )
        self.frame = Frame(
            HSplit([
                Label(text='Управление сервером', align=WindowAlign.CENTER),
                Frame(body=self.logs_area, title="Логи", height=10),
                self.launch_button,
            ]),
            title='Запуск сервера')
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

        self.on_update()

    def __pt_container__(self):
        return self.container

    def on_launch(self):
        pass

    def on_update(self):
        if settings.app_state.app.launched:
            self.launch_button.text = 'Остановить сервер'
        else:
            self.launch_button.text = 'Сохранить и запустить сервер'