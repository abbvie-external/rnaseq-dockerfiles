FROM ubuntu:noble-20240605

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

ARG version=4.6.0.0

RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
       openjdk-17-jre-headless \
       r-base \
       wget \
    && apt-get clean \
    && wget https://github.com/broadinstitute/gatk/releases/download/$version/gatk-$version.zip \
    && unzip gatk-$version.zip \
    && mv gatk-$version gatk-4 \
    && mv gatk-4 /usr/local \
    && mv /usr/local/gatk-4/gatk-package-$version-local.jar /usr/local/gatk-4/gatk-package-local.jar \
    && mv /usr/local/gatk-4/gatk-package-$version-spark.jar /usr/local/gatk-4/gatk-package-spark.jar \
    && rm gatk*.zip \
    && apt-get remove --purge -y \
       wget \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
