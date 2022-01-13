# Распознавание голоса и жестов на Raspberry Pi

## Описание
### Программа распознавания голоса
Используется библиотека [vosk](https://alphacephei.com/vosk/).
В качестве модели используется готовая русская модель [vosk-model-small](https://alphacephei.com/vosk/models).
Находится в `microphone/model`.

Непосредственно распознавание с микрофона и расслыка всем подключенным клиентам выполняется вебсокет-сервером.
Вебсокет-сервер находится в  `microphone/websocket-microphone/asr_server_microphone.py`. 
Источник - [vosk-server](https://github.com/alphacep/vosk-server/). 
Работает на адресе `0.0.0.0` и порту `2700`.

Для связи с django (поскольку django не может быть websocket-клиентом) используется скрипт `vosk_midleware.py`. 
Лежит в `microphone/websocket-microphone/`.
Подключается к серверу распознавания по адресу `ws://localhost:2700`. 
К django подключается по адресу `http://127.0.0.1:8080/voice_detect`.

### Программа распознавания жестов
Находится в `gestures/webcam.py`

### Тестовый сервер
Находится в `server/server.py`

### Production сервер
Работает **nginx + daphne**, они уже настроены на Raspberry (см. репозиторий **patrik**)

## Запуск
### Работа с демонами systemd
* Запуск происходит автоматически с помощью демонов systemd
* Конфигурации должны быть скопированы в папку `/etc/systemd/system/` из папки `conf/etc_sysyemd_system`
* Имеется три демона **vosk**, **vosk_midleware** и **gesture**
* В случае ошибки происходит перезапуск
* Остановить демона `sudo systemctl stop vosk`, `sudo systemctl stop vosk_midleware` или `sudo systemctl stop gesture`
* Запустить демона `sudo systemctl restart vosk`, `sudo systemctl restart vosk_midleware` или `sudo systemctl restart gesture`
* Если меняли конфиг, то нужно сделать 
```
sudo systemctl daemon-reload
sudo systemctl restart gesture
```
* Активировать, (т.е. поставить на автозапуск) `sudo systemctl enable gesture`
* Логи можно смотреть несколькими способами:
  * `journalctl - u vosk`, `journalctl - u vosk_midleware`, `journalctl - u gesture`
  * `sudo systemctl status vosk`. Аналогично для остальных демонов.
  
### Ручной запуск
* Скрипты для ручного запуска `start-vosk.sh`, `start-vosk-midleware.sh` и `start-gestures.sh` 

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