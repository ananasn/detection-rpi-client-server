# Распознавание голоса и жестов на Raspberry Pi

## Описание
### Программа распознавания голоса
Используется библиотека [vosk](https://alphacephei.com/vosk/).

В качестве модели используется готовая русская модель [vosk-model-small](https://alphacephei.com/vosk/models).\
Находится в `microphone/model`.
#### Сервер распознавания
Скрипт `asr_server_microphone.py` - вебсокет-сервер, распознает речь с микрофона и расслыет всем клиентам.\
Вебсокет-сервер находится в  `microphone/websocket-microphone`. \
Работает на адресе `0.0.0.0` и порту `2700`.\
Источник - [vosk-server](https://github.com/alphacep/vosk-server/). 
#### Связь с HTTP-сервером
Для связи с **django** (поскольку **django** не может быть websocket-клиентом) используется скрипт `vosk_midleware.py`.\
Лежит в `microphone/websocket-microphone/`.\
Подключается к серверу распознавания по адресу `ws://localhost:2700`. \
К **django** подключается по адресу `http://127.0.0.1:8080/voice_detect`.

Вместо **django** может выступать любой HTTP-сервер.

### Программа распознавания жестов
Находится в `gestures/webcam.py`

### Тестовый сервер
Находится в `server/server.py`

### Production сервер
Работает **nginx + daphne**, они уже настроены на Raspberry (см. репозиторий **patrik**)

## Запуск
### Работа с демонами systemd
* Запуск происходит автоматически с помощью демонов **systemd**.
* Конфигурации должны быть скопированы в папку `/etc/systemd/system/` из папки `conf/etc_sysyemd_system`.
* Имеется три демона **vosk**, **vosk_midleware** и **gesture**.
* В случае ошибки происходит перезапуск.
* Остановить демона `sudo systemctl stop vosk`.
* Запустить демона `sudo systemctl restart vosk`.
* Если меняли конфиг, то нужно сделать.
```
sudo systemctl daemon-reload
sudo systemctl restart vosk
```
* Активировать (т.е. поставить на автозапуск) `sudo systemctl enable vosk`.
* Логи можно смотреть несколькими способами:
  * `journalctl - u vosk`
  * `sudo systemctl status vosk`. Аналогично для остальных демонов.
  
### Ручной запуск
* Скрипты для ручного запуска `start-vosk.sh`, `start-vosk-midleware.sh` и `start-gestures.sh`.

## Требования к python и pip
Библиотека vosk предъявляет следующие требования:
* Python version: 3.5-3.9
* pip version: 20.3 and newer.

## Зависимости
```bash
python3 --version
pip3 --version
pip3 -v install vosk

pip3 install sounddevice
```
