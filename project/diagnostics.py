from flask import (
    Blueprint,
    current_app,
    jsonify,
)

diagnostics = Blueprint('diagnostics', __name__, static_folder='/static')


@diagnostics.route('/get-flask-config')
def get_flask_config():
    """
    Manually maintained list of Flask configuration values

    :rtype: str
    :return: Flask Configuration or None
    """

    # https://flask-docs-ja.readthedocs.io/en/latest/api/#flask.Config.get_namespace
    # https://flask.palletsprojects.com/en/stable/config/
    _config = {}
    # bad 'PERMANENT_'
    for _setting in ['PROPAGATE_', 'TRAP_', 'SECRET_', 'SESSION_', 'MAX_', 'TRAP_', 'SEND_', 'TRUSTED_', 'SERVER_',
                     'APPLICATION_', 'PREFERRED_', 'TEMPLATES_', 'EXPLAIN_', 'PROVIDE_', 'USE_', 'MONGO_']:
        _settings = current_app.config.get_namespace(_setting)
        for key, value in _settings.items():
            _config[f"{_setting}{key}".upper()] = value

    return jsonify(_config), 200


@diagnostics.route('/get-flask-variable/<prefix>')
def get_flask_variable(prefix=None):
    """
    Return Flask Environment variables with this prefix

    :rtype: str
    :return: Flask Configuration Variable
    """

    _config = {}
    # return f'{prefix} supplied'
    try:
        _settings = current_app.config.get_namespace(prefix)
        # return jsonify(_settings), 200
        if _settings == {}:
            _config[f"{prefix}"] = 'Not Found'
            return jsonify(_config), 400
        else:
            for key, value in _settings.items():
                _config[f"{prefix}{key}".upper()] = value
            return jsonify(_config), 200
    except ValueError:
        _config[f"{prefix}"] = 'ValueError'
        return jsonify(_config), 400
