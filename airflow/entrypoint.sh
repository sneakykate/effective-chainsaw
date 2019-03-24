#!/bin/bash
set -ex

export ETCDCTL_PEERS="$ETCD_PROTOCOL://$ETCD_HOST:$ETCD_PORT"

AIRFLOW_INIT_DB=${AIRFLOW_INIT_DB:=0}
if [ "$AIRFLOW_INIT_DB" -eq 1 ]; then
  airflow initdb
fi

DEVELOPMENT=${DEVELOPMENT:=0}
if [ "$DEVELOPMENT" -eq 1 ]; then
  airflow connections -a \
    --conn_id fakes3 \
    --conn_type aws \
    --conn_login 1234 \
    --conn_password 1234 \
    --conn_extra '{"host": "http://fakes3:4569"}'
fi

airflow webserver &
sleep 10
airflow scheduler
