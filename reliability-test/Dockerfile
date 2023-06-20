FROM almalinux:9

# Update the image
RUN dnf update -y

# Add EPEL repo
RUN dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm -y
RUN dnf config-manager --set-enabled crb
RUN dnf update -y

# Create work directory
RUN mkdir /workdir
WORKDIR /workdir

# Install R
RUN dnf install R -y
