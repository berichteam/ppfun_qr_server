#!/bin/bash

uwsgi=/usr/local/bin/uwsgi
home=/usr
app_dir=/Users/Superwen/pythonprojects/ppfun_qr_server


$uwsgi --uid root --gid root --chdir $app_dir --http :8011 -M  -p 1 -w server --callable app -t 60 --max-requests 5000 --vacuum --home $home --daemonize /tmp/ppfun_qr_server.log --pidfile /tmp/ppfun_qr_server.pid --touch-reload /tmp/ppfun_qr_server.touch


