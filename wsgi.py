import uuid
import requests
from flask import Flask
from flask import json
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
_client = MongoClient(application.config["MONGO_URI"])
_db = _client.flask


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
    # return jsonify(_dict), 200
    return render_template("question1.html", data=_dict["data"])  # need data array


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
    # return jsonify(_dict), 200
    return render_template("flexquestion.html", data=_dict["data"])  # need data array


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
        # return jsonify(_dict), 200
        return render_template("formgrid.html", data=_dict["data"])  # need data array


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
        # return jsonify(_dict), 200
        return render_template("formgrid2.html", data=_dict["data"])  # need data array


@application.route('/radiobutton')
def radiobutton():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("radiobutton.html", data=data)


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
@application.route('/mongo')
def mongo():
    # db = client.flask
    # _answer = _db.list_collection_names()
    _collection = _db.quizzes
    _answer = _collection.find_one({}, {'_id': 0})
    # _answer = _collection.find_one({}, {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1})
    # _answer = _collection.find_one({'data': {'$elemMatch': {"Noun": "Bleistift"}}},
    #                              {'_id': 0, 'cif': 1, 'quid': 1, 'name': 1})
    return jsonify(_answer), 200


@application.route('/user/<username>')
def show_user_profile(username):
    return f'User {escape(username)}'


@application.route('/questions/<cif>/<quid>')
def show_cif_quid(cif, quid):
    # QID-05db84d8-27ac-4067-9daa-d743ff56929b - questions/05db84d8-27ac-4067-9daa-d743ff56929b
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


@application.route('/questions/<quid>')
def show_quid(quid):
    # QID-05db84d8-27ac-4067-9daa-d743ff56929b - questions/05db84d8-27ac-4067-9daa-d743ff56929b
    _quid = escape(quid)

    if not is_valid_uuid4(_quid):
        _json_error = {'message': 'invalid question_id', 'code': 404, 'value': _quid}
        return jsonify(_json_error), 404

    _question_id = 'QID-' + _quid
    _collection = _db.questions
    _answer = _collection.find_one({'quid': _question_id}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@application.route('/quiz/<cif>/<quiz_id>')
def return_cif_qzid_data(cif, quiz_id):
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


@application.route('/quiz/<quiz_id>')
def return_qzid_data(quiz_id):
    _quiz_id = escape(quiz_id)

    if not is_valid_uuid4(_quiz_id):
        _json_error = {'message': 'invalid quiz_id', 'code': 404, 'value': _quiz_id}
        return jsonify(_json_error), 404

    _quiz = 'QIZ-' + _quiz_id
    _collection = _db.quizzes
    _answer = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
    return jsonify(_answer), 200


@application.route('/api')
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
