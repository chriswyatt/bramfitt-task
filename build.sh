#!/usr/bin/env bash

PROTOBUF_OUT_DIR=protobuf
STATIC_DIR=static

pip install -r requirements.txt --upgrade

npm install

if [[ ! -d "$PROTOBUF_OUT_DIR" ]]; then
  mkdir "$PROTOBUF_OUT_DIR"
fi

protoc \
  --proto_path=protobuf_src \
  --python_out=protobuf \
  --js_out=import_style=commonjs,binary:"$STATIC_DIR" \
  prediction.proto

browserify -o "$STATIC_DIR"/{bundle.js,client.js,prediction_pb.js}
