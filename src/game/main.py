import argparse
import os
import objects
import pathlib

# -- объявление функций
def valid_world_file(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"Файл мира '{path}' не существует")
    if not os.access(path, os.R_OK):
        raise argparse.ArgumentTypeError(f"Файл мира '{path}' недоступен для чтения")
    return path

def valid_port(value):
    port = int(value)
    if port < 1024 or port > 65535:
        raise argparse.ArgumentTypeError(
            f"Порт должен быть в диапазоне 1024-65535, получено: {port}")
    return port

# -- объявление переменных
parser = argparse.ArgumentParser(
    prog='Игровой сервер приложения КУЗНЯ.',
    description='Это часть движка КУЗНЯ, запускаемая для симуляции мира. Может быть запущена отдельно.',
    epilog='Исходный код: https://github.com/DanielBash/kuznya')

parser.add_argument('world_file', type=valid_world_file, help='Путь к файлу игрового мира')
parser.add_argument('rpyc_port', type=valid_port, help='Порт для RPyC-сервера')

# -- константы
ARGS = parser.parse_args()
WORLD = objects.World().load_filename(pathlib.Path(ARGS.world_file))

WORLD.run()