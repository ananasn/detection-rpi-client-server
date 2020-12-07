# Распознавание голоса и жестов на Raspberry Pi

## Описание
### Программа распознавание голоса 
Находится в `voices/microphone.py`

### Программа распознавания жестов
Находится в `gestures/webcam.py`

### Тестовый сервер
Находится в `server/server.py`

### Production сервер
Работает **nginx + daphne**, они уже настроены на Raspberry (см. репозиторий **patrik**)

## Конфигурация IP адреса и порта
Конфигурация происходит через файл `conf/config.json`.

## Запуск
### Работа с демонами systemd
* Запуск происходит автоматически с помощью демонов systemd
* Конфигурации должны быть скопированы в папку `/etc/systemd/system/` из папки `conf/etc_sysyemd_system`
* Имеется два демона **voice** и **gesture**
* В случае ошибки происходит перезапуск
* Остановить демона `sudo systemctl stop voice` или `sudo systemctl stop gesture`
* Запустить демона `sudo systemctl restart voice` или `sudo systemctl restart gesture`
* Если меняли конфиг, то нужно сделать 
```
sudo systemctl daemon-reload
sudo systemctl restart gesture
```
* Активировать, (т.е. поставит на автозапуск) `sudo systemctl enable gesture`

### Crontab
* Также присутствует скрипт `autostart.sh`, который создает задачи для crontab. **Сейчас не используется (теперь systemd)**

### Ручной запуск
* Скрипты для ручного запуска `./start-voice.sh`  `./start-gestures.sh` 
