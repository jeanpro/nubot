#!/bin/bash
/home/azureuser/.local/bin/pipenv run gunicorn -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0 main:app --daemon

