FROM ubuntu:20.04
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update \
    && apt-get install -y wget xz-utils \
    && rm -rf /var/lib/apt/lists/*
ARG CLASHVER=v1.10.0
RUN wget https://github.com/Dreamacro/clash/releases/download/$CLASHVER/clash-linux-amd64-$CLASHVER.gz \
    && gunzip clash-linux-amd64-$CLASHVER.gz \
    && mv clash-linux-amd64-$CLASHVER /usr/bin/clash \
    && chmod 774 /usr/bin/clash
ARG YACDVER=v0.3.4
RUN wget https://github.com/haishanh/yacd/releases/download/$YACDVER/yacd.tar.xz \
    && mkdir -p /default/clash/dashboard \
    && tar xvf yacd.tar.xz -C /default/clash/dashboard \
    && wget https://geolite.clash.dev/Country.mmdb -O /default/clash/Country.mmdb \
    && chmod -R a+r /default/clash
ENV CLASH_MIXED_PORT=7890
ENV CLASH_SOCKS_PORT=7891
ENV CLASH_HTTP_PORT=7892
ENV DASH_PORT=8080
EXPOSE $CLASH_MIXED_PORT $CLASH_SOCKS_PORT $CLASH_HTTP_PORT $DASH_PORT
VOLUME /etc/clash
COPY start.sh /start.sh
RUN chmod +x /start.sh
ENTRYPOINT [ "/start.sh" ]