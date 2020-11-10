FROM python:latest as ddi-dev-python

# Install git

RUN apt-get update

RUN apt install git-all --yes

# Clone repo

# RUN git clone https://github.com/DalbergDataInsights/cehs.git

# RUN git checkout origin dev/2.0

# Set up the GDAL
RUN apt-get install gdal-bin --yes
RUN apt-get install libgdal-dev --yes

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set the env

WORKDIR /app/
