from interpreter.src.utils.game import Worldfrom interpreter.src.utils.game import World

# Краткое руководство в примерах


## Создание проекта
Зайдите в ваш предпочитаемый терминал, и следуйте инструкциям из README.md, для установки.<br/>
Пользовательский интерфейс очевиден и его усвоение остается упражнением читателю. <br/>
**Примечание**: <br/>
При сохранении проекта не забудьте указать "Шаблон игрока" в настройках сервера.

## Написание скриптов
```python
# @world.on_event('on_stop')
@world.on_event('on_start') # функция запустится при запуске сервера
def on_start(*args, **kwargs):
    self.send('Сервер перезапущен') # Object.send отправляет подключенному к объекту игроку текст

@self.on_event('on_spawn') # имеет смысл только для шаблонов, запуститься при создании объекта из шаблона
def on_spawn():
    world.do_get_object_by_identity(self.identity).get_script_by_name('Скрипт 1').some_script_function('args', kwarg='kwarg')
    world.get_object_by_name('объект') # имя объекта это его атрибут name, то есть оно может быть не определено
    self.schedule(on_start, 1, 'args', kwarg='kwargs')

@world.on_schedule(1)
def one_second_after_script_start():
    self.send('Объект создан или сервер запущен секунду назад')
    self.attribues['second_passed'] = True
    self.trigger('on_elapsed', 1)
    world.trigger('on_elapsed', 1)
    world.get_object_by_name('объект2').trigger('on_elapsed', 1)
    player_prefab = world.do_get_prefab_by_name('Шаблон игрока')
    world.root_object.adopt(player_prefab.instance())
    self.transfer_user_connection_to(player_prefab)
    self.die()

# @self.on_event('on_disconnect')
@self.on_event('on_connect')
def do_script_on_when_connected_to_user():
    pass

@self.on_message
def on_message(message):
    self.send(f'Получено: {message}')
```