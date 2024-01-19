#!/bin/sh
flask db upgrade
flask run --port=5000 --reload --host=0.0.0.0