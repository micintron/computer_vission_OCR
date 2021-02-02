""" Methods to grab text content from images ID's and transform images for better readability 

    Methods 
    ---------
    
    * get_country_name /: get the country name from target passport 
    * clean_name /: clean out the extracted person name from passport
    * image_to_string /: Convert image to text using tesseract OCR
    * clean_image /: Clean image of noise to better extract text using open CV
    * get_image_content /: Perform multiple operations to gather image text content from passport


    USAGE
    -----

    call methods with respective peramiters to run code - 
"""

import os
import json
import logging
from werkzeug.utils import secure_filename
from passporteye.mrz.image import MRZPipeline
from passporteye import read_mrz
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import numpy as np
import re
from random import *

#new addtions
from skimage.util import img_as_ubyte, img_as_float
from skimage.morphology import reconstruction, opening, disk, dilation, erosion, black_tophat
from skimage.io import imread, imsave
from skimage import exposure
from skimage.color import rgb2gray

# for running locally
#UPLOAD_FOLDER = 'uploads'
#EDIT_FOLDER = 'edit'

# for docker build
UPLOAD_FOLDER = '/uploads'
EDIT_FOLDER = '/edit'
MAXIMUM_IMAGE_ROTATIONS = 3


def get_country_name(country_code):
    """get the country name from target passport 

        Parameters
        ----------
        country_code:
            string of the extarct country code text

        Returns
        -------
        :
            name of country if success country code if failed
    """
    with open('countries.json') as json_file:
        data = json.load(json_file)
        for d in data:
            if d['alpha-3'] == country_code:
                return d['name']
    return country_code


def clean_name(name):
    """clean out the extracted person name from passport

        Parameters
        ----------
        name:
            string of the name extracted from the passport

        Returns
        -------
        :
           string of name with extra symbols removed 
    """
    pattern = re.compile('([^\s\w]|_)+')
    name = pattern.sub('', name)
    return name.strip()


def image_to_string(img_path):
    """Convert image to text using tesseract OCR

        Parameters
        ----------
        img_path:
            string of the path to the uploaded user image 

        Returns
        -------
        :
           string of identified image text in uppercase 
    """

    img = cv2.imread(img_path)

    # Extract the file name without the file extension
    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]

    # Create a directory for outputs
    output_path = os.path.join(EDIT_FOLDER, file_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # Apply threshold to get image with only b&w (binarization)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Save the filtered image in the output directory
    save_path = os.path.join(output_path, file_name + "_filter.jpg")
    cv2.imwrite(save_path, img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img, lang="eng")

    os.remove(save_path)
    return result.upper()


def clean_image(img):
    """Clean image of noise to better extract text using open CV

        Parameters
        ----------
        img:
            user uploaded img png or jpg

        Returns
        -------
        :
           img with colors and contrast altered to bring out text 
    """
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (5, 5), 0)
    # Apply threshold to get image with only b&w (binarization)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    return img


def get_image_content(imagefile):
    """Perform multiple operations to gather image text content from passport

        Parameters
        ----------
        imagefile:
            user uploaded img png or jpg

        Returns
        -------
        :
           passport mrz code 
           full extracted image text as string
    """

    filename = secure_filename(imagefile.filename)
    full_path = os.path.join(UPLOAD_FOLDER, filename)
    imagefile.save(full_path)

    rotations = 0
    while(rotations < MAXIMUM_IMAGE_ROTATIONS):
        # Extract informations with PassportEye
        p = MRZPipeline(full_path, extra_cmdline_params='--oem 0')
        mrz = p.result

        # Convert image to text
        full_content = image_to_string(full_path)
        # logging.info('full image content = %s' %(full_content))

        if mrz is None:
            rotate_image(full_path)
            rotations += 1
        else:
            break
    
    os.remove(full_path)
    return mrz, full_content


def rotate_image(full_path):
    """Rotate a uploaded image to better extract text

        Parameters
        ----------
        full_path:
            string path of the uploaded image 

        Returns
        -------
        None
    """

    img = cv2.imread(full_path)
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(full_path, img)


def adjust_image(img_path: str):
    """
    Adjust contrast of image with morphological filtering
    
    Parameters
    ----------
    img_path:
        path to image file
    """
    # load image and convert to greyscale, necessary for morphological filters    
    img = rgb2gray(img_as_float(imread(img_path)))
    
    # kernel for morphology is a 20-pixel circle
    selem = disk(20)
    
    # black tophat filter will highlight contiguous dark regions smaller than the kernel
    # this is useful for identifying text
    img = black_tophat(img, selem)
    
    # adjust contrast by setting anything with intensity lower than 75th percentile to black
    v_min, v_max = np.percentile(img, (75,100))
    img = exposure.rescale_intensity(img, in_range=(v_min, v_max))
    
    return img_as_ubyte(img)