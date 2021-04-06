import subprocess

from behave import *

from simulationsteps.utils import read_process

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

    shell = f'redis-cli -h {target_config["host"]} -p {target_config["port"]} -a {target_config["password"]} {command}'
    print(f'$ {shell}')

    process = subprocess.Popen(shell, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = read_process(process)
    process.wait()
    assert process.returncode == 0, f'Unexpected code {process.returncode}, stderr: {stderr}'

    print(f'# {stdout}')


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

    print(f'{stdout}')

    assert len(stdout.splitlines()) > 0, f'any key not found'
