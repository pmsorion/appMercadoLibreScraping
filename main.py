import os
from os import path
from FacebookPostsScraper import FacebookPostsScraper as Fps
from database import database as dbs
from debuging import debuging as dbg
from textprocessor import textprocessor as txtpr
from pprint import pprint as pp
from flask import Flask, jsonify, make_response
import json

app = Flask(__name__)

tasks = [{'id': 1}]

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

    text = dbg.denoise_text(text)
    text = dbg.give_emoji_free_text(r'',text)
    text = dbg.replace_char(text)
    text = dbg.normalize(text)
    data = dbg.parce_json(text)
    data_podium = txtpr.processWords(text)

    # Synchronous mutation
    dataResponse = dbs.podium_graphql(data_podium)
    #dataResult = dbs.search_result_graphql(task_id, data)

    return json.dumps(data_podium)

if __name__ == '__main__':
    app.run(debug=True)