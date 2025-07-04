#!/bin/sh

echo "Building read-sheet docker image"
docker build read-sheet -t read-sheet:main
kind load docker-image read-sheet:main

echo "Building compute docker image"
docker build compute -t compute:main
kind load docker-image compute:main

echo "Building send-mail docker image"
docker build send-mail -t send-mail:main
kind load docker-image send-mail:main
