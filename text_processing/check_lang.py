import pandas as pd
import logging
import re
import pycld2 as cld2

from transformers import pipeline
from functools import wraps
from langdetect import detect #981kb
from google_trans_new import google_translator  

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

def _return_empty_string_for_invalid_input(func):
    """ Return empty string if the input is None or empty """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'input_text' in kwargs:
            input_text = kwargs['input_text']
        else:
            try:
                input_text = args[0]
            except IndexError as e:
                LOGGER.exception('No appropriate positional argument is provide.')
                raise e
        if input_text is None or len(input_text) == 0:
            return ''
        else:
            return func(*args, **kwargs)
    return wrapper

# pipe = pipeline("text-classification", model="jb2k/bert-base-multilingual-cased-language-detection")
pipe = lambda x : x

@_return_empty_string_for_invalid_input
def lang_checker_bert(text):
    label = ['Arabic', 'Basque', 'Breton', 'Catalan', 'Chinese_China', 'Chinese_Hongkong', 'Chinese_Taiwan', 'Chuvash', 'Czech', 'Dhivehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'French', 'Frisian', 'Georgian', 'German', 'Greek', 'Hakha_Chin', 'Indonesian', 'Interlingua', 'Italian', 'Japanese', 'Kabyle', 'Kinyarwanda', 'Kyrgyz', 'Latvian', 'Maltese', 'Mongolian', 'Persian', 'Polish', 'Portuguese', 'Romanian', 'Romansh_Sursilvan', 'Russian', 'Sakha', 'Slovenian', 'Spanish', 'Swedish', 'Tamil', 'Tatar', 'Turkish', 'Ukranian', 'Welsh']
    lang = pipe(text, truncation=True)
    output = label[int(lang['label'].split('_')[-1])]
    return output

@_return_empty_string_for_invalid_input
def lang_checker_langdetect(text):
    try:
        detected_language = detect(text)
    except Exception as e:
        print("An error occurred:", e, 'text : ', text[:15] )
        return None
    # end = time.time()
    # time_exec = end - start
    return detected_language

@_return_empty_string_for_invalid_input
def lang_checker_pycld2(text):
    try:
        detected_language = cld2.detect(text)
    except Exception as e:
        print("An error occurred:", e)
        return None
    # end = time.time()
    # time_exec = end - start
    return detected_language

@_return_empty_string_for_invalid_input
def en_to_id(text, target_lang):
    translator = google_translator()
    translate_text = translator.translate(text,lang_src='en',lang_tgt=target_lang)
    return translate_text 


@_return_empty_string_for_invalid_input
def multi_lang_abs_checker(text):
    return re.search('([^a-zA-Z0-9_])+(Abstract|Abstrak)([^a-zA-Z0-9_])*', text) != None