import uuid
# https://www.delftstack.com/howto/python/static-class-python/


def get_new_uuid4():
    """
    Generate a brand new uuid4 identifier

    :return: uuid4 identifier, e.g. 'e0e2d8ce-d00e-432b-b87e-8920b187462e'
    :rtype: str
    """
    return str(uuid.uuid4())


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


def sanitize_cif(cif, prefix=True):
    """
    Clean-up CIF, strip 'CIF-' for UUID check, adds 'CIF-' for MongoDB search (prefix=True)

    :param cif: to be sanitized, e.g. '74751363-3db2-4a82-b764-09de11b65cd6', optional 'cif-', 'CIF-' prefix
    :type cif: str

    :param prefix: has 'CIF-' prefix (mongodb) or not (mariadb)
    :type prefix: bool

    :rtype: str
    :return: 'CIF-<uuid>', '<uuid>' or None
    """

    _uuid = cif.lower()
    if cif.lower().startswith('cif-'):
        _uuid = cif.split('-', 1)[1]

    if is_valid_uuid4(_uuid):
        if prefix:
            return f"CIF-{_uuid}"
        else:
            return f"{_uuid}"
    else:
        return None


def sanitize_quid(quid, prefix=True):
    """
    Clean-up QID, strip 'QID-' for UUID check, adds 'QID-' for MongoDB search (prefix=True)

    :param quid: to be sanitized, e.g. '74751363-3db2-4a82-b764-09de11b65cd6', optional 'qid-', 'QID-' prefix
    :type quid: str

    :param prefix: has 'QID-' prefix (mongodb) or not (mariadb)
    :type prefix: bool

    :rtype: str
    :return: 'QID-<uuid>', '<uuid>' or None
    """
    _uuid = quid.lower()
    if quid.lower().startswith('qid-'):
        _uuid = quid.split('-', 1)[1]

    if is_valid_uuid4(_uuid):
        if prefix:
            return f"QID-{_uuid}"
        else:
            return f"{_uuid}"
    else:
        return None


def sanitize_qzid(qzid, prefix=True):
    """
    Clean-up QIZ, strip 'QIZ-' for UUID check, adds 'QIZ-' for MongoDB search (prefix=True)

    :param qzid: to be sanitized, e.g. '74751363-3db2-4a82-b764-09de11b65cd6', optional 'qiz-', 'QIZ-' prefix
    :type qzid: str

    :param prefix: has 'QIZ-' prefix (mongodb) or not (mariadb)
    :type prefix: bool

    :rtype: str
    :return: 'QIZ-<uuid>', '<uuid>' or None
    """

    _uuid = qzid.lower()
    if qzid.lower().startswith('qiz-'):
        _uuid = qzid.split('-', 1)[1]

    if is_valid_uuid4(_uuid):
        if prefix:
            return f"QIZ-{_uuid}"
        else:
            return f"{_uuid}"
    else:
        return None
