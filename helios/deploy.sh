#!/bin/bash

tar --exclude="local_settings.py" -czf manishop.tar.gz ../manishop
scp manishop.tar.gz root@192.168.2.44:/var/www/phaethon/manishop.tar.gz

cap deploy

rm manishop.tar.gz
