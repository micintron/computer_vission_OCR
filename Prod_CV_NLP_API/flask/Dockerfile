FROM python:3.7-slim-stretch


ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --no-install-recommends -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    gcc \
    g++ \
    libpoppler-cpp-dev \
    pkg-config \
    libsm6 \
    libxext6 \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y make
#RUN apt-get -y install tesseract-ocr && apt-get -y install tesseract-ocr-fra
#RUN apt-get -y install gcc g++ libpoppler-cpp-dev pkg-config
#RUN apt install -y libsm6 libxext6
#RUN apt install poppler-utils -y

COPY . /flask
WORKDIR /flask

RUN mkdir /uploads
RUN mkdir /output


RUN pip install -r requirements.txt
CMD ["python", "app.py"]
