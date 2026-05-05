## Variables

Variables are Airflow’s runtime configuration concept - a general key/value store that is global and can be queried from your tasks, and easily set via Airflow’s user interface, or bulk-uploaded as a JSON file.

To use them, just import and call get on the Variable model:

```
from airflow.sdk import Variable

# Normal call style
foo = Variable.get("foo")

# Auto-deserializes a JSON value
bar = Variable.get("bar", deserialize_json=True)

# Returns the value of default (None) if the variable is not set
baz = Variable.get("baz", default=None)
```

You can also access variables through the Task Context using get_current_context():

```
from airflow.sdk import get_current_context


def my_task():
    context = get_current_context()
    var = context["var"]
    my_variable = var["value"].get("my_variable_name")
    return my_variable
```

The context["var"] dictionary provides two ways to access variables:

var["value"]: returns the variable as a raw string value.

var["json"]: returns the variable as a JSON value. This is useful when the variable stores a dictionary, list, or other structured data.

```
# Raw value
echo {{ var.value.<variable_name> }}

# Auto-deserialize JSON value
echo {{ var.json.<variable_name> }}
```