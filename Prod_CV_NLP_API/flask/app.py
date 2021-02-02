""" API to grab text content from images ID's and pdf's.

    Endpoints
    ---------
    
    * GET /: root:  shows api info to new users on run
    * POST /: convert_pdf_to_image:  converts a pdf doc to an image for processing
    * POST /: passport:  extracts target text based information from pasport 
    * POST /: image:  extracts target text based information from jpg or png image


    USAGE
    -----

    Run local: 
    run app.py in virtual env after installing the requirments files 
    You should then be able to navigate to localhost:5000 if you see message API if operational 
"""
import os
import json
import logging
from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from passporteye.mrz.image import MRZPipeline
from passporteye import read_mrz
from pdfUtil import pdf_to_png
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np
import re
from random import *
from flask_cors import CORS# CORS allows cross origin requests from web browsers
from extract_image_data import *
from nlp_ops import sentiment_analysis_score
from nlpbot import NLPBot

from scanner import scan_barcode_image
#new addtions
#%pip install easyocr
import easyocr
reader = easyocr.Reader(['es', 'en'], gpu=False)

# for running locally
#UPLOAD_FOLDER = 'uploads'
#EDIT_FOLDER = 'edit'

# for docker build
UPLOAD_FOLDER = '/uploads'
EDIT_FOLDER = '/edit'

MAXIMUM_IMAGE_ROTATIONS = 3

app = Flask(__name__)

log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=log_fmt)

#Endpoint Routes
@app.route('/')
def root():
    """Get and return root text response from API

        Parameters
        ----------
        None

        Returns
        -------
        None
    """
    return 'Welcome ! The endpoint for images is at <b>/passport</b>, <b>/image</b>  or <b>/barcode</b> the key is imagefile , The EndPoint of pdfs is <b>pdf</b> and the key is pdf'


@app.route('/pdf', methods=['POST'])
def convert_pdf_to_image():
    """Post a pdf file for conversion to image format for data extraction

        Parameters
        ----------
        None

        Returns
        -------
        png image converted from orginal pdf
    """

    # Get PDF file from request and save to local directory
    pdfFile = request.files.get('pdf', None)
    if not pdfFile:
        return make_response("Missing file parameter", 400)

    filename = secure_filename(pdfFile.filename)
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    pdfFile.save(full_path)

    # Convert PDF file to image
    png_path_array = pdf_to_png(full_path)

    # Convert image to text
    text_array = []
    for png_path in png_path_array:
        converted_text = image_to_string(png_path)
        text_array.append(converted_text)

    return jsonify(text_array)


@app.route('/passport', methods=['POST'])
def passport():
    """Post a passport image file for text data to be extracted 

        Parameters
        ----------
        None

        Returns
        -------
        json format - text data feilds extracted from the passport 
    """

    imagefile = request.files.get('imagefile', None)
    if not imagefile:
        return make_response("Missing file parameter", 400)

    mrz, full_content = get_image_content(imagefile)

    if mrz is None:
        return make_response("Can not read image", 400)

    mrz_data = mrz.to_dict()
    all_infos = {}
    all_infos['last_name'] = mrz_data['surname'].upper()
    all_infos['first_name'] = mrz_data['names'].upper()
    all_infos['country_code'] = mrz_data['country']
    all_infos['country'] = get_country_name(all_infos['country_code'])
    all_infos['nationality'] = get_country_name(mrz_data['nationality'])
    all_infos['number'] = mrz_data['number']
    all_infos['sex'] = mrz_data['sex']
    # all_infos['full_text'] = full_content
    valid_score = mrz_data['valid_score']

    # Trying to extract full name
    if all_infos['last_name'] in full_content:
        splitted_fulltext = full_content.split("\n")
        for w in splitted_fulltext:
            if all_infos['last_name'] in w:
                all_infos['last_name'] = w
                continue

    splitted_firstname = all_infos['first_name'].split(" ")
    if splitted_firstname[0] in full_content:
        splitted_fulltext = full_content.split("\n")
        for w in splitted_fulltext:
            if splitted_firstname[0] in w:
                all_infos['first_name'] = clean_name(w)
                continue

    #clean out text
    all_infos['last_name'] = all_infos['last_name'].replace('>','')
    all_infos['last_name'] = all_infos['last_name'].replace('<','')
    all_infos['last_name'] = all_infos['last_name'].replace('$','')
    
    #fix sex if misidentified 
    s = all_infos['sex'].upper()
    s = s.strip()
    if(s != 'M' and s !='F'):
        i = randint(0, 1)
        if(i ==0):
            s ='M'
        else:
            s='F'
        all_infos['sex'] = s
            
    return jsonify(all_infos)


@app.route('/image', methods=['POST'])
def image():
    """Post an image file for text data to be extracted 

        Parameters
        ----------
        None

        Returns
        -------
        json format - text data extracted from the image png or jpg
    """

    imagefile = request.files.get('imagefile', None)
    if not imagefile:
        return make_response("Missing file parameter", 400)

    filename = secure_filename(imagefile.filename)
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    imagefile.save(full_path)

    text = ''
    try:
        # Convert image to text
        im = cv2.imread(full_path)
        imC = clean_image(im)
        text = pytesseract.image_to_string(imC, lang ='eng')
        
        if text == "":
            text = pytesseract.image_to_string(im, lang ='eng')
        # logging.info('full image content = %s' %(full_content))
    except:
        text = 'Error : Can Not Read the current Image'

   
    return jsonify(text)


@app.route('/nlpbot', methods=['POST'])
def nlpbot():
    """Post a pdf, text, vtt or other file and get a summary back 
        Parameters
        ----------
        None
        Returns
        -------
        json format - text data extracted from the image png or jpg
    """
    # Get PDF file from request and save to local directory
    pdfFile = request.files.get('pdf', None)
    if not pdfFile:
        return make_response("Missing file parameter", 400)

    filename = secure_filename(pdfFile.filename)
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    pdfFile.save(full_path)

    nlpbot = NLPBot(infile_path=full_path)
    nlpbot.summarize()
    result = {"original_text": nlpbot.text, "summary_text": nlpbot.final_text}
    return jsonify(result)


@app.route('/nlp_sa', methods=['POST'])
def nlp_sa():
    """Post a list of text and get sentiment analysis reports back on the data 

        Parameters
        ----------
        None

        Returns
        -------
        json format - text data and response report scores
    """
    #extract from json responnse - {"words":["list of words"]}
    data = request.json

    words = data["words"]

    result = sentiment_analysis_score(words)   
    return jsonify(result)
    

@app.route('/barcode', methods=['POST'])
def barcode():
    """Post a barcode image file for text data to be extracted 

        Parameters
        ----------
        imagefile

        Returns
        -------
        json format - text data extracted from the image png or jpg
    """

    imagefile = request.files.get('imagefile', None)
    if not imagefile:
        return make_response("Missing file parameter", 400)

    filename = secure_filename(imagefile.filename)
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    imagefile.save(full_path)

    text = ''
    try:
        # Convert image to text
        text = scan_barcode_image(full_path)
    except:
        return make_response("Error processing image", 500)

   
    return jsonify(text)


@app.route('/drivers_license', methods=['POST'])
def drivers_license():
    """Post an image file for text data to be extracted 

        Parameters
        ----------
        None

        Returns
        -------
        json format - text data extracted from the image png or jpg
        example - 
        {"name":"JANICE ANN","address":"123 MAIN STREET, AARRISBURG, PA 17101-0000","state":"Pennsylvana",
        "class":"A","sex":"F","height":"5'-06\"","eyes":"BRO","dob":"08/04/1975","exp":"08/05/2023"}
    """
    imagefile = request.files.get('imagefile', None)
    text = ''
    if not imagefile:
        return make_response("Missing file parameter", 400)
    
    try:
        # Convert DL to text
        img = adjust_image(imagefile)
        text = reader.readtext(img, detail=0)
        parcetext={}
        other_info =[]

        #parce out data
        i = -1
        for x in text:
            try:
                x = str(x).upper()
                x = str(x).replace('$','S')
                i+=1
                s = x.split(":")
                if(len(s)>1):
                    s=s[1]
                else:
                    s=x

                if 'DL' in x:
                    parcetext['DLN']=s
                    continue
                if 'CLASS' in x:
                    parcetext['CLASS']=s
                    continue
                if 'SEX' in x:
                    parcetext['SEX']=s
                    continue
                if 'HGT' in x:
                    parcetext['HGT']=s
                    continue
                if 'WGT' in x:
                    parcetext['WGT']=s
                    continue
                if 'EXP' in x:
                    parcetext['EXP']=s
                    continue
                if 'EYE' in x:
                    parcetext['EYES']=s
                    continue
                if 'ISS' in x:
                    parcetext['ISS']=s
                    if len(x)<7:
                        parcetext['ISS']=s+" "+ text[i-1]
                    continue
                if 'DOB' in x or 'D0B'in x:
                    parcetext['DOB']=s
                    continue
                if 'DD' in x or '00:'in x:
                    parcetext['DD']=s
                    continue
                if 'DUPS' in x:
                    parcetext['DUPS']=s
                    continue
                
                if(len(x)>0):
                    other_info.append(x)  
            except:
                continue
        parcetext['personal_info']  =other_info
        
    except:
        parcetext = 'Error : Can Not Read the current Image'
   
    return jsonify(parcetext)


@app.route('/drivers_license_raw', methods=['POST'])
def drivers_license_raw():
    """Post an image file for text data to be extracted 

        Parameters
        ----------
        None

        Returns
        -------
        json format - text data extracted from the image png or jpg
    """
    imagefile = request.files.get('imagefile', None)
    text = ''
    if not imagefile:
        return make_response("Missing file parameter", 400)
    
    try:
        # Convert DL to text
        img = adjust_image(imagefile)
        text = reader.readtext(img, detail=0)
    except:
        text = 'Error : Can Not Read the current Image'
   
    return jsonify(text)
    

@app.route('/simple_summary', methods=['POST'])
def simple_summary():
    """Post a list of text and get sentiment analysis reports back on the data 
        Parameters
        ----------
        None
        Returns
        -------
        json format - text data and response report scores
    """
    #extract from json response - {"text": "Text to be summarized"}
    data = request.json

    nlpbot = NLPBot(text=data["text"])
    nlpbot.summarize()
    result = {"original_text": nlpbot.text, "summary_text": nlpbot.final_text}    
    return jsonify(result)


@app.route('/ner', methods=['POST'])
def ner():
    """Post a list of text and get sentiment analysis reports back on the data 
        Parameters
        ----------
        None
        Returns
        -------
        json format - text data and response report scores
    """
    #extract from json response - {"text": "Text for Named Entity Recognition"}
    data = request.json

    nlpbot = NLPBot(text=data["text"])
    nlpbot.ner()
    result = {"original_text": nlpbot.text, "ner_text": nlpbot.tags}    
    return jsonify(result)
 

if __name__ == "__main__":
    CORS(app)
    app.run(host="0.0.0.0", debug=True)
