"""
Объявление всех сочетаний клавиш
"""
from prompt_toolkit.application import get_app
# -- импорт модулей
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.selection import SelectionType

# -- глобальные переменные
kb = KeyBindings()

# -- объявление функций
@kb.add("c-q", eager=True)
def do_quit_app(event):
    event.app.exit()

@kb.add('tab')
def _(event):
    focus_next(event)

@kb.add('s-tab')
def _(event):
    focus_previous(event)

@kb.add('c-c')
def _(event):
    buffer = event.app.current_buffer
    if buffer.selection_state:
        data = buffer.copy_selection()          # Get the selected text
        get_app().clipboard.set_data(data)

@kb.add('c-v')
def _(event):
    event.app.current_buffer.paste_clipboard_data(
        event.app.clipboard.get_data()
    )

@kb.add('c-z')
def _(event):
    event.app.current_buffer.undo()

@kb.add('c-space')
def _(event):
    event.app.current_buffer.start_selection(SelectionType.CHARACTERS)

@kb.add('backspace')
def _(event):
    buffer = event.app.current_buffer
    if buffer.selection_state:
        buffer.cut_selection()
    else:
        buffer.delete_before_cursor()