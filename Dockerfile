FROM eclipse-mosquitto:2.0.7

# Switch to root for installation
USER root

# Install Python and dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash

# Install Python dependencies
RUN pip3 install colorama

# Set up the fuzzer
WORKDIR /app

# Copy project files
COPY . /app/

# Copy mosquitto configuration
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Create sync directory
RUN mkdir -p /app/fume_sync /app/crashes

# Override the base image's entrypoint to prevent auto-starting mosquitto
# The fuzzer will control mosquitto via START_COMMAND
RUN rm -f /docker-entrypoint.sh

# Copy our entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


ENTRYPOINT ["/entrypoint.sh"]