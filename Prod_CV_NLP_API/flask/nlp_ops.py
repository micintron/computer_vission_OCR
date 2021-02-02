""" Use BERT based sentiment analiysis combined with our knowlege of flag targets from MPA's to score and target risk 
    in text extracted from our other service tools


    USAGE
    -----
    reference the risk_score method with its propper paramiters to extract scores from a full
    list of text examples

    Required Function and its parameters
    risk_score(words : list, spelling : bool = False):
"""
import ipywidgets as widgets
from transformers import pipeline
print('Please wait a moment for AI Models to Load...')
nlp_sentence_classif = pipeline('sentiment-analysis')


def test():
    """test the return of model on a basic statment

        Returns
        -------
            print out text's full evaluation after data is sent to the bert model 
    """
    res =nlp_sentence_classif('this was a good time')
    print(res)


def sentiment_analysis_score(words : list):
    """get the country name from target passport 

        Parameters
        ----------
        words:
            string of the extarct country code text

        Returns
        -------
        :
            all text sent with nlp scores in json format 
    """
    try:
        results = {}
        scores = []
        for x in words:
            result=[]
            result.append(x)
            res =nlp_sentence_classif(x)
            result.append(res)
            scores.append(result)
        
        results['scores']= scores

        return results

    except:
        return None



# run local test 
# test()
# words = ['this was great', 'this sucked', 'i loved the resturant', 'i hate the resturant', 'lets leave now please']
# print(sentiment_analysis_score(words))