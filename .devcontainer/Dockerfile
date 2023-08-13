# Use Fedora 38 as the base image
FROM fedora:38

# Install Java OpenJDK, python3-pip, and ansible
RUN dnf --assumeyes install git java-17-openjdk python3-pip && \
    export JAVA_HOME=/usr/lib/jvm/jre-17-openjdk && \
    pip3 install ansible ansible-rulebook ansible-runner ansible-lint

# Set the JAVA_HOME environment variable
ENV JAVA_HOME /usr/lib/jvm/jre-17-openjdk

RUN ansible-galaxy collection install ansible.eda cloin.eda