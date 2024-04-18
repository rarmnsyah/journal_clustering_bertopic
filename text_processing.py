import os
import re
import string
import logging

from typing import List, Optional, Callable
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


@_return_empty_string_for_invalid_input
def to_lower(input_text: str) -> str:
    """ Convert input text to lower case """
    return input_text.lower()

@_return_empty_string_for_invalid_input
def to_upper(input_text: str) -> str:
    """ Convert input text to upper case """
    return input_text.upper()

@_return_empty_string_for_invalid_input
def remove_url(input_text: str) -> str:
    """ Remove url in the input text """
    return re.sub('(www|http)\S+', '', input_text)

@_return_empty_string_for_invalid_input
def remove_number(input_text: str) -> str:
    """ Remove number in the input text """
    processed_text = re.sub('\d+', '', input_text)
    return processed_text

@_return_empty_string_for_invalid_input
def remove_nbsp(input_text: str) -> str:
    """ Remove tag nbsp in the input text """
    processed_text = re.sub('&nbsp', '', input_text)
    return processed_text

@_return_empty_string_for_invalid_input
def remove_abs_word(input_text: str) -> str:
    """ Remove abstract words in first sentence in the input text """
    processed_text = re.sub('^(Abstrak|Abstract|ABSTRAK|ABSTRACT)+', '', input_text)
    return processed_text

@_return_empty_string_for_invalid_input
def remove_multilang(input_text: str) -> str:
    """ Remove multi lang and only keep the first language in the input text """
    processed_text = re.sub('(Abstract|Abstrak|ABSTRAK|ABSTRACT).*', '', input_text)
    return processed_text

@_return_empty_string_for_invalid_input
def remove_katakunci(input_text: str) -> str:
    """ Remove kata kunci if theres in the input text """
    processed_text = re.sub('(Kata kunci|Keywords|Keyword).*', '', input_text)
    return processed_text

# @_return_empty_string_for_invalid_input
# def remove_physics_sign(input_text: str) -> str:
#     """ Remove number in the input text """
#     processed_text = re.sub(' (.+\/.+) ', ' ', input_text)
#     return processed_text

@_return_empty_string_for_invalid_input
def remove_itemized_bullet_and_numbering(input_text: str) -> str:
    """ Remove bullets or numbering in itemized input """
    processed_text = re.sub('[(\s][0-9a-zA-Z][.)]\s+|[(\s][ivxIVX]+[.)]\s+', ' ', input_text)
    return processed_text

@_return_empty_string_for_invalid_input
def remove_punctuation(input_text: str, punctuations: Optional[str] = None) -> str:
    """
    Removes all punctuations from a string, as defined by string.punctuation or a custom list.
    For reference, Python's string.punctuation is equivalent to '!"#$%&\'()*+,-./:;<=>?@[\\]^_{|}~'
    """
    if punctuations is None:
        punctuations = string.punctuation
    processed_text = input_text.translate(str.maketrans('', '', punctuations))
    return processed_text


@_return_empty_string_for_invalid_input
def remove_special_character(input_text: str, special_characters: Optional[str] = None) -> str:
    """ Removes special characters """
    if special_characters is None:
        # TODO: add more special characters
        special_characters = 'å¼«¥ª°©ð±§µæ¹¢³¿®ä£'
    processed_text = input_text.translate(str.maketrans('', '', special_characters))
    return processed_text


@_return_empty_string_for_invalid_input
def keep_alpha_numeric(input_text: str) -> str:
    """ Remove any character except alphanumeric characters """
    return re.sub(r'[^ \w+]', '', input_text)


@_return_empty_string_for_invalid_input
def remove_whitespace(input_text: str, remove_duplicate_whitespace: bool = True) -> str:
    """ Removes leading, trailing, and (optionally) duplicated whitespace """
    if remove_duplicate_whitespace:
        return ' '.join(re.split('\s+', input_text.strip(), flags=re.UNICODE))
    return input_text.strip()

@_return_empty_string_for_invalid_input
def remove_email(input_text: str) -> str:
    """ Remove email in the input text """
    regex_pattern = '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}'
    return re.sub(regex_pattern, '', input_text)

@_return_empty_string_for_invalid_input
def remove_tag(input_text: str) -> str:
    """ Remove email in the input text """
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(CLEANR, '', input_text)

@_return_empty_string_for_invalid_input
def remove_phone_number(input_text: str) -> str:
    """ Remove phone number in the input text """
    regex_pattern = '(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?'
    return re.sub(regex_pattern, '', input_text)

@_return_empty_string_for_invalid_input
def bersihkan_abstrak(input_text: str) -> str:
    """Clean abstract text by removing keywords, special characters, and non-alphanumeric characters."""
    input_text = input_text.lower()
    # Split text based on "ABSTRAK" or "Abstract" to get the abstract section
    bagian_abstrak = re.split(r'abstrak|abstract', input_text)[-1].strip()

    # Split the resulting text by '\n', '.' to get individual lines
    lines = re.split(r'\n|\.\s|\.', bagian_abstrak)

    # Remove lines containing keywords "Kata kunci" or "kata kunci:"
    cleaned_lines = [line for line in lines if not line.startswith('kata kunci')]

    # Join the cleaned lines back into a single string
    cleaned_abstract = ' '.join(cleaned_lines).strip()

    # Remove '&nbsp;' from the text
    # cleaned_abstract = cleaned_abstract.replace("&nbsp;", '')

    # # Remove special characters from the text
    # cleaned_abstract = cleaned_abstract.translate(str.maketrans('', '', 'å¼«¥ª°©ð±§µæ¹¢³¿β®äâ£'))

    # # Keep only alphanumeric characters
    # cleaned_abstract = re.sub(r'[^ \w+]', '', cleaned_abstract)

    # # Remove numbers from the text
    # cleaned_abstract = re.sub('\d+', '', cleaned_abstract)

    # Find the position of the keyword "kata kunci"
    keyword_position = cleaned_abstract.find('kata kunci')
    
    # If the keyword is found, remove text after it
    if keyword_position != -1:
        cleaned_abstract = cleaned_abstract[:keyword_position]

    return cleaned_abstract

def preprocess_text(input_text: str, processing_function_list: Optional[List[Callable]] = None) -> str:
    """ Preprocess an input text by executing a series of preprocessing functions specified in functions list """
    if processing_function_list is None:
        processing_function_list = [
            remove_tag,
            bersihkan_abstrak,
            remove_nbsp,
            remove_special_character,
            keep_alpha_numeric,
            remove_number
        ]
    for func in processing_function_list:
        input_text = func(input_text)
    if isinstance(input_text, str):
        processed_text = input_text
    else:
        processed_text = ' '.join(input_text)
    return processed_text

