#!/bin/bash

docker compose rm -sf && docker compose up --build -d

python3 app.py
