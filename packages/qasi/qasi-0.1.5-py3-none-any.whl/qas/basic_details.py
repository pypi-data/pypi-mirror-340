import re
from spacy.matcher import Matcher
from typing import Union

def extract_name(nlp, text) -> Union[str, None]:
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name, Middle name, and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],  # First name and Last name
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'PROPN'}],  # First name, optional punctuation, Middle name, optional punctuation, and Last name
        [{'POS': 'PROPN'}, {'IS_PUNCT': True, 'OP': '?'}, {'POS': 'PROPN'}],  # First name, optional punctuation, and Last name
    ]
    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])

    doc = nlp(text)

    matches = matcher(doc)
    for _, start, end in matches:
        span = doc[start:end]
        return " ".join([token.text for token in span])
    return None

def extract_contact_number(text) -> Union[str, None]:
    match = re.search(r"\b(?:\+?\d{1,3}[-.\s]?)??[-.\s]?\d{3}[-.\s]?\d{4}\b", text)
    return match.group() if match else None

def extract_email(text) -> Union[str, None]:
    match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", text)
    return match.group() if match else None