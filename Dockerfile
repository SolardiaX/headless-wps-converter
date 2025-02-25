FROM debian:bullseye-slim AS finally

LABEL maintainer="XtraVisions"

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=Asia/Shanghai

WORKDIR /root

RUN apt update && apt-get install -y curl bsdmainutils xdg-utils libxslt1.1 libglu1-mesa libqt5gui5 libqt5xml5 xvfb python3 python3-pip fonts-wqy-zenhei

RUN \
    export WPSOFFICE_VERSION=$(curl -sL "https://aur.archlinux.org/cgit/aur.git/plain/PKGBUILD?h=wps-office" | awk -F'=' '/^pkgver=/ {print $2}') && \
    curl -o \
        /tmp/wps.deb -L \
        "https://wdl1.pcfg.cache.wpscdn.com/wpsdl/wpsoffice/download/linux/${WPSOFFICE_VERSION##*.}/wps-office_${WPSOFFICE_VERSION}.XA_amd64.deb" && \
    dpkg -i /tmp/wps.deb

COPY fonts /tmp/fonts
RUN cd /tmp/fonts && bash install.sh

RUN python3 -m pip --no-cache-dir install pywpsrpc flask waitress loguru

RUN mkdir -p /root/.config/Kingsoft

COPY Office.conf /root/.config/Kingsoft/Office.conf
COPY api /root/api
COPY entrypoint.sh /root/entrypoint.sh

RUN chmod +x /root/entrypoint.sh

RUN apt-get clean -y && rm -rf /var/lib/apt/lists/* /var/tmp/* /tmp/*

EXPOSE 6100

ENTRYPOINT ["/root/entrypoint.sh"]
