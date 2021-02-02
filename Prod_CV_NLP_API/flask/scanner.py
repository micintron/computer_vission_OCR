""" Net steps work : build code to fully scan a licence barcode using ZXing Barcode 
    scanner from image
    
"""
import argparse
from pyzxing import BarCodeReader
from license_decoder import decode_license

parser = argparse.ArgumentParser(
    description="A Python Wrapper of ZXing Barcode Scanner")
parser.add_argument('-f', '--file', default=None)
args = parser.parse_args()


def barcode_to_string(imagefile):
    reader = BarCodeReader()
    results = reader.decode(imagefile)
    return results[0].get('parsed')

def scan_barcode_image(imagefile):
    results_string = barcode_to_string(imagefile)
    decoded_string = decode_license(results_string)
    return decoded_string

def main(args):
    results_string = barcode_to_string(args.file)
    decoded_string = decode_license(results_string)
    for key in decoded_string:
        print(key + ": " + decoded_string[key])


if __name__ == '__main__':
    main(args)
