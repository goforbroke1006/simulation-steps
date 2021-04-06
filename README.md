# simulation_steps


### How to use in your project

##### ./features/environment.py

```python
from features.misc.utils import patch_context
from features.misc.validators import fields_exists

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