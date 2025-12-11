FROM eclipse-mosquitto:2.0.7

USER root

RUN apk add --no-cache python3 py3-pip bash && \
    pip3 install colorama && \
    addgroup -g 1000 fuzzer && \
    adduser -D -u 1000 -G fuzzer fuzzer && \
    rm -f /docker-entrypoint.sh

WORKDIR /app
COPY . /app/
COPY mosquitto.conf /mosquitto/config/mosquitto.conf
COPY entrypoint.sh /entrypoint.sh

RUN mkdir -p /app/fume_sync && \
    chown -R 1000:1000 /app && \
    chmod +x /entrypoint.sh

USER fuzzer
ENTRYPOINT ["/entrypoint.sh"]