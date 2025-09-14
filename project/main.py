import json
import re
import os

import requests
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    abort,
    send_from_directory,
    current_app,
    jsonify,
    flash,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from markupsafe import escape

from . import (
    uuid4_utils, mongo_client, mongo_data, mongo_images
)
from .uuid4_utils import is_valid_uuid4

_questions = [
    {
        'cif': 'CIF-919ae5a5-34e4-4b88-979a-5187d46d1617',
        'quid': 'QID-42cb197a-d10f-47e6-99bb-a814d4ca95da',
        'name': 'questionA'
    },
    {
        'cif': 'CIF-919ae5a5-34e4-4b88-979a-5187d46d1617',
        'quid': 'QID-ba88f889-37d3-41ec-8829-d7ea2a45c61c',
        'name': 'questionB'
    },
    {
        'cif': 'CIF-919ae5a5-34e4-4b88-979a-5187d46d1617',
        'quid': 'QID-05db84d8-27ac-4067-9daa-d743ff56929b',
        'name': 'questionC'
    }
]

_quizzes = [
    {
        'cif': 'CIF-919ae5a5-34e4-4b88-979a-5187d46d1617',
        'quid': 'QID-42cb197a-d10f-47e6-99bb-a814d4ca95da',
        'qzid': 'QIZ-3021178c-c430-4285-bed2-114dfe4db9df',
        'name': 'quizA'
    },
    {
        'cif': 'CIF-919ae5a5-34e4-4b88-979a-5187d46d1617',
        'quid': 'QID-ba88f889-37d3-41ec-8829-d7ea2a45c61c',
        'qzid': 'QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86',
        'name': 'quizB'
    },
    {
        'cif': 'CIF-919ae5a5-34e4-4b88-979a-5187d46d1617',
        'quid': 'QID-05db84d8-27ac-4067-9daa-d743ff56929b',
        'qzid': 'QIZ-74751363-3db2-4a82-b764-09de11b65cd6',
        'name': 'quizC'
    }
]

main = Blueprint('main', __name__, static_folder='/static')


@main.route('/')
def index():
    return render_template("index.html")



@main.route('/login', methods=['GET', 'POST'])
def login():
    # https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY
    if request.method == 'POST':
        data = request.form
        # return jsonify(data), 200
        current_user.session['username'] = request.form['username']
        current_user.session['cif'] = 'a5366e29-4314-4b91-b90b-1639da02c2d8'
        current_user.session['theme'] = 'hootstrap'  # 'hootstrap', 'fresca', 'herbie'
        return redirect(url_for('index'))
    else:
        return render_template("login.html")

@main.route('/logout')
def logout():
    # remove the username from the session if it's there
    current_user.session.pop('username', None)
    return redirect(url_for('index'))


# https://www.digitalocean.com/community/tutorials/how-to-use-and-validate-web-forms-with-flask-wtf
# https://flask.palletsprojects.com/en/stable/patterns/wtforms/
courses_list = [{
    'title': 'Python 101',
    'description': 'Learn Python basics',
    'price': 34,
    'available': True,
    'level': 'Beginner'
},
    {
        'title': 'How To Build Web Applications with Flask',
        'description': 'How To Create Your First Web Application Using Flask and Python 3',
        'price': 50,
        'available': True,
        'level': 'Beginner'
    }]


@main.route('/courses')
def courses():
    return render_template('courses.html', courses_list=courses_list)


@main.route('/add-course', methods=['GET', 'POST'])
def add_course():
    form = CourseForm()
    return render_template('add-course.html', form=form)


@main.route('/question1')
def question1():
    _quid = _questions[0]['quid']

    _collection = mongo_data.questions
    # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
    _dict = _collection.find_one({'quid': _quid}, {'_id': 0, 'data': 1})
    if _dict:
        return render_template("question1.html", data=_dict["data"])  # need data array
    return jsonify(_dict), 200


@main.route('/deutsch')
def deutsch():
    return render_template("deutsch.json")


@main.route('/flex-question')
def flex_question():
    _quid = _questions[0]['quid']

    _collection = mongo_data.questions
    # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
    _dict = _collection.find_one({'quid': _quid}, {'_id': 0, 'data': 1})
    if _dict:
        return render_template("flexquestion.html", data=_dict["data"])  # need data array
    return jsonify(_dict), 200


@main.route('/form-grid', methods=['GET', 'POST'])
def form_grid():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        _quid = _questions[0]['quid']
        _collection = mongo_data.questions
        # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
        _dict = _collection.find_one({'quid': _quid}, {'_id': 0, 'data': 1})
        if _dict:
            return render_template("formgrid.html", data=_dict["data"])  # need data array
        return jsonify(_dict), 200


@main.route('/nouns-table-result')
def nouns_table_result():
    return render_template("nouns-result.html")


@main.route('/quiz', methods=['GET', 'POST'])
def nouns_quiz():
    if request.method == 'POST':
        _request = request.form
        # return jsonify(_request), 200
        _request_values = {}  # sanitize _request in another Dictionary (_request immutable)

        # Check UUID values, and build 'data' array for responses
        for _key in _request:
            if _key == 'cif':
                if is_valid_uuid4(escape(_request['cif'])):
                    _request_values['cif'] = "CIF-{0}".format(escape(_request['cif']))
            if _key == 'quid':
                if is_valid_uuid4(escape(_request['quid'])):
                    _request_values['quid'] = "QID-{0}".format(escape(_request['quid']))
            if _key == 'qzid':
                if is_valid_uuid4(escape(_request['qzid'])):
                    _request_values['qzid'] = "QIZ-{0}".format(escape(_request['qzid']))
            if _key.startswith('name-radio-'):
                _key_name = _key.replace('name-radio-', '')
                _request_values[_key_name] = escape(_request[_key])

        if _request_values:
            # return jsonify(_request_values), 200 # sanitized (cooked :-))
            # if _request:
            #     return jsonify(_request), 200    # raw

            # Extract 'Ans' and 'Plural' for each 'Noun' from 'quid'
            _question_ans = mongo_data.questions.find_one({'quid': _request_values['quid']},
                                                          {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1,
                                                           'data': {'Label': 1, 'Noun': 1, 'Ans': 1, 'Plural': 1}})
            _question_ans_data = _question_ans['data']

            # Extract _quiz ('qzid') corresponding to _request_values['gzid']
            _quiz = mongo_data.quizzes.find_one({'qzid': _request_values['qzid']},
                                                {'_id': 0, 'cif': 1, 'quid': 1, 'qzid': 1, 'name': 1, 'data': 1})

            # Add extra fields to _quiz with default values
            for _x in _quiz['data']:
                _x['Ans'] = None
                _x['Correct'] = 'x'
                _x['Choice'] = None
                _x['Plural'] = None

            # Populate _quiz 'Ans', 'Plural' with _question 'Ans', 'Plural'
            for _x in _quiz['data']:
                for _y in _question_ans_data:
                    if _x['Label'] == _y['Label']:
                        _x['Ans'] = _y['Ans']
                        _x['Plural'] = _y['Plural']

            # Check Ans (answer), 'Plural' check no done
            # Loop over sanitized POST response (_request_values) and update _quiz 'Choice', 'Correct'
            for _key, _value in _request_values.items():
                for _y in _quiz['data']:
                    if _key == _y['Label']:
                        _y['Choice'] = _value
                        _y['Correct'] = 'n'
                        if _value == _y['Ans']:
                            _y['Correct'] = 'y'

            # Score totals added to _meta_data
            _correct_ans = 0
            _incorrect_ans = 0
            _unanswered = 0

            for _x in _quiz['data']:
                if _x["Correct"] == "y":
                    _correct_ans += 1
                elif _x["Correct"] == "n":
                    _incorrect_ans += 1
                else:
                    _unanswered += 1

            # return jsonify(_quiz), 200

            # _quiz = {
            #  "cif": "CIF-919ae5a5-34e4-4b88-979a-5187d46d1617",
            #  "quid": "QID-ba88f889-37d3-41ec-8829-d7ea2a45c61c",
            #  "qzid": "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86",
            #  "name": "quizB",
            #  "data": [
            #    {"Ans": "die", "Choice": "der", "Correct": "n", "Desc": "Stamp", "Label": "Q01", "Noun": "Briefmarke",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Briefmarken"},
            #    {"Ans": "die", "Choice": "die", "Correct": "y", "Desc": "Bill, Invoice", "Label": "Q02",
            #     "Noun": "Rechnung", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Rechnungen"},
            #    {"Ans": "das", "Choice": "das", "Correct": "y", "Desc": "Telephone", "Label": "Q03", "Noun": "Telefon",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Telefone"},
            #    {"Ans": "das", "Choice": "die", "Correct": "n", "Desc": "Form", "Label": "Q04", "Noun": "Formular",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Formulare"},
            #    {"Ans": "der", "Choice": "die", "Correct": "n", "Desc": "Printer", "Label": "Q05", "Noun": "Drucker",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Drucker"}
            #  ]
            # }
            _meta_data = {'name': _quiz['name'], 'cif': _quiz['cif'].replace('CIF-', ''),
                          'quid': _quiz['quid'].replace('QID-', ''), 'qzid': _quiz['qzid'].replace('QIZ-', ''),
                          'correct': _correct_ans, 'incorrect': _incorrect_ans, 'unanswered': _unanswered}

            # return jsonify(_meta_data), 200
            # return jsonify(_data), 200
            return render_template("nouns-result.html", data=_quiz["data"], meta_data=_meta_data)

        return jsonify(_request), 404

    else:
        _quiz_id = None
        _request_values_id = None
        try:
            _request_values_id = request.args.get('id', '')  # (key, default, type)
        except KeyError:
            abort(400)

        # _request_values_id = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df", "name": "quizA"
        if _request_values_id.startswith('qiz-'):
            _request_values_id = _request_values_id.replace('qiz', 'QIZ', 1)

        _quiz_id = _request_values_id.replace('QIZ-', '')

        _collection = mongo_data.quizzes
        # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
        # db.quizzes.find({qzid:'QIZ-3021178c-c430-4285-bed2-114dfe4db9df'},{_id:0,data:1})
        _dict = _collection.find_one({'qzid': _request_values_id}, {'_id': 0, 'data': 1})
        # return jsonify(_dict), 200

        # db.quizzes.find({qzid:'QIZ-3021178c-c430-4285-bed2-114dfe4db9df'},{_id:0,cif:1,qzid:1,quid:1,name:1})
        _meta_data = _collection.find_one({'qzid': _request_values_id},
                                          {'_id': 0, 'cif': 1, 'quid': 1, 'qzid': 1, 'name': 1})
        # return jsonify(_meta_data), 200

        if _meta_data is None:
            abort(400)

        # strip prefix, so pure UUID sent/received on GET/POST
        _meta_data['cif'] = _meta_data['cif'].replace('CIF-', '')
        _meta_data['quid'] = _meta_data['quid'].replace('QID-', '')
        _meta_data['qzid'] = _meta_data['qzid'].replace('QIZ-', '')
        # return jsonify(_meta_data), 200

        if _dict:
            return render_template("nouns-quiz.html", data=_dict["data"], meta_data=_meta_data)

        return jsonify(_dict), 200


@main.route('/form-grid2', methods=['GET', 'POST'])
def form_grid2():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        _quid = _questions[1]['quid']
        _collection = mongo_data.questions
        # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
        _dict = _collection.find_one({'quid': _quid}, {'_id': 0, 'data': 1})
        if _dict:
            return render_template("formgrid2.html", data=_dict["data"])  # need data array
        return jsonify(_dict), 200


@main.route('/radio-button')
def radio_button():
    _quid = _questions[0]['quid']
    _collection = mongo_data.questions
    # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
    _dict = _collection.find_one({'quid': _quid}, {'_id': 0, 'data': 1})
    if _dict:
        return render_template("radiobutton.html", data=_dict["data"])  # need data array
    return jsonify(_dict), 200


# allow both GET and POST requests
@main.route('/form-example', methods=['GET', 'POST'])
def form_example():
    # handle the POST request
    if request.method == 'POST':
        language = request.form.get('language')
        framework = request.form.get('framework')
        return '''
                      <h1>The language value is: {}</h1>
                      <h1>The framework value is: {}</h1>'''.format(language, framework)

    # otherwise handle the GET request
    return '''
               <form method="POST">
                   <div><label>Language: <input type="text" name="language"></label></div>
                   <div><label>Framework: <input type="text" name="framework"></label></div>
                   <input type="submit" value="Submit">pi
               </form>'''


# GET requests will be blocked
@main.route('/json-echo', methods=['POST'])
def json_echo():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    return jsonify(data), 200


@main.route('/json-form', methods=['GET', 'POST'])
def json_form():
    if request.method == 'POST':
        data = request.form
        # return data # => returns identical JSON output
        return jsonify(data), 200

    else:
        return render_template("jsonform.html")


# flask> db.questions.find({},{_id:0,cif:1,quid:1,name:1})
# https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html
# https://www.mongodb.com/docs/manual/tutorial/query-documents/
@main.route('/api/questions')
def get_questions():
    _collection = mongo_data.questions
    _answer = []
    for doc in _collection.find({}, {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1}):
        _answer.append(doc)

    return jsonify(_answer), 200


@main.route('/api/quizzes')
def get_quizzes():
    _collection = mongo_data.quizzes
    _answer = []
    for doc in _collection.find({}, {'_id': 0, 'cif': 1, 'qzid': 1, 'quid': 1, 'name': 1}):
        _answer.append(doc)

    return jsonify(_answer), 200


@main.route('/api/mongo-collections')
def get_mongodb_collections():
    _answer = mongo_data.list_collection_names()
    return jsonify(_answer), 200


# @main.route('/api/user/<username>/')
# redirects to URL with trailing '/', search engines will index twice
# https://flask.palletsprojects.com/en/stable/quickstart/#unique-urls-redirection-behavior
@main.route('/api/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'


# Needs trailing '/' to accept because URL is not unique
@main.route('/api/question/<cif>/<quid>/')
def get_cif_quid_json(cif, quid):
    # "cif": "CIF-919ae5a5-34e4-4b88-979a-5187d46d1617",
    # "quid": "QID-05db84d8-27ac-4067-9daa-d743ff56929b",
    # "name": "questionC",

    _cif_id = escape(cif)
    if not is_valid_uuid4(_cif_id):
        _json_error = {'message': 'invalid cif', 'code': 404, 'value': _cif_id}
        return jsonify(_json_error), 404

    _quid = escape(quid)
    if not is_valid_uuid4(_quid):
        _json_error = {'message': 'invalid question_id', 'code': 404, 'value': _quid}
        return jsonify(_json_error), 404

    _question_id = 'QID-' + _quid
    _collection = mongo_data.questions
    _answer = _collection.find_one({'quid': _question_id}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@main.route('/api/question/<quid>')
def get_quid_json(quid):
    # QID-05db84d8-27ac-4067-9daa-d743ff56929b - questions/05db84d8-27ac-4067-9daa-d743ff56929b
    _quid = escape(quid)

    if not is_valid_uuid4(_quid):
        _json_error = {'message': 'invalid question_id', 'code': 404, 'value': _quid}
        return jsonify(_json_error), 404

    _question_id = 'QID-' + _quid
    _collection = mongo_data.questions
    _answer = _collection.find_one({'quid': _question_id}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


# Needs trailing '/' to accept because URL is not unique
@main.route('/api/quiz/<cif>/<quiz_id>/')
def get_cif_qzid_json(cif, quiz_id):
    # /quiz: CIF=919ae5a5-34e4-4b88-979a-5187d46d1617 / QZID=74751363-3db2-4a82-b764-09de11b65cd6
    # QIZ-74751363-3db2-4a82-b764-09de11b65cd6 ('QIZ-' + QZID)
    # db.quizzes.find({"cif":"CIF-919ae5a5-34e4-4b88-979a-5187d46d1617","qzid":"QIZ-74751363-3db2-4a82-b764-09de11b65cd6"},{_id:0,data:1})
    _cif_id = escape(cif)
    if not is_valid_uuid4(_cif_id):
        _json_error = {'message': 'invalid cif', 'code': 404, 'value': _cif_id}
        return jsonify(_json_error), 404

    _quiz_id = escape(quiz_id)
    if not is_valid_uuid4(_quiz_id):
        _json_error = {'message': 'invalid quiz_id', 'code': 404, 'value': _quiz_id}
        return jsonify(_json_error), 404

    _cif = 'CIF-' + _cif_id
    _quiz = 'QIZ-' + _quiz_id
    _collection = mongo_data.quizzes
    _answer = _collection.find_one({'cif': _cif, 'qzid': _quiz}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@main.route('/api/quiz/<quiz_id>')
def get_qzid_json(quiz_id):
    _quiz_id = escape(quiz_id)

    if not is_valid_uuid4(_quiz_id):
        _json_error = {'message': 'invalid quiz_id', 'code': 404, 'value': _quiz_id}
        return jsonify(_json_error), 404

    _quiz = 'QIZ-' + _quiz_id
    _collection = mongo_data.quizzes
    _answer = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@main.route('/api/runnable-com-users')
def runnable():
    r = requests.get('https://api.github.com/users/runnable')
    return jsonify(r.json())


@main.route('/isready')
@main.route('/isReady')
@main.route('/IsReady')
def is_ready():
    return 'isReady'


@main.route('/isalive')
@main.route('/isAlive')
@main.route('/IsAlive')
def is_alive():
    return 'isAlive'
