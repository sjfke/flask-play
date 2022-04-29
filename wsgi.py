from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import requests

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
# JSON
# {
#     "language" : "Python",
#     "framework" : "Flask",
#     "website" : "Scotch",
#     "version_info" : {
#         "python" : "3.9.0",
#         "flask" : "1.1.2"
#     },
#     "examples" : ["query", "form", "json"],
#     "boolean_test" : true
# }
@application.route('/json-example', methods=['POST'])
def json_example():
    request_data = request.get_json()

    language = request_data['language']
    framework = request_data['framework']

    # two keys are needed because of the nested object
    python_version = request_data['version_info']['python']

    # an index is needed because of the array
    example = request_data['examples'][0]

    boolean_test = request_data['boolean_test']

    return '''
           The language value is: {}
           The framework value is: {}
           The Python version is: {}
           The item at index 0 in the example list is: {}
           The boolean value is: {}'''.format(language, framework, python_version, example, boolean_test)


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
