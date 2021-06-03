import subprocess

from behave import *

from simulationsteps.utils import read_process, json_has_subset

use_step_matcher("parse")


@step('postgres "{config_name}" command')
def postgres_command_step_impl(context, config_name):
    """
    :type context: behave.runner.Context
    :param config_name: string
    """

    # config_name = config_name.strip('"')

    target_config = context.simulation.targets['postgres'][config_name]
    if target_config is None:
        raise Exception(f'target {config_name} not found')

    sql = context.text
    sql = sql.replace('"', '\\"')

    shell = f'PGPASSWORD="{target_config["password"]}" ' \
            f'psql -h {target_config["host"]} -p {target_config["port"]} ' \
            f'-U {target_config["user"]} ' \
            f'-d {target_config["name"]} ' \
            f'-c "{sql}"'
    print(f'$ {shell}')

    process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = read_process(process)
    process.wait()
    assert process.returncode == 0, f'Unexpected code {process.returncode}, stderr: {stderr}'

    print(f'# {stdout}')


@then('postgres "{config_name}" command return {count:d} rows')
def postgres_assets_command_return_certain_count_step_impl(context, config_name, count):
    """
    :type context: behave.runner.Context
    :type config_name: str
    :type count: int
    """

    target_config = context.simulation.targets['postgres'][config_name]
    if target_config is None:
        raise Exception(f'target {config_name} not found')

    sql = context.text

    shell = f'PGPASSWORD="{target_config["password"]}" ' \
            f'psql -h {target_config["host"]} -p {target_config["port"]} ' \
            f'-U {target_config["user"]} ' \
            f'-d {target_config["name"]} ' \
            f'-c "{sql}"'
    print(f'$ {shell}')

    process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = read_process(process)
    process.wait()
    assert process.returncode == 0, f'Unexpected code {process.returncode}, stderr: {stderr}'

    print(stdout)

    output_lines_count = len(stdout.splitlines())
    tuples_count = output_lines_count - 1 - 1 - 1 - 1  # minus headers, delimiter, status line, last empty line
    assert tuples_count == count, f'wrong rows count returned, expect {count}, actual {tuples_count}'


@step('redis "{config_name}" command "{command}"')
def redis_command_step_impl(context, config_name, command):
    """
    :type context: behave.runner.Context
    :type config_name: str
    :type command: str
    """

    target_config = context.simulation.targets['redis'][config_name]
    if target_config is None:
        raise Exception(f'target {config_name} not found')

    shell = f'redis-cli -h {target_config["host"]} -p {target_config["port"]} -a \'{target_config["password"]}\' {command}'
    print(f'$ {shell}')

    process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = read_process(process)
    process.wait()
    assert process.returncode == 0, f'Unexpected code {process.returncode}, stderr: {stderr}'

    print(stdout)


@then('redis "{config_name}" KEYS {pattern}')
def redis_assert_keys_exists(context, config_name, pattern):
    """

    :type context: behave.runner.Context
    :type config_name: str
    :type pattern: str
    :return:
    """

    target_config = context.simulation.targets['redis'][config_name]
    if target_config is None:
        raise Exception(f'target {config_name} not found')

    shell = f'redis-cli ' \
            f'-h {target_config["host"]} -p {target_config["port"]} ' \
            f'-a {target_config["password"]} ' \
            f'KEYS \'{pattern}\''
    print(f'$ {shell}')

    process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = read_process(process)
    process.wait()
    assert process.returncode == 0, f'Unexpected code {process.returncode}, stderr: {stderr}'

    print(stdout)

    assert len(stdout.splitlines()) > 0, f'any key not found'


@step('openapi "{config_name}" request [{method}] "{uri}" with "{body}" body, response contains')
def openapi_assert_response_contains_data(context, config_name, method, uri, body):
    """

    :type context: behave.runner.Context
    :type config_name: str
    :type method: str
    :type uri: str
    :type body: str
    :return:
    """

    target_config = context.simulation.targets['openapi'][config_name]
    if target_config is None:
        raise Exception(f'target {config_name} not found')

    expected_resp = context.text
    method = method.upper()
    base_url = target_config["url"]
    full_url = base_url + uri

    shell = f'curl -H "Content-Type: application/json" -X {method} {full_url} --data "{body}"'
    print(f'$ {shell}')

    process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = read_process(process)
    process.wait()
    assert process.returncode == 0, f'Unexpected code {process.returncode}, stderr: {stderr}'

    print(stdout)

    assert json_has_subset(stdout, expected_resp), f'response {stdout} is not contains {expected_resp}'

    pass
