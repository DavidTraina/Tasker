# Tasker

Tasker is a to-do list web app made with Flask, Python and Docker.

## Installation
With [Docker](https://www.docker.com/products/docker-desktop) installed, clone this repo and build the image:
```bash
docker build -t tasker .
```

## Usage

At the root directory, spin up a container from the image you built
```bash
docker run -dp 5000:5000 tasker-image
```
and open http://127.0.0.1:5000/ in a web browser.

Now add, edit and delete tasks at will!