import pandas as pd 
import time
import spacy

# from polyglot.detect import Detector # only can used in python 2.7 to 3.4 vers
from langdetect import detect #981kb    


DATASET = pd.read_excel('dataset/dataset_raw_deteksi_bahasa.xlsx')

def langdetect_det(text):
    # start = time.time()
    try:
        detected_language = detect(text)
    except Exception as e:
        print("An error occurred:", e)
        return None
    # end = time.time()
    # time_exec = end - start
    return detected_language

# def spacy_det(text):
#     try:
#         nlp = spacy.load("en_core_web_sm")
#         doc = nlp(text)
#         detected_language = doc._.language['language']
#         return detected_language
#     except Exception as e:
#         print("An error occurred:", e)
#         return None
    
# def detect(text):
#     langdet = langdetect_det(text)
#     # spacydet = spacy_det(text)
#     return langdet

pred_data_title = DATASET.title.apply(langdetect_det)
pred_data_abstract = DATASET.abstract.apply(langdetect_det)

pred_data = DATASET.copy()

for i in range(len(pred_data_title)):
    print(i+2, pred_data_title[i], DATASET.title_lang[i], 0 if pred_data_title[i] != DATASET.title_lang[i] else 1)

for i in range(len(pred_data_abstract)):
    print(i+2, pred_data_abstract[i], DATASET.abstract_lang[i], 0 if pred_data_abstract[i] != DATASET.abstract_lang[i] else 1)

pred_data['title_pred_langdetect'] = pred_data_title 
pred_data['abstract_pred_langdetect'] = pred_data_abstract 

pred_data.to_excel('dataset/dataset_deteksi_bahasa_langdetect.xlsx')






