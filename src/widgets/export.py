"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление окна настроек.
"""
from pathlib import Path

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.completion import PathCompleter
from prompt_toolkit.filters import Condition
# -- импортирование модулей
# - глобальные
from prompt_toolkit.layout import HSplit, Dimension, WindowAlign, ConditionalContainer, BufferControl, Window, \
    FloatContainer, Float, CompletionsMenu
from prompt_toolkit.widgets import Frame, TextArea, Box, Button, Label

# - локальные
import settings


# -- объявление виджетов
# - вкладка запуска приложения
class ExportContainer:
    def __init__(self):
        self.save_button = Button(
            text='Сохранить',
            width=30,
            handler=self.on_save
        )
        self.save_as_button = Button(
            text='Сохранить как',
            width=30,
            handler=self.on_save_as
        )
        self.load_button = Button(
            text='Загрузить',
            width=30,
            handler=self.on_load
        )
        self.load_new_button = Button(
            text='Создать новый',
            width=30,
            handler=self.on_load_new
        )
        self.frame = Frame(
            HSplit([
                self.save_button,
                self.save_as_button,
                self.load_button,
                self.load_new_button
            ]),
            title='Экспорт приложения')

        self.filename_buffer = TextArea(
            multiline=False,
            completer=PathCompleter(),
            width=30
        )
        self.input_dialog = ConditionalContainer(
            content=Frame(
                HSplit([
                    Label(text="Введите имя файла:"),
                    self.filename_buffer,
                    HSplit([
                        Button(text='ОК', handler=self.confirm_filename),
                        Button(text='Отмена', handler=self.cancel_filename),
                    ])
                ]),
                title='Имя файла'
            ),
            filter=Condition(lambda: self.show_filename_dialog)
        )
        self.show_filename_dialog = False
        self.filename_dialog_purpose = 'save'

        self.container = Box(
            FloatContainer(
                content=self.frame,
                floats=[
                    Float(
                        content=self.input_dialog,
                        height=6
                    ),
                    Float(
                        xcursor=True,
                        ycursor=True,
                        content=CompletionsMenu(max_height=16, scroll_offset=1),
                    )
                ]
            ),
            height=Dimension()
        )

    def __pt_container__(self):
        return self.container

    def on_save(self):
        settings.app_state.world.save_filename(settings.app_state.world.filename)

    def on_save_as(self):
        self.filename_buffer.text = str(settings.app_state.world.filename)
        self.filename_dialog_purpose = 'save'
        self.show_filename_dialog = True

    def cancel_filename(self):
        self.show_filename_dialog = False

    def confirm_filename(self):
        if self.filename_dialog_purpose == 'save':
            try:
                settings.app_state.world.save_filename(Path(self.filename_buffer.text))
                settings.app_state.world.filename = Path(self.filename_buffer.text)
                self.show_filename_dialog = False
            except Exception as e:
                self.show_filename_dialog = False
        elif self.filename_dialog_purpose == 'load':
            try:
                settings.app_state.world.load_filename(Path(self.filename_buffer.text))
                self.show_filename_dialog = False
            except Exception as e:
                self.show_filename_dialog = False
                print(e)

    def on_load(self):
        self.filename_buffer.text = str(settings.app_state.world.filename)
        self.filename_dialog_purpose = 'load'
        self.show_filename_dialog = True

    def on_load_new(self):
        settings.app_state.world.load_new()
        self.filename_buffer.text = str(settings.app_state.world.filename)