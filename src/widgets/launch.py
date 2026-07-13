"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление окна настроек.
"""
import os
import signal
import subprocess
import sys
import threading
from pathlib import Path

# -- импортирование модулей
# - глобальные
from prompt_toolkit.layout import HSplit, Dimension, WindowAlign, FloatContainer, Float, CompletionsMenu
from prompt_toolkit.widgets import Frame, TextArea, Box, Button, Label

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
            width=50,
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
        self.stdout_thread = None

        self.on_update()

    def __pt_container__(self):
        return self.container

    def update_logs(self, pipe, prefix):
        for line in iter(pipe.readline, ''):
            self.logs_area.text = self.logs_area.text + line

    def on_launch(self):
        settings.app_state.app.launched = not settings.app_state.app.launched
        if settings.app_state.app.launched:
            settings.app_state.world.save_filename(settings.app_state.world.filename)
            process = subprocess.Popen(
                [
                    sys.executable, '-u',
                    str(Path(__file__).parent.parent.parent / 'interpreter/src/main.py'),
                    str(settings.app_state.world.filename.resolve())
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                start_new_session=True,
            )
            settings.app_state.app.world_process = process
            stdout_thread = threading.Thread(target=self.update_logs, args=(process.stdout, "OUT"))
            stdout_thread.daemon = True
            self.logs_area.text = ''

            self.stdout_thread = stdout_thread
            self.stdout_thread.start()
        else:
            proc = settings.app_state.app.world_process
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGINT)
            except ProcessLookupError:
                pass
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                proc.wait()

            if self.stdout_thread:
                self.stdout_thread.join(timeout=5)

            settings.app_state.world.load_filename(settings.app_state.world.filename)

        self.on_update()

    def on_update(self):
        if settings.app_state.app.launched:
            self.launch_button.text = 'Остановить мир и подгрузить изменения'
        else:
            self.launch_button.text = 'Сохранить и запустить мир'