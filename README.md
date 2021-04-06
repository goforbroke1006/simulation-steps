# simulation-steps


### How to use in your project

```bash
python3 -m pip install \
  -e git+https://github.com/goforbroke1006/simulationsteps.git@0.0.13#egg=simulationsteps
pip freeze > requirements.txt
```

##### ./features/environment.py

```python
from simulationsteps.utils import patch_context
from simulationsteps.validators import fields_exists


def before_all(context):
    """

    :type context: behave.runner.Context
    :return:
    """

    validators = {
        'data-bus': lambda t: fields_exists(t, 'host', 'port', 'consumer')
    }
    patch_context(context,
                  config_filename='config.json',
                  custom_validators_fn=validators)

    pass
```