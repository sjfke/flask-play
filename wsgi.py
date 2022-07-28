from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import requests
import os

application = Flask(__name__, instance_relative_config=True)


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


@application.route('/formgrid')
def formgrid():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("formgrid.html", data=data)


@application.route('/dropdown')
def dropdown():
    data = [
        {"Noun": "Laptop", "Ans": "der", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Laptops",
         "Desc": "Laptop"},
        {"Noun": "E-Mail", "Ans": "die", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "E-Mails",
         "Desc": "EMail"},
        {"Noun": "Handy", "Ans": "das", "Opt1": "der", "Opt2": "die", "Opt3": "das", "Plural": "Handys",
         "Desc": "CellPhone"}
    ]

    return render_template("dropdown.html", data=data)


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
