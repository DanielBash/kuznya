"""
Объявление всех сочетаний клавиш
"""

# -- импорт модулей
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous


# -- глобальные переменные
kb = KeyBindings()

# -- объявление функций
@kb.add("c-c", eager=True)
@kb.add("c-q", eager=True)
def do_quit_app(event):
    event.app.exit()

@kb.add('tab')
def _(event):
    focus_next(event)

@kb.add('s-tab')
def _(event):
    focus_previous(event)