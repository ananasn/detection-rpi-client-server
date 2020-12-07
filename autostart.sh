(crontab -l ; echo "@reboot /home/pi/detection-rpi-client-server/start-server.sh") | sort - | uniq - | crontab -
(crontab -l ; echo "@reboot /home/pi/detection-rpi-client-server/start-voice.sh") | sort - | uniq - | crontab -
(crontab -l ; echo "@reboot /home/pi/detection-rpi-client-server/start-gestures.sh") | sort - | uniq - | crontab -
