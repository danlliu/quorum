#!/bin/bash

export FLASK_ENV=development
export FLASK_APP=quorum
export DATABASE_URL="postgresql:///quorum"
flask run --host 0.0.0.0 --port 8000
