# localdev
#
# Version: 0.0.1
FROM ubuntu:14.04

# install system deps
RUN apt-get -y -qq --force-yes update \
    && apt-get -y -qq --force-yes install \
        openssh-server \
        sudo \
        python \
        python-setuptools \
        build-essential \
        python-dev \
        libffi-dev \
        libssl-dev \
    && easy_install pip \
    && pip install pyopenssl ndg-httpsclient pyasn1

# configure user and ssh group
ENV SSH_GROUP ssh_access
RUN useradd -d /home/dev -u 1000 -m -s /bin/bash dev \
    && groupadd $SSH_GROUP \
    && usermod -a -G $SSH_GROUP dev \
    && usermod -a -G sudo dev \
    && passwd -d dev

# configure ssh access
RUN mkdir /var/run/sshd \
    && chown root:dev /usr/sbin/sshd \
    && echo AllowGroups $SSH_GROUP >> /etc/ssh/sshd_config \
    && sed -ri 's/^([a-z ]+)(pam_loginuid.so)/#\1\2/g' /etc/pam.d/sshd \
    && chmod 4750 /usr/sbin/sshd

# configure user ssh keys
COPY dev.pub /home/dev/.ssh/authorized_keys
RUN chmod 600 /home/dev/.ssh/authorized_keys \
    && chown --recursive dev:dev /home/dev/.ssh

# install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# configure container
ENV LANG en_US.utf8
ENV TERM xterm
EXPOSE 22
USER dev
VOLUME /opt/code
WORKDIR /opt/code
CMD ["/usr/sbin/sshd", "-D"]
