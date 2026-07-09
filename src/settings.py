"""
Скрипт настроек приложения. Тут объявляются константы. Не подлежат изменениям в рантайме.
В основном файн-тюнинг для разработчиков. Также содержит создание класса текущего состояния приложения
"""

# -- импортирование модулей
# - глобальные
from prompt_toolkit.styles import Style
# - локальные
from world import WorldFile

# -- константы
STYLE = Style([
    ('tab-bar', 'fg:#00cc00'),
    ('tab-active', 'fg:#00ff00 bg:#000000 bold'),
    ('tab-inactive', 'fg:#008800 bg:#000000'),
    ('tab-close', 'fg:#ff4444 bg:#000000 bold'),
    ('menu-bar', 'fg:#00ff00 bg:#000000'),
    ('menu-bar.selected-item', 'fg:#00ff00 bg:#002200 bold'),
    ('menu', 'fg:#00ff00 bg:#000000'),
    ('menu.border', 'fg:#005500 bg:#000000'),
    ('menu-item', 'fg:#00cc00 bg:#000000'),
    ('menu-item.selected', 'fg:#00ff00 bg:#003300 bold'),
    ('menu-item.disabled', 'fg:#004400 bg:#000000'),
    ('tab-content', 'fg:#aaffaa bg:#000000'),
    ('shadow', 'bg:#004400'),
    ('frame.border', 'bg:#000000 fg:#00ff00 bold'),
    ('frame.label', 'bg:#000000 fg:#00ff00 bold'),
    ('text-area', 'bg:#000000 fg:#00ff00'),
    ('button', 'bg:#000000 fg:#00ff00'),
    ('label', 'bg:#000000 fg:#00ff00'),
    ('dialog', 'bg:#000000'),
    ('dialog frame.label', 'fg:#00ff00 bg:#000000 bold'),
    ('dialog body', 'fg:#00cc00 bg:#000000'),
    ('dialog input', 'fg:#00ff00 bg:#000000'),
    ('dialog input cursor', 'bg:#00ff00 fg:#000000')
])
MOUSE_SUPPORT = True
FULLSCREEN = True


# -- состояние приложения
class AppState:
    def __init__(self):
        self.world = WorldFile()
        self.app = None

app_state = AppState()