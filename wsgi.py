import uuid

import requests
from flask import Flask
from flask import abort
from flask import jsonify
from flask import render_template
from flask import request
from markupsafe import escape
from pymongo import MongoClient


def is_valid_uuid4(value):
    """
    Check if value is a UUID version 4 string

    :param value: to be checked, e.g. '74751363-3db2-4a82-b764-09de11b65cd6'
    :type value: str

    :rtype: Boolean
    :return: True or False
    """

    try:
        _rv = uuid.UUID(str(value))

        if _rv.version == 4:
            return True
        else:
            return False
    except ValueError:
        return False


application = Flask(__name__, instance_relative_config=True)
# flask config: https://flask.palletsprojects.com/en/2.2.x/config/
application.config['TESTING'] = True

# clean-up: https://pymongo.readthedocs.io/en/stable/examples/authentication.html
application.config["MONGO_URI"] = "mongodb://root:example@mongo:27017"
application.config["MONGO_DB"] = "flask"
_client = MongoClient(application.config["MONGO_URI"])
_db = _client[application.config["MONGO_DB"]]


@application.route('/')
def index():
    return render_template("index.html")


@application.route('/question1')
def question1():
    # "name": "quizA"
    _quiz = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df"
    # "name": "quizB"
    # _quiz = "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86"
    # "name": "quizC"
    # _quiz = "QIZ-74751363-3db2-4a82-b764-09de11b65cd6"

    _collection = _db.quizzes
    # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
    _dict = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
    if _dict:
        return render_template("question1.html", data=_dict["data"])  # need data array
    return jsonify(_dict), 200


@application.route('/data')
def pirate():
    return render_template("deutsch.json")


@application.route('/flexquestion')
def flexquestion():
    # TODO: 2022-10-12T11:11:53 remove because it does not use the data
    # "name": "quizA"
    _quiz = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df"
    # "name": "quizB"
    # _quiz = "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86"
    # "name": "quizC"
    # _quiz = "QIZ-74751363-3db2-4a82-b764-09de11b65cd6"

    _collection = _db.quizzes
    # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
    _dict = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
    if _dict:
        return render_template("flexquestion.html", data=_dict["data"])  # need data array
    return jsonify(_dict), 200


@application.route('/formgrid', methods=['GET', 'POST'])
def formgrid():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        # "name": "quizA"
        # _quiz = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df"
        # "name": "quizB"
        _quiz = "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86"
        # "name": "quizC"
        # _quiz = "QIZ-74751363-3db2-4a82-b764-09de11b65cd6"

        _collection = _db.quizzes
        # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
        _dict = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
        if _dict:
            return render_template("formgrid.html", data=_dict["data"])  # need data array
        return jsonify(_dict), 200


@application.route('/nouns-table-result')
def nouns_table_result():
    return render_template("nouns-table-result.html")


@application.route('/quiz', methods=['GET', 'POST'])
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
            _question_ans = _db.questions.find_one({'quid': _request_values['quid']},
                                                   {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1,
                                                    'data': {'Label': 1, 'Noun': 1, 'Ans': 1, 'Plural': 1}})
            _question_ans_data = _question_ans['data']

            # Extract _quiz ('qzid') corresponding to _request_values['gzid']
            _quiz = _db.quizzes.find_one({'qzid': _request_values['qzid']},
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

            # return jsonify(_quiz), 200

            # _quiz = {
            #  "cif": "CIF-919ae5a5-34e4-4b88-979a-5187d46d1617",
            #  "quid": "QID-ba88f889-37d3-41ec-8829-d7ea2a45c61c",
            #  "qzid": "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86",
            #  "name": "quizB",
            #  "data": [
            #    {"Ans": "die", "Choice": "der", "Correct": "n", "Desc": "Stamp", "Label": "Q01", "Noun": "Briefemarke",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Briefmarken"},
            #    {"Ans": "die", "Choice": "die", "Correct": "y", "Desc": "Bill, Invoice", "Label": "Q02",
            #     "Noun": "Rechnung", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Rechnungen"},
            #    {"Ans": "das", "Choice": "das", "Correct": "y", "Desc": "Telephone", "Label": "Q03", "Noun": "Telefon",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Telefone"},
            #    {"Ans": "das", "Choice": "die", "Correct": "n", "Desc": "Form", "Label": "Q04", "Noun": "Forumlar",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Formulare"},
            #    {"Ans": "der", "Choice": "die", "Correct": "n", "Desc": "Printer", "Label": "Q05", "Noun": "Drucker",
            #     "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Drucker"}
            #  ]
            # }
            _meta_data = {'name': _quiz['name'], 'cif': _quiz['cif'].replace('CIF-', ''),
                          'quid': _quiz['quid'].replace('QID-', ''), 'qzid': _quiz['qzid'].replace('QIZ-', '')}

            return render_template("nouns-table-result.html", data=_quiz["data"], meta_data=_meta_data)
            return render_template("nouns-form-result.html", data=_quiz["data"], meta_data=_meta_data)

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

        _collection = _db.quizzes
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


@application.route('/formgrid2', methods=['GET', 'POST'])
def formgrid2():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        # "name": "quizA"
        # _quiz = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df"
        # "name": "quizB"
        _quiz = "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86"
        # "name": "quizC"
        # _quiz = "QIZ-74751363-3db2-4a82-b764-09de11b65cd6"

        _collection = _db.quizzes
        # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
        _dict = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
        if _dict:
            return render_template("formgrid2.html", data=_dict["data"])  # need data array
        return jsonify(_dict), 200


@application.route('/radiobutton')
def radiobutton():
    # "name": "quizA"
    # _quiz = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df"
    # "name": "quizB"
    _quiz = "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86"
    # "name": "quizC"
    # _quiz = "QIZ-74751363-3db2-4a82-b764-09de11b65cd6"

    _collection = _db.quizzes
    # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
    _dict = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
    if _dict:
        return render_template("radiobutton.html", data=_dict["data"])  # need data array
    return jsonify(_dict), 200


# allow both GET and POST requests
@application.route('/form-example', methods=['GET', 'POST'])
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
@application.route('/json-echo', methods=['POST'])
def json_echo():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    data = request.get_json()
    return jsonify(data), 200


@application.route('/json-form', methods=['GET', 'POST'])
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
@application.route('/api/questions')
def get_questions():
    _collection = _db.questions
    _answer = []
    for doc in _collection.find({}, {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1}):
        _answer.append(doc)

    return jsonify(_answer), 200


@application.route('/api/quizzes')
def get_quizzes():
    _collection = _db.quizzes
    _answer = []
    for doc in _collection.find({}, {'_id': 0, 'cif': 1, 'qzid': 1, 'quid': 1, 'name': 1}):
        _answer.append(doc)

    return jsonify(_answer), 200


@application.route('/api/mongo')
def get_mongodb_collections():
    _answer = _db.list_collection_names()
    return jsonify(_answer), 200


# @application.route('/api/user/<username>/')
# redirects to URL with trailing '/', search engines will index twice
# https://flask.palletsprojects.com/en/2.1.x/quickstart/#unique-urls-redirection-behavior
@application.route('/api/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'


# Needs trailing '/' to accept because URL is not unique
@application.route('/api/question/<cif>/<quid>/')
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
    _collection = _db.questions
    _answer = _collection.find_one({'quid': _question_id}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@application.route('/api/question/<quid>')
def get_quid_json(quid):
    # QID-05db84d8-27ac-4067-9daa-d743ff56929b - questions/05db84d8-27ac-4067-9daa-d743ff56929b
    _quid = escape(quid)

    if not is_valid_uuid4(_quid):
        _json_error = {'message': 'invalid question_id', 'code': 404, 'value': _quid}
        return jsonify(_json_error), 404

    _question_id = 'QID-' + _quid
    _collection = _db.questions
    _answer = _collection.find_one({'quid': _question_id}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


# Needs trailing '/' to accept because URL is not unique
@application.route('/api/quiz/<cif>/<quiz_id>/')
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
    _collection = _db.quizzes
    _answer = _collection.find_one({'cif': _cif, 'qzid': _quiz}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@application.route('/api/quiz/<quiz_id>')
def get_qzid_json(quiz_id):
    _quiz_id = escape(quiz_id)

    if not is_valid_uuid4(_quiz_id):
        _json_error = {'message': 'invalid quiz_id', 'code': 404, 'value': _quiz_id}
        return jsonify(_json_error), 404

    _quiz = 'QIZ-' + _quiz_id
    _collection = _db.quizzes
    _answer = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@application.route('/api/runnable')
def runnable():
    r = requests.get('https://api.github.com/users/runnable')
    return jsonify(r.json())


@application.route('/isready')
@application.route('/isReady')
@application.route('/IsReady')
def is_ready():
    return 'isReady'


@application.route('/isalive')
@application.route('/isAlive')
@application.route('/IsAlive')
def is_alive():
    return 'isAlive'


if __name__ == "__main__":
    application.run()
