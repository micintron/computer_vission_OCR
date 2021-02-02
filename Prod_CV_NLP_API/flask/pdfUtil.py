""" Methods to grab text content from images ID's and transform images for better readability 

    Methods 
    ---------
    
    * pdf_to_png /: convert a pdf with all its pages into png format 


    USAGE
    -----

    call methods with respective peramiters to run code - 
"""
from pdf2image import convert_from_path

# Returns an array of output file paths for the images created from a PDF
# One file per page
#OUTPUT_FOLDER = 'output'

# for docker build
OUTPUT_FOLDER = '/output'

def pdf_to_png(filepath):
  """get the country name from target passport 

        Parameters
        ----------
        filepath:
            string of path to target pdf file 

        Returns
        -------
        :
            filepath array of paths to pdf images one for each page 
    """
  pages = convert_from_path(filepath, 500)
  filepath_array = []
  for idx, page in enumerate(pages):
    filename = OUTPUT_FOLDER+'/out' + str(idx) + '.PNG'
    page.save(filename, 'PNG')
    filepath_array.append(filename)

  return filepath_array