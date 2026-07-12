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
    ('tab-bar', 'fg:#7A9A8A'),
    ('tab-active', 'fg:#A7C080 bg:#343F44 bold'),
    ('tab-inactive', 'fg:#5A7A6A bg:#232A2E'),
    ('tab-close', 'fg:#E67E80 bg:#232A2E bold'),
    ('menu-bar', 'fg:#D3C6AA bg:#232A2E'),
    ('menu-bar.selected-item', 'fg:#A7C080 bg:#343F44 bold'),
    ('menu', 'fg:#D3C6AA bg:#2B3339'),
    ('menu.border', 'fg:#4A5A4E bg:#2B3339'),
    ('menu-item', 'fg:#C2BAA4 bg:#2B3339'),
    ('menu-item.selected', 'fg:#A7C080 bg:#343F44 bold'),
    ('menu-item.disabled', 'fg:#5A6A5E bg:#2B3339'),
    ('tab-content', 'fg:#D3C6AA bg:#232A2E'),
    ('shadow', 'bg:#1C2124'),
    ('frame.border', 'bg:#232A2E fg:#4A5A4E bold'),
    ('frame.label', 'bg:#232A2E fg:#A7C080 bold'),
    ('text-area', 'fg:#D3C6AA bg:#232A2E'),
    ('button', 'fg:#A7C080 bg:#232A2E'),
    ('label', 'fg:#D3C6AA bg:#232A2E'),
    ('dialog', 'bg:#232A2E'),
    ('dialog frame.label', 'fg:#A7C080 bg:#232A2E bold'),
    ('dialog body', 'fg:#C2BAA4 bg:#232A2E'),
    ('dialog input', 'fg:#D3C6AA bg:#2B3339'),
    ('dialog input cursor', 'bg:#A7C080 fg:#232A2E'),
    ('button.focused', 'fg:#A7C080 bg:#343F44 bold'),
    ('green-button', 'fg:#A7C080 bg:#232A2E bold'),
    ('red-button', 'fg:#E67E80 bg:#232A2E bold'),
])
MOUSE_SUPPORT = True
FULLSCREEN = True
DEFAULT_CLIENT = """<!DOCTYPE html>
<html>
<head>
    <title>Веб-Клиент</title>
    <style>
        body { font-family: monospace; margin: 20px; }
        #log { 
            border: 1px solid #ccc; 
            padding: 10px; 
            height: 300px; 
            overflow-y: scroll;
            background: #f9f9f9;
        }
        input { width: 80%; padding: 5px; }
        button { padding: 5px 10px; }
    </style>
</head>
<body>
    <h1>Веб-Клиент</h1>
    <div id="log"></div>
    <input id="message" type="text" placeholder="Введите команду...">
    <button onclick="sendMessage()">Отправить</button>

    <script>
        const ws = new WebSocket('ws://localhost:1337');
        const log = document.getElementById('log');
        const input = document.getElementById('message');

        ws.onmessage = (event) => {
            log.innerHTML += `<div>> ${event.data}</div>`;
            log.scrollTop = log.scrollHeight;
        };

        ws.onopen = () => {
            log.innerHTML += '<div style="color: green">Подключение успешно.</div>';
        };

        ws.onclose = () => {
            log.innerHTML += '<div style="color: red">Отключено</div>';
        };

        function sendMessage() {
            if (input.value) {
                ws.send(input.value);
                log.innerHTML += `<div style="color: blue">< ${input.value}</div>`;
                input.value = '';
            }
        }

        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

# -- состояние приложения
class AppState:
    def __init__(self):
        self.world = WorldFile()
        self.app = None

app_state = AppState()