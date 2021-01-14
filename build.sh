#!/usr/bin/env bash

pip install -r requirements.txt --upgrade
protoc --python_out=. protobuf/*.proto
