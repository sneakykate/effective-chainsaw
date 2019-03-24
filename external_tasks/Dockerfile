FROM alpine:3.7

# install python and pip 3
RUN set -ex \
        && apk add --no-cache \
            postgresql-dev \
            gcc \
            python3-dev \
            musl-dev \
            py3-psycopg2 \
            postgresql \
            postgresql-contrib \
        && ln -s /usr/bin/python3-dev /usr/bin/python \
        && ln -s /usr/bin/pip3 /usr/bin/pip

# install pipenv
RUN set -ex \
        && pip install pipenv --upgrade

# install common tools
RUN set -ex \
        && apk add --no-cache \
            bash \
            curl \
            dumb-init \
            gzip

# -- Install Application into container:
RUN set -ex && mkdir /data

COPY Pipfile /data
COPY Pipfile.lock /data
COPY /tasks /data/tasks

WORKDIR /data

# -- Install dependencies:
RUN set -ex \
        && pipenv install --deploy --system


# make scripts executable
RUN set -ex \
        && chmod +x ./tasks/test.py
