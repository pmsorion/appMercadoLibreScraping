import os
from os import path
from FacebookPostsScraper import FacebookPostsScraper as Fps
from pprint import pprint as pp
#from python_graphql_client import GraphqlClient
from database import database as dbs
import json
from bs4 import BeautifulSoup
import re
import string
import unicodedata
import emoji
import spacy
import en_core_web_sm
import requests
import random
from flask import Flask, jsonify, make_response

app = Flask(__name__)

tasks = [{'id': 1}]

def strip_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
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

def processWords(words):
    word = words[random.randrange(0, len(words), 1)]
    data_podium = processWordtoWord(word)
    return data_podium

def processWordtoWord(word):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    url = (f'http://listado.mercadolibre.com.mx/{word}#D[A:{word},L:1]')

    response = requests.get(url,headers=headers)#, proxies=proxies)

    items = []

    content = response.content
    soup = BeautifulSoup(content, 'lxml')

    for item in soup.select('.ui-search-layout__item'):
        try:
            items.append([item.select('a')[0]['title'], item.select('a')[0]['href'], item.select('.price-tag')[0].get_text(), item.select('.ui-search-result-image__element')[0]['data-src']])
        except:
            Exception

    LIMIT = 3
    counter = 0
    podium = []
    while counter < LIMIT:
        podium.append(items[random.randrange(0, len(items), 1)])
        counter += 1

    json_podium = json.dumps(podium, ensure_ascii=False)
    data_podium = {}
    data_podium["products"] = []
    data_podium["products"].append(json_podium)

    return data_podium

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        not_found(404)

    #id_user_facebok = conect_graphql(task_id)
    id_user_facebok = dbs.conect_graphql(task_id)

    # Enter your Facebook email and password
    email = 'sue@synapbox.com'
    password = 'Suevcello30'

    # Instantiate an object
    fps = Fps(email, password, post_url_text='Full Story')

    # Example with single profile
    single_profile = id_user_facebok #facebook user
    data = fps.get_posts_from_profile(single_profile)

    fps.posts_to_csv('my_posts')  # You can export the posts as CSV document

    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text = open(path.join(d, 'my_posts.csv')).read()

    text = denoise_text(text)
    text = give_emoji_free_text(r'',text)
    text = replace_char(text)
    text = normalize(text)
    data = parce_json(text)
    data_podium = processWords(text)

    # Synchronous mutation
    dataResponse = dbs.podium_graphql(data_podium)
    #dataResult = client.execute(query=mutation_result, variables=variables_result)

    return jsonify(dataResponse)

if __name__ == '__main__':
    app.run(debug=True)