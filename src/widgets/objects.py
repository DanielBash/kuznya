"""
Объявление специфичных для приложения виджетов и контейнеров.
Объявление вкладки просмотра дерева объектов.
"""

# -- импорт модулей
# - глобальные
from prompt_toolkit.layout import Window, ScrollablePane, FormattedTextControl, ScrollOffsets
from prompt_toolkit.widgets import Frame, Box
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings

# - локальные
import settings


# -- вкладка дерева объектов
class ObjectsContainer:
    def __init__(self):
        self.root_object = settings.app_state.world.root_object
        self._collapsed_ids = set()
        self.vertical_scroll = 0
        self.pane_height = 30

        self.kb = KeyBindings()
        self.kb.add('up')(self.move_up)
        self.kb.add('down')(self.move_down)
        self.control = FormattedTextControl(
            text=self.render,
            focusable=True,
            key_bindings=self.kb,
        )
        self.window = Window(content=self.control, wrap_lines=False, style='bg:#000000', )
        self.pane = ScrollablePane(self.window, keep_cursor_visible=False,
                                   keep_focused_window_visible=False, height=self.pane_height)
        self.frame = Frame(self.pane, title="Объекты", )
        self.container = Box(self.frame)

    def move_up(self, event):
        self.vertical_scroll -= 1
        if self.vertical_scroll < 0:
            self.vertical_scroll = 0
        self.control.text = self.render()

    def move_down(self, event):
        self.vertical_scroll += 1
        maximum = max(0, self.render_object(self.root_object, None, 0, []) - self.pane_height)
        if self.vertical_scroll > maximum:
            self.vertical_scroll = maximum

        self.control.text = self.render()

    def render(self):
        self.pane.vertical_scroll = self.vertical_scroll
        fragments = []
        if self.root_object:
            self.render_object(self.root_object, None, 0, fragments)
        return FormattedText(fragments)

    def render_object(self, object, parent_object, depth, fragments):
        rendered = 1
        object_id = object.identity
        children = object.children
        is_collapsed = object_id in self._collapsed_ids
        has_children = len(children) > 0
        name = object.get_name()

        indent = " " * depth

        if has_children:
            symbol = "[v] " if not is_collapsed else "[>] "
            fragments.append(
                ('bg:#000000 fg:#aaff00', indent + symbol, self._make_toggle_handler(object_id))
            )
        else:
            fragments.append(('bg:#000000 fg:#555555', indent + " - "))

        fragments.append(
            ('bg:#000000 fg:#ffffff', name, self._make_select_handler(object))
        )

        fragments.append(
            ('bg:#000000 fg:#ff0000', '[+]', self._make_add_child_handler(object))
        )

        if parent_object is not None:
            fragments.append(
                ('bg:#000000 fg:#ff0000', '[-]', self._make_remove_handler(object, parent_object))
            )

        fragments.append(('', '\n'))

        if has_children and not is_collapsed:
            for child in children:
                rendered += self.render_object(child, object, depth + 1, fragments)

        return rendered

    def _make_toggle_handler(self, object_id):
        def handler(mouse_event: MouseEvent):
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                if object_id in self._collapsed_ids:
                    self._collapsed_ids.remove(object_id)
                else:
                    self._collapsed_ids.add(object_id)
                self.control.text = self.render()

        return handler

    def _make_select_handler(self, object):
        def handler(mouse_event: MouseEvent):
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                self.control.text = self.render()
                settings.app_state.app.do_object_inspector_tab(object.identity)
        return handler

    def _make_add_child_handler(self, object):
        def handler(mouse_event: MouseEvent):
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                object.add_child()
                self.control.text = self.render()

        return handler

    def _make_remove_handler(self, object, parent_object):
        def handler(mouse_event: MouseEvent):
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                node_id = object.identity
                parent_object.delete_child(node_id)
                self.control.text = self.render()

        return handler

    def on_update(self):
        self.control.text = self.render()

    def __pt_container__(self):
        return self.container
