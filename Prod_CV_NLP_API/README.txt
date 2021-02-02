A Python Flask based API that can take in non text based documents such as a PDF of a scanned doc and a passport correctly extract the text from those images.
A Angular application to interact with said API for UI based tools such as the upload feature and visualize back results.
A Flask API for performing initial basic NLP on the processed text such as structure analysis or classification of document types.


What it uses from python
Flask==1.0.2
PassportEye==1.4.0
pillow==6.0.0
pytesseract==0.2.6
opencv-python==4.1.0.25
flask-cors==3.0.7

What it installs in the docker file
FROM python:3.7-slim-stretch
RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get install -y make
RUN apt-get -y install tesseract-ocr && apt-get -y install tesseract-ocr-fra
RUN apt install -y libsm6 libxext6

How to use it
1: make sure you have docker installed

2: open main folder in terminal call : 
docker-compose build
docker-compose up

3: once done this will build and run the docker container open docker dashboard to see it

4: Make sure you have insomnia installed

5: run a get command on http://localhost:5000
This will show you it is working


6:  run a post command on http://localhost:5000/image
Go to body set imagefile as the key - set the body to choose file

response should convert text in image - works best on images of documents

7:  run a post command on http://localhost:5000/pdf
Go to body set pdf as the key - set the body to choose file

response should convert text in pdfs - works best on pdf documents with well formatted text


8:  run a post command on http://localhost:5000/passport
Go to body set imagefile as the key - set the body to choose file

response should convert text in passport to Jason format - works only on images of passports




