FROM r-base:4.3.1

# Update the image
RUN apt-get update
RUN apt-get upgrade -y

# Create work directory
RUN mkdir /workdir
WORKDIR /workdir

# Install language server
RUN apt-get install libxml2-dev -y
RUN R -e 'install.packages("languageserver")'

# Install R packages
RUN R -e 'install.packages("readxl")'
RUN R -e 'install.packages("rhoR")'
RUN R -e 'install.packages("irr")'
