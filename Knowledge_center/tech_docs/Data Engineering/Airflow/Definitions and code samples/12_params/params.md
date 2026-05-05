## Params

Params enable you to provide runtime configuration to tasks. You can configure default Params in your Dag code and supply additional Params, or overwrite Param values, at runtime when you trigger a Dag. Param values are validated with JSON Schema. For scheduled Dag runs, default Param values are used.

Also defined Params are used to render a nice UI when triggering manually. When you trigger a Dag manually, you can modify its Params before the Dag run starts. If the user-supplied values don’t pass validation, Airflow shows a warning instead of creating the Dag run.

---
### Dag-level Params
To add Params to a DAG, initialize it with the params kwarg. Use a dictionary that maps Param names to either a Param or an object indicating the parameter’s default value.

```
 from airflow.sdk import DAG, task, Param, get_current_context
 import logging

 with DAG(
     "the_dag",
     params={
         "x": Param(5, type="integer", minimum=3),
         "my_int_param": 6
     },
 ) as dag:

     @task.python
     def example_task():
         ctx = get_current_context()
         logger = logging.getLogger("airflow.task")

         # This will print the default value, 6:
         logger.info(ctx["dag"].params["my_int_param"])

         # This will print the manually-provided value, 42:
         logger.info(ctx["params"]["my_int_param"])

         # This will print the default value, 5, since it wasn't provided manually:
         logger.info(ctx["params"]["x"])

     example_task()

 if __name__ == "__main__":
     dag.test(
         run_conf={"my_int_param": 42}
     )
```

### Task-level Params

```
def print_my_int_param(params):
  print(params.my_int_param)

PythonOperator(
    task_id="print_my_int_param",
    params={"my_int_param": 10},
    python_callable=print_my_int_param,
)
```

Task-level params take precedence over Dag-level params, and user-supplied params (when triggering the Dag) take precedence over task-level params.

### Referencing Params in a Task
```
 PythonOperator(
     task_id="from_template",
     op_args=[
         "{{ params.my_int_param + 10 }}",
     ],
     python_callable=(
         lambda my_int_param: print(my_int_param)
     ),
 )

```

Another way to access your param is via a task’s context kwarg.

```
 def print_my_int_param(**context):
     print(context["params"]["my_int_param"])

 PythonOperator(
     task_id="print_my_int_param",
     python_callable=print_my_int_param,
     params={"my_int_param": 12345},
 )
```

---

```
with DAG(
    dag_id=Path(__file__).stem,
    dag_display_name="Params Trigger UI",
    description=__doc__.partition(".")[0],
    doc_md=__doc__,
    schedule=None,
    start_date=datetime.datetime(2022, 3, 4),
    catchup=False,
    tags=["example", "params"],
    params={
        "names": Param(
            ["Linda", "Martha", "Thomas"],
            type="array",
            description="Define the list of names for which greetings should be generated in the logs."
            " Please have one name per line.",
            title="Names to greet",
        ),
        "english": Param(True, type="boolean", title="English"),
        "german": Param(True, type="boolean", title="German (Formal)"),
        "french": Param(True, type="boolean", title="French"),
    },
) as dag:

    @task(task_id="get_names", task_display_name="Get names")
    def get_names(**kwargs) -> list[str]:
        params = kwargs["params"]
        if "names" not in params:
            print("Uuups, no names given, was no UI used to trigger?")
            return []
        return params["names"]

    @task.branch(task_id="select_languages", task_display_name="Select languages")
    def select_languages(**kwargs) -> list[str]:
        params = kwargs["params"]
        selected_languages = []
        for lang in ["english", "german", "french"]:
            if params[lang]:
                selected_languages.append(f"generate_{lang}_greeting")
        return selected_languages

    @task(task_id="generate_english_greeting", task_display_name="Generate English greeting")
    def generate_english_greeting(name: str) -> str:
        return f"Hello {name}!"

    @task(task_id="generate_german_greeting", task_display_name="Erzeuge Deutsche Begrüßung")
    def generate_german_greeting(name: str) -> str:
        return f"Sehr geehrter Herr/Frau {name}."

    @task(task_id="generate_french_greeting", task_display_name="Produire un message d'accueil en français")
    def generate_french_greeting(name: str) -> str:
        return f"Bonjour {name}!"

    @task(task_id="print_greetings", task_display_name="Print greetings", trigger_rule=TriggerRule.ALL_DONE)
    def print_greetings(greetings1, greetings2, greetings3) -> None:
        for g in greetings1 or []:
            print(g)
        for g in greetings2 or []:
            print(g)
        for g in greetings3 or []:
            print(g)
        if not (greetings1 or greetings2 or greetings3):
            print("sad, nobody to greet :-(")

    lang_select = select_languages()
    names = get_names()
    english_greetings = generate_english_greeting.expand(name=names)
    german_greetings = generate_german_greeting.expand(name=names)
    french_greetings = generate_french_greeting.expand(name=names)
    lang_select >> [english_greetings, german_greetings, french_greetings]
    results_print = print_greetings(english_greetings, german_greetings, french_greetings)

```

```
    params={
        # Let's start simple: Standard dict values are detected from type and offered as entry form fields.
        # Detected types are numbers, text, boolean, lists and dicts.
        # Note that such auto-detected parameters are treated as optional (not required to contain a value)
        "number_param": 3,
        "text_param": "Hello World!",
        "bool_param": False,
        "list_param": ["one", "two", "three", "actually one value is made per line"],
        "dict_param": {"key": "value"},
        # You can arrange the entry fields in sections so that you can have a better overview for the user
        # Therefore you can add the "section" attribute.
        # But of course you might want to have it nicer! Let's add some description to parameters.
        # Note if you can add any Markdown formatting to the description, you need to use the description_md
        # attribute.
        "most_loved_number": Param(
            42,
            type="integer",
            title="Your favorite number",
            description_md="Everybody should have a **favorite** number. Not only _math teachers_. "
            "If you can not think of any at the moment please think of the 42 which is very famous because "
            "of the book [The Hitchhiker's Guide to the Galaxy]"
            "(https://en.wikipedia.org/wiki/Phrases_from_The_Hitchhiker%27s_Guide_to_the_Galaxy#"
            "The_Answer_to_the_Ultimate_Question_of_Life,_the_Universe,_and_Everything_is_42).",
            minimum=0,
            maximum=128,
            section="Typed parameters with Param object",
        ),
        # If you want to have a selection list box then you can use the enum feature of JSON schema
        "pick_one": Param(
            "value 42",
            type="string",
            title="Select one Value",
            description="You can use JSON schema enum's to generate drop down selection boxes.",
            enum=[f"value {i}" for i in range(16, 64)],
            section="Typed parameters with Param object",
        ),

```

```
        "required_field": Param(
            # In this example we have no default value
            # Form will enforce a value supplied by users to be able to trigger
            type="string",
            title="Required text field",
            minLength=10,
            maxLength=30,
            description="This field is required. You can not submit without having text in here.",
            section="Typed parameters with Param object",
        ),
        "optional_field": Param(
            "optional text, you can trigger also w/o text",
            type=["null", "string"],
            title="Optional text field",
            description_md="This field is optional. As field content is JSON schema validated you must "
            "allow the `null` type.",
            section="Typed parameters with Param object",
        ),

```

```
    @task(task_display_name="Show used parameters")
    def show_params(**kwargs) -> None:
        params = kwargs["params"]
        print(f"This DAG was triggered with the following parameters:\n\n{json.dumps(params, indent=4)}\n")

    show_params()
```


