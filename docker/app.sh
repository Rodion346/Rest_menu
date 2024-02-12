#!/bin/bash

sleep 10

alembic downgrade head
alembic upgrade head

uvicorn main:app --reload --host=0.0.0.0 --port=8000
