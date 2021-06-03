import json

from simulationsteps.validators import validate_postgres, validate_redis


def patch_context(context, config_filename, custom_validators_fn: {}):
    """
    Append targets configs that imported from config file
    :type context: behave.runner.Context
    :type config_filename: str
    :type custom_validators_fn: dict
    :return: None
    """

    f = open(config_filename, "r")
    config = json.loads(f.read())

    context.simulation = type('', (), {})()
    context.simulation.targets = {}

    validators_fn = {
        'postgres': validate_postgres,
        'redis': validate_redis,
    }
    for cv_type in custom_validators_fn:
        validators_fn[cv_type] = custom_validators_fn[cv_type]

    for t in config['targets']:
        target_type = t['type']
        target_name = t['name']
        target_config = t['config']

        if target_type not in context.simulation.targets:
            context.simulation.targets[target_type] = {}

        if target_name in context.simulation.targets[target_type]:
            raise Exception(f'target {target_name} already exists')

        if target_type in validators_fn:
            validator = validators_fn[target_type]
            validator(t)
        else:
            raise Exception(f'can\'t fount validator for target type "{target_type}"')

        context.simulation.targets[target_type][target_name] = target_config
        print(f'{target_name} ({target_type}) loaded')

    pass


def read_process(process):
    stdout = ''
    stderr = ''

    for line in process.stdout:
        stdout += line.decode("utf-8")

    for line in process.stderr:
        stderr += line.decode("utf-8")

    return stdout, stderr


def json_has_subset(target, subset):
    def recursive_check_subset(a, b):
        for x in a:
            if not isinstance(a[x], dict):
                yield (x in b) and (a[x] == b[x])  # return a bool
            else:
                if x in b:
                    yield all(recursive_check_subset(a[x], b[x]))
                else:
                    yield False

    return all(recursive_check_subset(target, subset))
