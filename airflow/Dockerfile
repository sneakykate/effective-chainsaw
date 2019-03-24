FROM alpine:3.7

# install certificates and ssl libraries
RUN set -ex \
        && apk add --no-cache \
        ca-certificates \
        libressl


# install python and pip 3
RUN set -ex \
        && apk add --no-cache \
            python3 \
        && ln -s /usr/bin/python3 /usr/bin/python \
        && ln -s /usr/bin/pip3 /usr/bin/pip


# install numpy and pandas
ENV NUMPY_VERSION 1.12.1
ENV PANDAS_VERSION 0.19.2

RUN set -ex \
        && apk add --no-cache \
            openblas \
            python3-dev \
            freetype-dev \
            make \
            g++ \
            gfortran \
            musl

# create numpy cfg file and install
RUN { \
              echo '[openblas]'; \
              echo 'libraries = openblas'; \
              echo 'library_dirs = /usr/lib'; \
              echo 'include_dirs = /usr/include'; \
              echo; \
      } > /root/.numpy-site.cfg
RUN set -ex \
        && ln -sv /usr/include/locale.h /usr/include/xlocale.h \
        && pip install --no-cache-dir Cython --install-option="--no-cython-compile" \
        && pip install --no-cache-dir numpy=="$NUMPY_VERSION" pandas=="$PANDAS_VERSION" \
        && python -c 'import numpy, pandas; print("NUMPY VERSION: ", numpy.__version__, "\nPANDAS VERSION: ", pandas.__version__)'


# install airflow
ENV AIRFLOW_COMPONENTS="celery,crypto,postgres,redis,s3,slack"
ENV AIRFLOW_GPL_UNIDECODE yes

RUN set -ex \
        && apk add --no-cache \
            bash \
            dumb-init \
            libffi \
            libffi-dev \
            libxml2 \
            libxml2-dev  \
            libxslt \
            libxslt-dev \
            linux-headers \
            postgresql-dev \
        && CFLAGS="-I/usr/include/libxml2" \
            pip install --no-cache-dir \
                apache-airflow["$AIRFLOW_COMPONENTS"]==1.9.0 \
                boto3 \
                celery[redis] \
                docker-py \
                python-etcd \
                Flask-OAuthlib

# install etcd
ENV PATH $PATH:/home/bin/
RUN set -ex \
        && apk add --no-cache curl \
        && mkdir -p /home/bin/ \
        && curl -L https://github.com/coreos/etcd/releases/download/v2.3.7/etcd-v2.3.7-linux-amd64.tar.gz \
        | tar xzfv - --directory=/home/bin/ --strip-components=1


EXPOSE 8080 5555 8793
VOLUME /airflow

COPY entrypoint.sh /

ENV \
  AIRFLOW__CORE__AIRFLOW_HOME=/airflow \
  AIRFLOW__CORE__DAGS_FOLDER=/airflow/dags \
  AIRFLOW__CORE__BASE_LOG_FOLDER=/airflow/logs \
  AIRFLOW__CORE__PLUGINS_FOLDER=/airflow/plugins \
  AIRFLOW__CORE__EXECUTOR=SequentialExecutor \
  AIRFLOW__CORE__SQL_ALCHEMY_CONN=sqlite:////airflow/airflow.db \
  AIRFLOW__CORE__LOAD_EXAMPLES=False

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/entrypoint.sh"]