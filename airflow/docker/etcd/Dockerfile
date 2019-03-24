FROM frolvlad/alpine-glibc

WORKDIR /home

# install common tools
RUN set -ex \
        && apk add --no-cache \
            bash \
            curl \
            dumb-init \
            git

ENV PATH $PATH:/home/bin/
RUN set -ex \
        && mkdir -p /home/bin/ \
        && curl -o /home/bin/etcdtool -L https://github.com/mickep76/etcdtool/releases/download/3.2/etcdtool-3.2-201602171504.linux.x86_64

RUN set -ex \
        && curl -L https://github.com/coreos/etcd/releases/download/v2.3.7/etcd-v2.3.7-linux-amd64.tar.gz \
        | tar xzfv - --directory=/home/bin/ --strip-components=1

ADD . /home/
RUN set -ex \
        && chmod +x /home/entrypoint.sh \
        && chmod +rwx /home/bin/etcdtool

EXPOSE 2379 2380

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["./entrypoint.sh"]
