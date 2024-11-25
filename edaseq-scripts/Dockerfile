FROM sfo-docker-dtr.abbvienet.com/savagjh/edaseq

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

COPY edaseq-scripts/* /usr/local/bin/

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \ 
        python3
