# Bramfitt Technical Task

## Prerequisites

* Python
* Google Protobuf
* Node.js
* Node Package Manager (NPM)

## Setup development environment

* Create virtual Python environment, e.g., in BASH:
  ```shell
  python -m venv venv
  source venv/bin/activate
  ```
* Run ./build.sh

## Run server
* In the root of the project, run:
  ```shell
  flask run
  ```
* In a web browser, go to the URL: `http://127.0.0.1:5000/static/client.html`

## Troubleshooting
 - browserify command not found
   - Make sure that node_modules/.bin is included in your PATH environment variable
  
## Known limitations
 - Server URL is currently hardcoded into the client code
