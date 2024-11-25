FROM ubuntu:16.04

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

RUN apt-get update \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       ca-certificates \
       wget \
    && wget http://security.ubuntu.com/ubuntu/pool/main/o/openjdk-7/openjdk-7-jre-headless_7u211-2.6.17-0ubuntu0.1_amd64.deb \
    && wget http://security.ubuntu.com/ubuntu/pool/main/t/tzdata/tzdata-java_2019a-0ubuntu0.14.04_all.deb \
    && wget http://security.ubuntu.com/ubuntu/pool/main/t/tzdata/tzdata_2019a-0ubuntu0.14.04_all.deb \
    && apt-get install .//tzdata_2019a-0ubuntu0.14.04_all.deb ./tzdata-java_2019a-0ubuntu0.14.04_all.deb ./openjdk-7-jre-headless_7u211-2.6.17-0ubuntu0.1_amd64.deb -y
