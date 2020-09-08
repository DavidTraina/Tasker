# Note: only the instructions RUN, COPY, ADD create layers.

# initialize build over base image 3-alpine.
# 3 refers to python 3 (can get more specific if you want)
# alpine is a very small linux distribution. We use this linux environment with python for the app
FROM python:3-alpine

# This directory is created in the container. all relative paths are now from this absolute path
WORKDIR /tasker-app

# Support dependency caching by copying dependencies and installing them before copying everything else.
# This way, if some file changes, but the dependencies (i.e. requirements.txt) don't, 
# we don't have to install them all again because this layer up will still be valid. 
# We are sperating these layers. if we copied everything here and anything changed, the build cache 
# or this whole layer would be invalidated.
COPY requirements.txt ./
# todo taken from stackoverflow to deal with psycopg2 stuff on alpine. not a clue what's going on here
RUN \ 
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

# unsure if this is necessary
EXPOSE 5000

# copy the rest of our files into the container's working directory
# host-dir container-dir
COPY . .

# container executes this command by default when we launch the built image.
# run tasker with python tasker.py
CMD ["python", "./src/tasker.py"]


