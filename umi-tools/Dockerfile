FROM fedora:36

MAINTAINER Jeremiah H. Savage <jeremiah.savage@abbvie.com>

arg version=1.1.2

run dnf upgrade -y \
    && dnf install -y \
        bzip2 \
        bzip2-devel \
        gcc \
        make \
        python3 \
        python3-Cython \
        python3-devel \
        python3-pip \
        # python3-dateutil \
        # python3-future \
        # python3-numpy \
        # python3-pandas \
        # python3-pillow \
        # python3-pysam \
        # python3-matplotlib \
        # python3-regex \
        # python3-scipy \
        # python3-scipy \
        python3-wheel \
        wget \
        xz \
        xz-devel \
        zlib \
        zlib-devel \
    && dnf clean all \
    && pip install pyyaml \
    && wget https://github.com/cgatoxford/umi-tools/archive/$version.tar.gz \
    && tar xf $version.tar.gz \
    && cd UMI-tools-$version/ \
    && pip install -e . \
    && cd - \
    && rm -rf umi-tools* $version.tar.gz \
    && dnf remove -y \
        bzip2-devel \
        gcc \
        glibc-devel \
        kernel-headers \
        make \
        python3-devel \
        python3-pip \
        wget \
        xz-devel \
        zlib-devel \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
