#!/bin/bash
set -ex -o monitor

# start etcd in the background, bootstrap with values, and
# bring back to the foreground
etcd &
sleep 3
etcdtool import / bootstrap_etcd.json --yes
fg
