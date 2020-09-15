#!/bin/bash

#  HTTPS setup checking
ERR=0
if [ ! -f "certificate.crt" ]; then
    echo "[-] Need SSL certifacate ! File Missing(./certificate.crt)"
    ERR=1
fi
if [ ! -f "private.key" ]; then
    echo "[-] Need SSL Private Key ! File Missing(./private.key)"
    ERR=1
fi

if [ $ERR -eq 1 ]; then
	exit 1
fi
echo "asdfasdf";

if [ $1 = "--temp" ]; then
	SERVER="temp:app"
else
	SERVER="main:app"
fi

mkdir -p ./log
gunicorn3 -w 6 -b 0.0.0.0:8443 $SERVER --certfile certificate.crt --keyfile private.key --access-logfile=log/access.log --error-logfile=log/error.log --capture-output --enable-stdio-inheritance &
echo "[+] Server (0.0.0.0:8443) Started !..."
