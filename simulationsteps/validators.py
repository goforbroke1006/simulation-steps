def validate_postgres(target):
    """

    :param target:
    :return: bool
    """

    fields_exists(target, 'host', 'port', 'name', 'user', 'password')

    pass


def validate_redis(target):
    """

    :param target:
    :return: bool
    """

    fields_exists(target, 'host', 'port', 'db', 'password')

    pass


def validate_openapi(target):
    """

    :param target:
    :return: bool
    """

    fields_exists(target, 'url', )

    pass


def fields_exists(target, *fields):
    for f in fields:
        assert f in target['config'], \
            f'target "{target["name"]}", field "{f}" should be defined'
    pass
