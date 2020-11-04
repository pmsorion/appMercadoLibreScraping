from bs4 import BeautifulSoup
import re
import string
import unicodedata
import emoji
import spacy
import en_core_web_sm
import requests
import random
import json

class debuging:

    def strip_html(text):
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()

    def remove_between_square_brackets(text):
        return re.sub('\[[^]]*\]', '', text)

    def denoise_text(text):
        text = debuging.strip_html(text)
        text = debuging.remove_between_square_brackets(text)
        return text

    def give_emoji_free_text(self, text):
        allchars = [str for str in text]
        emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
        clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
        return clean_text

    def replace_char(text):
        text = re.sub('[,"''"!@#$1234567890.:;?¿¡!]', '', text)
        text = text.replace("enero", "")
        text = text.replace("febrero", "")
        text = text.replace("marzo", "")
        text = text.replace("abril", "")
        text = text.replace("mayo", "")
        text = text.replace("junio", "")
        text = text.replace("julio", "")
        text = text.replace("agosto", "")
        text = text.replace("septiembre", "")
        text = text.replace("octubre", "")
        text = text.replace("noviembre", "")
        text = text.replace("diciembre", "")
        text = text.replace("make", "")
        text = text.replace("will", "")
        return text

    def normalize(text):
        nlp = en_core_web_sm.load()
        doc = nlp(text)
        words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
        lexical_tokens = [t.lower() for t in words if len(t) > 3 and t.isalpha()]
        return lexical_tokens

    def parce_json(text):
        json_text = json.dumps(text, ensure_ascii=False)
        data = {}
        data["words"] = []
        data["words"].append(json_text)
        return data