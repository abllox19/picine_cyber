FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    iproute2 \
    net-tools \
    tcpdump \
    libpcap-dev \
    gcc \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir scapy

WORKDIR /app

CMD ["tail", "-f", "/dev/null"]