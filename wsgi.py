import uuid

import requests
from flask import Flask
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


@application.route('/quiz', methods=['GET', 'POST'])
def get_quiz_form():
    if request.method == 'POST':
        _answer = request.form
        if _answer:
            return jsonify(_answer), 200
        return jsonify(_answer), 404

    else:
        _quiz_id = None
        try:
            _quiz_id = request.args.get('id', '')  # (key, default, type)
        except KeyError:
            f'Invalid key: need quiz "id"'

        # _quiz_id = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df", "name": "quizA"
        # _quiz_id = "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86", "name": "quizB"
        # _quiz_id = "QIZ-74751363-3db2-4a82-b764-09de11b65cd6", "name": "quizC"

        _collection = _db.quizzes
        # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
        _dict = _collection.find_one({'qzid': _quiz_id}, {'_id': 0, 'data': 1})

        if _dict:
            return render_template("quiz.html", data=_dict["data"])
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
def is_ready():
    return 'isReady'


@application.route('/isalive')
def is_alive():
    return 'isAlive'


if __name__ == "__main__":
    application.run()
