""" Use BERT based summarization through a class with a full summarization pipeline 
    that takes in raw text and transforms it into a full concatinated summery of the orginal
    
    USAGE
    -----
    reference the NLPBot class method with its propper paramiters to instantiate the object
    then reference a subsequent class method to use its specific service such as 
    summarize()

    Required Function and its parameters
    pdf_get_text(self)
    vtt_get_text(self)
    summarize(self)
"""
import os
import argparse
import re
import docx
import math
import pdftotext
from transformers import pipeline

print('Initializing summarization pipeline...')
summarizer = pipeline('summarization')
#print('Initializing NER pipeline...')
#ner = pipeline('ner', grouped_entities=True)

# holding place for ner pipeline - sometimes has memory issues
# if all bert pipelines downloaded on app init
ner = print

class NLPBot:
    '''NLPs!'''
    def __init__(self, text='', infile_path='', outfile_path='', batch_size=2700, tags=False, nlp_kwargs=None):
        """initilze the NLPbot class 

            Parameters
            ----------
        text='', 
                orginial text
        infile_path='', 
                targeted file path
        outfile_path='', 
                out file path
        batch_size=2700, 
                max size of batch 
        tags=False, 
                bool for using tags or not
        nlp_kwargs=None
                any keyword arguments

            Returns
            -------
            :
                None
        """
        self.infile_path = infile_path
        self.text = text
        
        print("Extacting text...")
        if self.infile_path[-3:] == 'pdf':
            self.pdf_get_text()

        if self.infile_path[-3:] == 'vtt':
            self.vtt_get_text()

        self.outfile_path = outfile_path
        self.batch_size = batch_size
               
        self.nlp_results = [] 
        self.tags = ''

    def pdf_get_text(self):
        """get pdf text

            Parameters
            ----------
                None

            Returns
            -------
            :
                extracted pdf text 
        """
        with open(self.infile_path, 'rb') as f:
            self.pages = pdftotext.PDF(f)
        self.text = '\n\n'.join(page for page in self.pages)

    def vtt_get_text(self):
        """MS Stream Transcripts

            Parameters
            ----------
                None

            Returns
            -------
            :
                alltered orginal text
        """
        with open(self.infile_path, 'r') as f:
            transcript = f.read()
        keepers = []
        for line in transcript.split('\n')[1:]:
    
            if line == '' or 'NOTE' in line or '-' in line:
                pass
            else:
                keepers.append(line)
        
        self.text = " ".join(keepers)

    def ner(self):
        """perform name entity recognition 

            Parameters
            ----------
                None

            Returns
            -------
            :
                sumerized text with NER tags
        """
        tag_set = set()
        for x in self.do_nlp(ner):
            print("Inside ner loop:", x)
            tag_set.update(set(item['word'] for item in x))
            print(tag_set)
        self.tags = ", ".join(tag_set)

    def summarize(self):
        """summerize the text

            Parameters
            ----------
                None

            Returns
            -------
            :
                summerized orginal text 
        """
        self.summaries = list(s[0]['summary_text'] for s in self.do_nlp(summarizer, min_length=5, max_length=200))
        self.clean_summaries()
        return self.final_text

    def do_nlp(self, nlp_pipe, **kwargs):
        """Summarizes text scraped from links

            Parameters
            ----------
                nlppipe:
                the pipline for text to go to model
                kwargs:
                the key word arguments associated with the model

            Returns
            -------
            :
                nlp pipeline output text
        """
        N = len(self.text)
        print("\n\nInside get_summaries\n", N, self.text)
        # maker sure n_batches is always at least 1
        n_batches = math.ceil((N+1) / self.batch_size)
        batch = N // n_batches

        for i in range(0, N, batch):
            print(i, batch+i)
            section = self.text[i:(i+batch)]
            if len(section) < 5:
                print("section too short")
                continue

            output = nlp_pipe(section, **kwargs)
            print(output)
            yield output     

    def clean_summaries(self):
        """Cleans summarized text

            Parameters
            ----------
                None

            Returns
            -------
            :
                summerized and cleaned final text
        """
        print("Inside clean_summaries")
        self.final_text = ". ".join(sentence[0].upper() + sentence[1:] for sentence in "\n".join(self.summaries).split(" . "))
        return self.final_text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Various NLP Pipelines Courtesy of Huggingface")
    #parser.add_argument('infile_path', type=str, help="Path to file to be read (pdf, vtt, etc.)")
    #parser.add_argument('outfile_path', type=str, help="Word Document filepath")
    #args = parser.parse_args()

    wp = NLPBot(text="The Big Blue ball is a ball of fun. I love to bounce the ball.  Soccer is a fun sport that children love!  They kick the ball and play and exercise - what a charming time is something the English say!")
    wp.summarize()
    print(wp.final_text)
    wp.ner()
    print(wp.tags)