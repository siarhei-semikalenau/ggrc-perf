#!/usr/bin/env bash
export FLASK_APP=./http_test.py
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8888
export FLASK_RUN_RELOAD=True
#export FLASK_DEBUG=True
/Users/siarheis/venv/bin/flask run