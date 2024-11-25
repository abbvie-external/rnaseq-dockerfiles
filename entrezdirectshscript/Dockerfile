 FROM ubuntu:noble-20240605

COPY entrezdiret.sh /usr/local/bin

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \ 
       ca-certificates \
       curl \
       perl \
    && sh -c "$(curl -fsSL https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh)" \
    && mv /root/edirect/* /usr/local/bin/ \
    && apt-get clean \
    && apt autoremove --purge -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add labels to the Docker image
LABEL maintainer="Jifeng Qian <jifeng.qianl@example.com>"
LABEL description="This is a Docker image that includes a custom script to extract a refseq id from NCBI record"
LABEL version="v1.0.0"
