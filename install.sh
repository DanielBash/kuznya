#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Пути установки
INSTALL_DIR="$HOME/.local/share/kuznya"
VENV_DIR="$INSTALL_DIR/.venv"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
REPO_URL="https://github.com/DanielBash/kuznya.git"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  Установка КУЗНЯ RPG Engine${NC}"
echo -e "${BLUE}================================${NC}\n"

# Проверка зависимостей
echo -e "${YELLOW}[1/7] Проверка системных зависимостей...${NC}"

command -v python3 >/dev/null 2>&1 || {
    echo -e "${RED}❌ Python3 не установлен. Установите python3${NC}"
    exit 1
}

command -v git >/dev/null 2>&1 || {
    echo -e "${RED}❌ Git не установлен. Установите git: sudo apt install git${NC}"
    exit 1
}

# Проверка наличия модуля venv
python3 -c "import venv" 2>/dev/null || {
    echo -e "${RED}❌ Модуль python3-venv не установлен. Установите: sudo apt install python3-venv${NC}"
    exit 1
}

echo -e "${GREEN}✓ Системные зависимости найдены${NC}"

# Создание директорий
echo -e "\n${YELLOW}[2/7] Создание директорий...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
echo -e "${GREEN}✓ Директории созданы${NC}"

# Клонирование репозитория
echo -e "\n${YELLOW}[3/7] Клонирование репозитория...${NC}"
if [ -d "$INSTALL_DIR/.git" ]; then
    echo -e "${YELLOW}⚠️  Репозиторий уже существует, обновляю...${NC}"
    cd "$INSTALL_DIR" && git pull origin main
else
    git clone "$REPO_URL" "$INSTALL_DIR"
fi
echo -e "${GREEN}✓ Репозиторий клонирован${NC}"

# Создание виртуального окружения
echo -e "\n${YELLOW}[4/7] Создание виртуального окружения Python...${NC}"
if [ -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠️  Виртуальное окружение уже существует, пересоздаю...${NC}"
    rm -rf "$VENV_DIR"
fi

cd "$INSTALL_DIR"
python3 -m venv "$VENV_DIR"
echo -e "${GREEN}✓ Виртуальное окружение создано${NC}"

# Активация venv и установка зависимостей
echo -e "\n${YELLOW}[5/7] Установка Python-зависимостей в venv...${NC}"
source "$VENV_DIR/bin/activate"

# Проверяем, что мы в venv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${GREEN}✓ Виртуальное окружение активировано: $VIRTUAL_ENV${NC}"

    # Обновляем pip внутри venv
    python3 -m pip install --upgrade pip --quiet

    # Устанавливаем зависимости
    if [ -f "$INSTALL_DIR/requirements.txt" ]; then
        python3 -m pip install -r "$INSTALL_DIR/requirements.txt"
        echo -e "${GREEN}✓ Зависимости установлены${NC}"
    else
        echo -e "${RED}❌ Файл requirements.txt не найден${NC}"
        deactivate
        exit 1
    fi
else
    echo -e "${RED}❌ Не удалось активировать виртуальное окружение${NC}"
    exit 1
fi

deactivate
echo -e "${GREEN}✓ Установка в venv завершена${NC}"

# Создание исполняемого скрипта в PATH
echo -e "\n${YELLOW}[6/7] Создание команды kuznya...${NC}"
cat > "$BIN_DIR/kuznya" << 'EOF'
#!/bin/bash

INSTALL_DIR="$HOME/.local/share/kuznya"
VENV_DIR="$INSTALL_DIR/.venv"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "❌ КУЗНЯ не установлена. Запустите скрипт установки."
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Виртуальное окружение не найдено. Переустановите КУЗНЮ."
    exit 1
fi

# Активация виртуального окружения и запуск
source "$VENV_DIR/bin/activate"
cd "$INSTALL_DIR/src"
python3 main.py "$@"
EOF

chmod +x "$BIN_DIR/kuznya"

# Проверка PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}⚠️  Добавляю $BIN_DIR в PATH...${NC}"

    # Определяем shell и добавляем PATH
    if [ -f "$HOME/.bashrc" ]; then
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.bashrc"
    fi
    if [ -f "$HOME/.zshrc" ]; then
        echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.zshrc"
    fi
    if [ -f "$HOME/.config/fish/config.fish" ]; then
        echo "set -gx PATH $BIN_DIR \$PATH" >> "$HOME/.config/fish/config.fish"
    fi

    export PATH="$BIN_DIR:$PATH"
    echo -e "${YELLOW}⚠️  Перезапустите терминал или выполните: source ~/.bashrc${NC}"
fi

echo -e "${GREEN}✓ Команда kuznya создана${NC}"

# Создание .desktop файла
echo -e "\n${YELLOW}[7/7] Создание .desktop файла...${NC}"
cat > "$DESKTOP_DIR/kuznya.desktop" << EOF
[Desktop Entry]
Name=КУЗНЯ
Name[ru]=КУЗНЯ
Comment=Движок для создания текстовых RPG-мультиплееров
Comment[ru]=Движок для создания текстовых RPG-мультиплееров
Exec=$BIN_DIR/kuznya
Terminal=true
Type=Application
Categories=Development;Game;RolePlaying;
Icon=applications-games
Keywords=rpg;game;text;mud;multiplayer;development;
EOF

chmod +x "$DESKTOP_DIR/kuznya.desktop"
echo -e "${GREEN}✓ Desktop файл создан${NC}"

# Финал
echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}  ✅ Установка завершена!${NC}"
echo -e "${GREEN}================================${NC}"
echo -e "\n${BLUE}Теперь вы можете:${NC}"
echo -e "  • Запустить из терминала: ${YELLOW}kuznya${NC}"
echo -e "  • Найти в меню приложений: ${YELLOW}КУЗНЯ${NC}"
echo -e "\n${BLUE}Расположение:${NC} ${INSTALL_DIR}"
echo -e "${BLUE}Виртуальное окружение:${NC} ${VENV_DIR}"
echo -e "${BLUE}Для обновления выполните:${NC} bash <(curl -s https://raw.githubusercontent.com/DanielBash/kuznya/main/install.sh)"
echo ""