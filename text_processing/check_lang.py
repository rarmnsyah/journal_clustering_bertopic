import pandas as pd
import logging
import re

from transformers import pipeline
from functools import wraps

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

pipe = pipeline("text-classification", model="jb2k/bert-base-multilingual-cased-language-detection")

@_return_empty_string_for_invalid_input
def lang_checker(text):
    label = ['Arabic', 'Basque', 'Breton', 'Catalan', 'Chinese_China', 'Chinese_Hongkong', 'Chinese_Taiwan', 'Chuvash', 'Czech', 'Dhivehi', 'Dutch', 'English', 'Esperanto', 'Estonian', 'French', 'Frisian', 'Georgian', 'German', 'Greek', 'Hakha_Chin', 'Indonesian', 'Interlingua', 'Italian', 'Japanese', 'Kabyle', 'Kinyarwanda', 'Kyrgyz', 'Latvian', 'Maltese', 'Mongolian', 'Persian', 'Polish', 'Portuguese', 'Romanian', 'Romansh_Sursilvan', 'Russian', 'Sakha', 'Slovenian', 'Spanish', 'Swedish', 'Tamil', 'Tatar', 'Turkish', 'Ukranian', 'Welsh']
    lang = pipe(text, truncation=True)

@_return_empty_string_for_invalid_input
def multi_lang_abs(text):
    return re.search('([^a-zA-Z0-9_])+(Abstract|Abstrak)([^a-zA-Z0-9_])*', text) != None