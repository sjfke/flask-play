import uuid
from enum import Enum

import requests
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, abort, session
from flask_bootstrap import Bootstrap5, SwitchField
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from flask_babel import Babel
from markupsafe import Markup, escape
from pymongo import MongoClient
from wtforms.fields import *
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, InputRequired, ReadOnly, Disabled


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

# python -c 'import uuid; print(uuid.uuid4().hex)'
# python -c 'import secrets; print(secrets.token_hex())'
# python  -c 'import os; print(os.urandom(16).hex())'
HEX_SECRET_KEY = 'cad2d4ec59b74b9ab55a57cd8df4763b'
application.secret_key = HEX_SECRET_KEY
# application.config['SECRET_KEY'] = HEX_SECRET_KEY # configuration alternative
# from os import urandom
# application.secret_key = urandom(16).hex()
# application.secret_key = 'dev'
application.config['SESSION_COOKIE_NAME'] = 'flask-play'  # default 'session'

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Use local bootstrap files not CDN
application.config['BOOTSTRAP_SERVE_LOCAL'] = True

# set default button style and size, will be overwritten by macro parameters
application.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
application.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

# set default icon title of table actions
application.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
application.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
application.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
application.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

# application.config['WTF_CSRF_SECRET_KEY'] = 'bb5951a47f9442b8a3077f44f6a9b202'  # Defaults to session SECRET_KEY

# clean-up: https://pymongo.readthedocs.io/en/stable/examples/authentication.html
application.config["MONGO_URI"] = "mongodb://root:example@mongo:27017"
application.config["MONGO_DB"] = "flask"
_client = MongoClient(application.config["MONGO_URI"])
_db = _client[application.config["MONGO_DB"]]

bootstrap = Bootstrap5(application)
db = SQLAlchemy(application)
csrf = CSRFProtect(application)
babel = Babel(application)


class ExampleForm(FlaskForm):
    """An example form that contains all the supported bootstrap style form fields."""
    date = DateField(description="We'll never share your email with anyone else.")  # add help text with `description`
    datetime = DateTimeField(render_kw={'placeholder': 'this is a placeholder'})  # add HTML attribute with `render_kw`
    datetime_local = DateTimeLocalField()
    time = TimeField()
    month = MonthField()
    color = ColorField()
    floating = FloatField()
    integer = IntegerField()
    decimal_slider = DecimalRangeField()
    integer_slider = IntegerRangeField(render_kw={'min': '0', 'max': '4'})
    email = EmailField()
    url = URLField()
    telephone = TelField()
    image = FileField(render_kw={'class': 'my-class'}, validators=[Regexp('.+\.jpg$')])  # add your class
    option = RadioField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select = SelectField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select_multiple = SelectMultipleField(
        choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    bio = TextAreaField()
    search = SearchField()  # will autocapitalize on mobile
    title = StringField()  # will not autocapitalize on mobile
    secret = PasswordField()
    remember = BooleanField('Remember me')
    submit = SubmitField()


class HelloForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField('Remember me')
    submit = SubmitField()


class ButtonForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    confirm = SwitchField('Confirmation')
    submit = SubmitField()
    delete = SubmitField()
    cancel = SubmitField()


class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code/Exchange')
    number = StringField('Number')


class IMForm(FlaskForm):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = StringField()


class ContactForm(FlaskForm):
    first_name = StringField()
    last_name = StringField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)
    emails = FieldList(StringField("Email"), min_entries=3)
    im_accounts = FieldList(FormField(IMForm), min_entries=2)


class BootswatchForm(FlaskForm):
    """Form to test Bootswatch."""
    # DO NOT EDIT! Use list-bootswatch.py to generate the Radiofield below.
    theme_name = RadioField(
        default='default',
        choices=[
            ('default', 'none'),
            ('cerulean', 'Cerulean 5.3.1'),
            ('cosmo', 'Cosmo 5.3.1'),
            ('cyborg', 'Cyborg 5.3.1'),
            ('darkly', 'Darkly 5.3.1'),
            ('flatly', 'Flatly 5.3.1'),
            ('journal', 'Journal 5.3.1'),
            ('litera', 'Litera 5.3.1'),
            ('lumen', 'Lumen 5.3.1'),
            ('lux', 'Lux 5.3.1'),
            ('materia', 'Materia 5.3.1'),
            ('minty', 'Minty 5.3.1'),
            ('morph', 'Morph 5.3.1'),
            ('pulse', 'Pulse 5.3.1'),
            ('quartz', 'Quartz 5.3.1'),
            ('sandstone', 'Sandstone 5.3.1'),
            ('simplex', 'Simplex 5.3.1'),
            ('sketchy', 'Sketchy 5.3.1'),
            ('slate', 'Slate 5.3.1'),
            ('solar', 'Solar 5.3.1'),
            ('spacelab', 'Spacelab 5.3.1'),
            ('superhero', 'Superhero 5.3.1'),
            ('united', 'United 5.3.1'),
            ('vapor', 'Vapor 5.3.1'),
            ('yeti', 'Yeti 5.3.1'),
            ('zephyr', 'Zephyr 5.3.1'),
        ]
    )
    submit = SubmitField()


class MyCategory(Enum):
    CAT1 = 'Category 1'
    CAT2 = 'Category 2'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum(MyCategory), default=MyCategory.CAT1, nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    create_time = db.Column(db.Integer, nullable=False, unique=True)


with application.app_context():
    db.drop_all()
    db.create_all()
    for i in range(20):
        url = 'mailto:x@t.me'
        if i % 7 == 0:
            url = 'www.t.me'
        elif i % 7 == 1:
            url = 'https://t.me'
        elif i % 7 == 2:
            url = 'http://t.me'
        elif i % 7 == 3:
            url = 'http://t'
        elif i % 7 == 4:
            url = 'http://'
        elif i % 7 == 5:
            url = 'x@t.me'
        m = Message(
            text=f'Message {i + 1} {url}',
            author=f'Author {i + 1}',
            create_time=4321 * (i + 1)
        )
        if i % 2:
            m.category = MyCategory.CAT2
        if i % 4:
            m.draft = True
        db.session.add(m)
    db.session.commit()


class RegistrationForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(6, 35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), Length(8, 150), EqualTo('password')])
    remember = BooleanField('Remember me')
    accept_tos = BooleanField('I accept the TOS', validators=[InputRequired()])
    submit = SubmitField()



@application.route('/')
def index():
    return render_template('index.html')


@application.route('/form', methods=['GET', 'POST'])
def test_form():
    _form = HelloForm()
    if _form.validate_on_submit():
        flash('Form validated!')
        return redirect(url_for('index'))
    return render_template(
        'form.html',
        form=_form,
        telephone_form=TelephoneForm(),
        contact_form=ContactForm(),
        im_form=IMForm(),
        button_form=ButtonForm(),
        example_form=ExampleForm()
    )


@application.route('/nav', methods=['GET', 'POST'])
def test_nav():
    return render_template('nav.html')


@application.route('/bootswatch', methods=['GET', 'POST'])
def test_bootswatch():
    _form = BootswatchForm()
    if _form.validate_on_submit():
        if _form.theme_name.data == 'default':
            application.config['BOOTSTRAP_BOOTSWATCH_THEME'] = None
        else:
            application.config['BOOTSTRAP_BOOTSWATCH_THEME'] = _form.theme_name.data
        flash(f'Render style has been set to {_form.theme_name.data}.')
    else:
        if application.config['BOOTSTRAP_BOOTSWATCH_THEME'] is not None:
            _form.theme_name.data = application.config['BOOTSTRAP_BOOTSWATCH_THEME']
    return render_template('bootswatch.html', form=_form)


@application.route('/pagination', methods=['GET', 'POST'])
def test_pagination():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page=page, per_page=10)
    messages = pagination.items
    return render_template('pagination.html', pagination=pagination, messages=messages)


@application.route('/flash', methods=['GET', 'POST'])
def test_flash():
    flash('A simple default alert—check it out!')
    flash('A simple primary alert—check it out!', 'primary')
    flash('A simple secondary alert—check it out!', 'secondary')
    flash('A simple success alert—check it out!', 'success')
    flash('A simple danger alert—check it out!', 'danger')
    flash('A simple warning alert—check it out!', 'warning')
    flash('A simple info alert—check it out!', 'info')
    flash('A simple light alert—check it out!', 'light')
    flash('A simple dark alert—check it out!', 'dark')
    flash(Markup(
        'A simple success alert with <a href="#" class="alert-link">an example link</a>. Give it a click if you like.'),
        'success')
    return render_template('flash.html')


@application.route('/table')
def test_table():
    page = request.args.get('page', 1, type=int)
    pagination = Message.query.paginate(page=page, per_page=10)
    messages = pagination.items
    titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('draft', 'Draft'),
              ('create_time', 'Create Time')]
    data = []
    for msg in messages:
        data.append({'id': msg.id, 'text': msg.text, 'author': msg.author, 'category': msg.category, 'draft': msg.draft,
                     'create_time': msg.create_time})
    return render_template('table.html', messages=messages, titles=titles, Message=Message, data=data)


@application.route('/table/<int:message_id>/view')
def view_message(message_id):
    message = Message.query.get(message_id)
    if message:
        return f'Viewing {message_id} with text "{message.text}". Return to <a href="/table">table</a>.'
    return f'Could not view message {message_id} as it does not exist. Return to <a href="/table">table</a>.'


@application.route('/table/<int:message_id>/edit')
def edit_message(message_id):
    message = Message.query.get(message_id)
    if message:
        message.draft = not message.draft
        db.session.commit()
        return f'Message {message_id} has been edited by toggling draft status. Return to <a href="/table">table</a>.'
    return f'Message {message_id} did not exist and could therefore not be edited. Return to <a href="/table">table</a>.'


@application.route('/table/<int:message_id>/delete', methods=['POST'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return f'Message {message_id} has been deleted. Return to <a href="/table">table</a>.'
    return f'Message {message_id} did not exist and could therefore not be deleted. Return to <a href="/table">table</a>.'


@application.route('/table/<int:message_id>/like')
def like_message(message_id):
    return f'Liked the message {message_id}. Return to <a href="/table">table</a>.'


@application.route('/table/new-message')
def new_message():
    return 'Here is the new message page. Return to <a href="/table">table</a>.'


@application.route('/icon')
def test_icon():
    return render_template('icon.html')


@application.route('/icons')
def test_icons():
    return render_template('icons.html')


####

@application.route('/flask-config')
def flask_config():
    """
    Automatically generated list of Flask configuration values

    :rtype: str
    :return: Flask Configuration or None
    """

    # https://flask.palletsprojects.com/en/latest/config/#builtin-configuration-values
    # need to convert 'value' to string for JSON and organize
    _flask_cfg = {}
    _bootstrap_cfg = {}
    _wtf_cfg = {}
    _database_cfg = {}
    for key, value in application.config.items():
        if key.startswith('BOOTSTRAP'):
            _bootstrap_cfg[key] = str(value)
        elif key.startswith('WTF'):
            _wtf_cfg[key] = str(value)
        elif key.startswith('MONGO') or key.startswith('SQLALCHEMY'):
            _database_cfg[key] = str(value)
        else:
            _flask_cfg[key] = str(value)

    _flask_config = {'Flask': _flask_cfg, 'Bootstrap': _bootstrap_cfg, 'WTF': _wtf_cfg, 'Database': _database_cfg}

    return jsonify(_flask_config), 200


@application.route('/login', methods=['GET', 'POST'])
def login():
    # https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY
    if request.method == 'POST':
        data = request.form
        # return jsonify(data), 200
        session['username'] = request.form['username']
        session['cif'] = '919ae5a5-34e4-4b88-979a-5187d46d1617'
        session['theme'] = 'hootstrap'  # 'hootstrap', 'fresca', 'herbie'
        return redirect(url_for('index'))
    else:
        return render_template("old-registration.html")


@application.route('/registration', methods=['GET', 'POST'])
def registration():
    _form = RegistrationForm()
    # https://flask.palletsprojects.com/en/2.2.x/config/#SECRET_KEY
    if _form.validate_on_submit():
        data = request.form
        return jsonify(data), 200
        # session['username'] = request.form['username']
        # session['cif'] = '919ae5a5-34e4-4b88-979a-5187d46d1617'
        # session['theme'] = 'hootstrap'  # 'hootstrap', 'fresca', 'herbie'
        # return redirect(url_for('index'))
    else:
        return render_template('registration.html', form=_form, action='/registration', method='post')


@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@application.route('/question-form', methods=['GET', 'POST'])
def question_form():

    _choices = [('der', 'der'), ('die', 'die'), ('das', 'das')]
    _noun = ['Maus', 'Computer', 'Stift', 'Kalendar']
    _description = ['Mouse', 'Computer', 'Pencil', 'Calendar']
    _question = ['Q01', 'Q02', 'Q03', 'Q04']
    _max = 1

    class QuestionForm(FlaskForm):
        select0 = SelectField('Choice',choices=[('', '')] + _choices, validators=[DataRequired()])
        question0 = StringField("Question", default=_question[0], validators=[ReadOnly()])
        noun0 = StringField("Noun", default=_noun[0], validators=[ReadOnly()])
        description0 = StringField("Description", default=_description[0], validators=[ReadOnly()])
        select1 = SelectField('Choice',choices=[('', '')] + _choices, validators=[DataRequired()])
        question1 = StringField("Question", default=_question[1], validators=[ReadOnly()])
        noun1 = StringField("Noun", default=_noun[1], validators=[ReadOnly()])
        description1 = StringField("Description", default=_description[1], validators=[ReadOnly()])
        select3 = SelectField('Choice',choices=[('', '')] + _choices, validators=[DataRequired()])
        question3 = StringField("Question", default=_question[3], validators=[ReadOnly()])
        noun3 = StringField("Noun", default=_noun[3], validators=[ReadOnly()])
        description3 = StringField("Description", default=_description[3], validators=[ReadOnly()])
        submit = SubmitField()

    _form = QuestionForm()
    if _form.validate_on_submit():
        data = request.form
        return jsonify(data), 200
        # flash('Form validated!')
        # return redirect(url_for('index'))

    # _form.question = 'Q01'
    # _form.noun = 'Laptop'
    # _form.descr = 'Laptop'
    # {
    #     "Noun": "Laptop",
    #     "Ans": "der",
    #     "Opt1": "der",
    #     "Opt2": "die",
    #     "Opt3": "das",
    #     "Plural": "Laptops",
    #     "Desc": "Laptop"
    # },
    return render_template('question-form.html', form=_form, action='/question-form', method='post', max=_max)


@application.route('/question-table')
def question_table():
    # https://en.wikipedia.org/wiki/NATO_phonetic_alphabet

    # _quiz_name = "Quiz Alfa"
    # "name": "quizA"
    # _quiz = "QIZ-3021178c-c430-4285-bed2-114dfe4db9df"

    # _quiz_name = "Quiz Bravo"
    # "name": "quizB"
    # _quiz = "QIZ-d1e25109-ef1d-429c-9595-0fbf820ced86"

    _quiz_name = "Quiz Charlie"
    # "name": "quizC"
    _quiz = "QIZ-74751363-3db2-4a82-b764-09de11b65cd6"

    _collection = _db.quizzes
    # db.collection.find_one() returns a Dict: {"data": [{...},{...},{...}]}
    _dict = _collection.find_one({'qzid': _quiz}, {'_id': 0, 'data': 1})  # dictionary

    titles = [('label', 'Question'), ('opt1', 'Masculine'), ('opt2', 'Feminine'), ('opt3', 'Neuter'), ('noun', 'Noun'),
              ('desc', 'Desc')]
    data = []
    for _d in _dict['data']:
        data.append(
            {'label': _d['Label'], 'opt1': _d['Opt1'], 'opt2': _d['Opt2'], 'opt3': _d['Opt3'], 'noun': _d['Noun'],
             'desc': _d['Desc']})

    return render_template('question-table.html', titles=titles, data=data, quiz_name=_quiz_name)


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
    return render_template("nouns-result.html")


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
