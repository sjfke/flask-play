import uuid
import requests
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from markupsafe import escape
from pymongo import MongoClient

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


@application.route('/data')
def pirate():
    return render_template("deutsch.json")


@application.route('/question1')
def question1():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("question1.html", data=data)


@application.route('/flexquestion')
def flexquestion():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("flexquestion.html", data=data)


@application.route('/formgrid', methods=['GET', 'POST'])
def formgrid():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        data = [
            {"Noun": "Laptop", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "Laptop"},
            {"Noun": "E-Mail", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "EMail"},
            {"Noun": "Handy", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "CellPhone"}
        ]
        return render_template("formgrid.html", data=data)


@application.route('/formgrid2', methods=['GET', 'POST'])
def formgrid2():
    if request.method == 'POST':
        answer = request.form
        # return data # => returns identical JSON output
        return jsonify(answer), 200
    else:
        data = [
            {"Noun": "Laptop", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "Laptop"},
            {"Noun": "E-Mail", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "EMail"},
            {"Noun": "Handy", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Desc": "CellPhone"}
        ]
        return render_template("formgrid2.html", data=data)


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


@application.route('/questions/<quid>')
def show_question_id(quid):
    # any/uuid return 404 if uuid is invalid # https://www.geeksforgeeks.org/python-404-error-handling-in-flask/
    # flask error handling: https://flask.palletsprojects.com/en/2.2.x/errorhandling/
    # QID-05db84d8-27ac-4067-9daa-d743ff56929b - questions/05db84d8-27ac-4067-9daa-d743ff56929b
    _quid = escape(quid)
    try:
        uuid.UUID(str(_quid))
        return f'Valid uuid{": " + _quid}'
    except ValueError:
        return f'Invalid uuid{escape(": " + quid)}'


@application.route('/quiz/<cif>/<quiz_id>')
def return_quiz_data(cif, quiz_id):
    # any/uuid return 404 if uuid is invalid # https://www.geeksforgeeks.org/python-404-error-handling-in-flask/
    # flask error handling: https://flask.palletsprojects.com/en/2.2.x/errorhandling/
    # /quiz: CIF=919ae5a5-34e4-4b88-979a-5187d46d1617 / QZID=74751363-3db2-4a82-b764-09de11b65cd6
    # QIZ-74751363-3db2-4a82-b764-09de11b65cd6 ('QIZ-' + QZID)
    # db.quizzes.find({"qzid":"QIZ-3021178c-c430-4285-bed2-114dfe4db9df"},{_id:0,data:1})
    _cif = escape(cif)
    _quiz_id = escape(quiz_id)
    try:
        uuid.UUID(str(_cif))
        uuid.UUID(str(_quiz_id))

        # TODO: perform CIF and QZID check
        _quiz = 'QIZ-' + _quiz_id
        _collection = _db.quizzes
        _answer = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})
        return jsonify(_answer), 200
    except ValueError:
        # TODO: return JSON 404
        return f'Invalid uuid{escape(": " + cif + ", " +  quiz_id)}'


@application.route('/api')
def runnable():
    r = requests.get('https://api.github.com/users/runnable')
    return jsonify(r.json())


@application.route('/isready')
def isready():
    return 'isReady'


@application.route('/isalive')
def isalive():
    return 'isAlive'


if __name__ == "__main__":
    application.run()
