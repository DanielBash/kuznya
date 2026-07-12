"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление окна настроек.
"""
from prompt_toolkit.completion import WordCompleter
# -- импортирование модулей
# - глобальные
from prompt_toolkit.layout import HSplit, Dimension, WindowAlign, FloatContainer, Float, CompletionsMenu
from prompt_toolkit.widgets import Frame, TextArea, Box, Button, Label

# - локальные
import settings


# -- объявление виджетов
# - настройки
class ServerContainer:
    def __init__(self):
        self.telnet_area = TextArea(
            text=str(settings.app_state.world.port_telnet),
            multiline=False,
            focusable=True,
            focus_on_click=True,
        )
        self.ssh_area = TextArea(
            text=str(settings.app_state.world.port_ssh),
            multiline=False,
            focusable=True,
            focus_on_click=True,
        )
        self.web_area = TextArea(
            text=str(settings.app_state.world.port_web),
            multiline=False,
            focusable=True,
            focus_on_click=True,
        )
        self.connection_prefab_area = TextArea(
            text=str(settings.app_state.world.connection_prefab_identity),
            multiline=False,
            focusable=True,
            focus_on_click=True,
            completer=WordCompleter([prefab.identity for prefab in settings.app_state.world.prefabs]),
        )
        self.web_client_code_button = Button(
            text='Редактировать веб-клиент',
            width=30,
            handler=self.on_web_client_code
        )
        self.submit_button = Button(
            text='Подтвердить',
            width=30,
            handler=self.on_submit
        )
        self.frame = Frame(
            HSplit([
                Label(text='Настройки сервера', align=WindowAlign.CENTER),
                Frame(body=self.telnet_area, title="Порт telnet", height=3),
                Frame(body=self.ssh_area, title="Порт ssh", height=3),
                Frame(body=self.web_area, title="Порт web", height=3),
                Frame(body=self.connection_prefab_area, title="Шаблон игрока", height=3),
                self.web_client_code_button,
                self.submit_button,
            ]),
            title='Сервер')
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

    def __pt_container__(self):
        return self.container

    def on_submit(self):
        self.frame.title = 'Сервер'

        try:
            telnet_port = int(self.telnet_area.text)
            ssh_port = int(self.ssh_area.text)
            web_port = int(self.web_area.text)
            connection_prefab_identity = str(self.connection_prefab_area.text)

            if 0 > telnet_port or telnet_port > 65535: raise Exception
            if 0 > ssh_port or ssh_port > 65535: raise Exception
            if 0 > web_port or web_port > 65535: raise Exception

            settings.app_state.world.port_telnet = telnet_port
            settings.app_state.world.port_ssh = ssh_port
            settings.app_state.world.port_web = web_port
            settings.app_state.world.connection_prefab_identity = connection_prefab_identity

            self.frame.title = f'Сервер (Сохранено)'

        except Exception:
            self.frame.title = 'Сервер (Ошибка)'

    def on_update(self):
        self.telnet_area.text = str(settings.app_state.world.port_telnet)
        self.ssh_area.text = str(settings.app_state.world.port_ssh)
        self.web_area.text = str(settings.app_state.world.port_web)
        self.connection_prefab_area.text = str(settings.app_state.world.connection_prefab_identity)

    def on_web_client_code(self):
        settings.app_state.app.on_web_client_code()