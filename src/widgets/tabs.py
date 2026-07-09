"""
Объявление виджетов вкладок
"""

# -- импортирование модулей
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import HSplit, Window, DynamicContainer, WindowAlign
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.application.current import get_app
from prompt_toolkit.widgets import Box


def message_container(text: str):
    return Box(Window(
        FormattedTextControl(text),
        style="fg:#00ff00 bold",
        align=WindowAlign.CENTER,
        height=1,
    ))


class TabContainer:
    def __init__(self, tabs, no_container_message_container=None):
        self.tabs = tabs
        self.active_tab = 0

        self.bar = Window(
            content=FormattedTextControl(
                text=self.get_tabs,
                focusable=True,
                key_bindings=self.get_kb(),
            ),
            height=1,
            style='class:tab-bar',
        )

        self.content_container = DynamicContainer(self.get_tab)

        self.container = HSplit([
            self.bar,
            self.content_container,
        ])

        if no_container_message_container is None:
            no_container_message_container = message_container("Не выбрана ни одна вкладка")
        self.no_container_message_container = no_container_message_container

    def get_tabs(self):
        result = []
        for i, tab in enumerate(self.tabs):
            if i == self.active_tab:
                tab_style = 'class:tab-active'
            else:
                tab_style = 'class:tab-inactive'

            def make_switch_handler(idx):
                def handler(mouse_event):
                    if mouse_event.event_type == MouseEventType.MOUSE_UP:
                        self.switch_tab(idx)

                return handler

            def make_close_handler(idx):
                def handler(mouse_event):
                    if mouse_event.event_type == MouseEventType.MOUSE_UP:
                        self.close_tab(idx)

                return handler

            result.append((
                tab_style,
                f' {tab.title} ',
                make_switch_handler(i)
            ))

            result.append((
                'class:tab-close',
                ' ✕ ',
                make_close_handler(i)
            ))

        if not self.tabs:
            result.append(('', ' Нет вкладок '))

        return result

    def get_tab(self):
        if len(self.tabs) > self.active_tab > -1:
            return self.tabs[self.active_tab]
        else:
            return self.no_container_message_container

    def get_kb(self):
        kb = KeyBindings()

        @kb.add('left')
        def left(event):
            if len(self.tabs) == 0:
                return
            tab = (self.active_tab - 1) % len(self.tabs)
            self.switch_tab(tab)

        @kb.add('right')
        def right(event):
            if len(self.tabs) == 0:
                return
            tab = (self.active_tab + 1) % len(self.tabs)
            self.switch_tab(tab)

        for i in range(1, 10):
            @kb.add(str(i))
            def number(event, idx=i - 1):
                if idx < len(self.tabs):
                    self.switch_tab(idx)

        return kb

    def switch_tab(self, tab_index):
        if 0 <= tab_index < len(self.tabs):
            self.active_tab = tab_index
            get_app().layout.focus(self.content_container)
            self.tabs[tab_index].on_update()
        else:
            self.active_tab = 0
            get_app().layout.focus(self.bar)

    def close_tab(self, tab_index):
        if 0 <= tab_index < len(self.tabs):
            del self.tabs[tab_index]

            if not self.tabs:
                self.active_tab = 0
            elif self.active_tab >= len(self.tabs):
                self.active_tab = len(self.tabs) - 1

            self.switch_tab(self.active_tab)

    def __pt_container__(self):
        return self.container


class Tab:
    def __init__(self, container, title):
        self.container = container
        self.title = title

    def on_update(self):
        if hasattr(self.container, 'on_update'):
            self.container.on_update()

    def __pt_container__(self):
        return self.container
