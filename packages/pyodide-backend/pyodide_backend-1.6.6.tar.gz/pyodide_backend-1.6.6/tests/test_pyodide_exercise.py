import base64
import json
import re


from pyodide_backend import PyodideExercise


def test_run_code():
    pec = "x = 10"
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_code("print(x)\nx+1\n# All good!")

    assert json.loads(result) == [
        {"type": "output", "payload": "10"},
        {"type": "result", "payload": "11"},
    ]


def test_run_code_with_ipython_magic_command():
    pec = ""
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_code("?pow")

    assert json.loads(result) == [
        {
            "type": "output",
            "payload": """Signature: pow(base, exp, mod=None)
Docstring:
"""
            + pow.__doc__
            + """
Type:      builtin_function_or_method""",
        }
    ]


def test_run_indented_code():
    pec = ""
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_code("    print(1+1)")

    assert json.loads(result) == [{"type": "output", "payload": "2"}]


def test_run_dataframe_code():
    pec = "import pandas as pd"
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_code(
        """
d = {'store': [1, 2], 'type': ['A', 'A'], 'department': [1, 1], 'date': ['2010-02-05', '2010-03-05'], 'weekly_sales': [24924.50, 35034.06], 'is_holiday': [False, False], 'temperature_c': [5.727778, 4.55], 'fuel_price_usd_per_l': [0.679451, 0.679451], 'unemployment': [8.106, 8.324]}
df = pd.DataFrame(data=d)
print(df)
df
"""
    )

    assert json.loads(result) == [
        {
            "type": "output",
            "payload": """   store type  department        date  weekly_sales  is_holiday  temperature_c  fuel_price_usd_per_l  unemployment
0      1    A           1  2010-02-05      24924.50       False       5.727778              0.679451         8.106
1      2    A           1  2010-03-05      35034.06       False       4.550000              0.679451         8.324""",
        },
        {
            "type": "result",
            "payload": """
   store type  department        date  weekly_sales  is_holiday  temperature_c  fuel_price_usd_per_l  unemployment
0      1    A           1  2010-02-05      24924.50       False       5.727778              0.679451         8.106
1      2    A           1  2010-03-05      35034.06       False       4.550000              0.679451         8.324""",
        },
    ]


def test_run_code_with_graph():
    pec = ""
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_code(
        """
year = [2024, 2025]
pop = [2.53,2.57]

import matplotlib.pyplot as plt

plt.plot(year, pop)
plt.show()
"""
    )

    result_output = json.loads(result)[0]
    assert result_output["type"] == "graph"

    # Payload is a base64 encoded SVG
    assert re.match(
        r"^[A-Za-z0-9+/]+={0,2}$", result_output["payload"]
    ), "Invalid base64 encoding"
    decoded_svg = base64.b64decode(result_output["payload"]).decode("utf-8")
    assert re.match(
        r"<\?xml.*>\n<!DOCTYPE svg.*>\n<svg.*>", decoded_svg, re.DOTALL
    ), "Decoded string is not an SVG"


def test_run_code_error():
    pec = "x = 10"
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_code("this is invalid syntax")

    assert json.loads(result) == [
        {
            "type": "error",
            "payload": '  File "<script.py>", line 1\n    this is invalid syntax\n                    ^^^^^^\nSyntaxError: invalid syntax\n',
        }
    ]


def test_run_submit():
    pec = ""
    solution = """
# Create a variable savings
savings = 100

# Print out savings
print(savings)
"""
    sct = """
Ex().check_object("savings").has_equal_value(incorrect_msg="Assign `100` to the variable `savings`.")
Ex().has_printout(0, not_printed_msg = "Print out `savings`, the variable you created, with `print(savings)`.")
success_msg("Great! Let's try to do some calculations with this variable now!")
    """
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    code = """
savings = 100
print(savings)
1+1
    """
    result = exercise.run_submit(code)

    assert json.loads(result) == [
        {
            "payload": {"output": "100", "script_name": "script.py"},
            "type": "script-output",
        },
        {
            "payload": {
                "correct": True,
                "message": "Great! Let's try to do some calculations with this variable now!",
            },
            "type": "sct",
        },
    ]


def test_run_submit_with_graph():
    pec = ""
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_submit(
        """
year = [2024, 2025]
pop = [2.53,2.57]

import matplotlib.pyplot as plt

plt.plot(year, pop)
plt.show()
"""
    )

    result_outputs = json.loads(result)
    assert result_outputs[0]["type"] == "graph"

    # Payload is a base64 encoded SVG
    assert re.match(
        r"^[A-Za-z0-9+/]+={0,2}$", result_outputs[0]["payload"]
    ), "Invalid base64 encoding"
    decoded_svg = base64.b64decode(result_outputs[0]["payload"]).decode("utf-8")
    assert re.match(
        r"<\?xml.*>\n<!DOCTYPE svg.*>\n<svg.*>", decoded_svg, re.DOTALL
    ), "Decoded string is not an SVG"

    assert result_outputs[1] == {
        "payload": {
            "correct": True,
            "message": "Great work!",
        },
        "type": "sct",
    }


def test_run_submit_syntax_error():
    pec = ""
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_submit("print(1+1")

    assert json.loads(result) == [
        {
            "type": "error",
            "payload": "  File \"<script.py>\", line 1\n    print(1+1\n         ^\nSyntaxError: '(' was never closed\n",
        },
        {
            "type": "sct",
            "payload": {
                "correct": False,
                "message": "Your code can not be executed due to a syntax error:<br><code>'(' was never closed (script.py, line 1).</code>",
            },
        },
    ]


def test_run_submit_runtime_error():
    pec = ""
    solution = ""
    sct = ""
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    result = exercise.run_submit(
        """
print(1)
print(a)
"""
    )

    assert json.loads(result) == [
        {
            "payload": {"output": "1", "script_name": "script.py"},
            "type": "script-output",
        },
        {
            "type": "error",
            "payload": "NameError: name 'a' is not defined\n",
        },
        {
            "type": "sct",
            "payload": {
                "correct": False,
                "message": "Your code generated an error. Fix it and try again!",
            },
        },
    ]


def test_run_submit_sct_failure():
    pec = ""
    solution = """
# Create a variable savings
savings = 100

# Print out savings
print(savings)
    """
    sct = """
Ex().check_object("savings").has_equal_value(incorrect_msg="Assign `100` to the variable `savings`.")
Ex().has_printout(0, not_printed_msg = "Print out `savings`, the variable you created, with `print(savings)`.")
success_msg("Great! Let's try to do some calculations with this variable now!")
        """
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    code = """
savings = 123
print(savings)
        """
    result = exercise.run_submit(code)

    assert json.loads(result) == [
        {
            "payload": {"output": "123", "script_name": "script.py"},
            "type": "script-output",
        },
        {
            "payload": {
                "correct": False,
                "message": "Assign <code>100</code> to the variable <code>savings</code>.",
                "line_start": 2,
                "column_start": 1,
                "line_end": 2,
                "column_end": 13,
            },
            "type": "sct",
        },
    ]


def test_run_submit_sct_after_previous_submits():
    pec = "savings = 100"
    solution = "print(savings)"
    sct = """
Ex().check_object("savings").has_equal_value(incorrect_msg="Assign `100` to the variable `savings`.")
Ex().has_printout(0, not_printed_msg = "Print out `savings`, the variable you created, with `print(savings)`.")
success_msg("Great! Let's try to do some calculations with this variable now!")
        """
    exercise = PyodideExercise(pec=pec, solution=solution, sct=sct)
    exercise.run_init()

    code = "print(savings)"
    result1 = exercise.run_submit(code)
    assert json.loads(result1) == [
        {
            "payload": {"output": "100", "script_name": "script.py"},
            "type": "script-output",
        },
        {
            "payload": {
                "correct": True,
                "message": "Great! Let's try to do some calculations with this variable now!",
            },
            "type": "sct",
        },
    ]

    code = "print(savings)"
    result2 = exercise.run_submit(code)

    assert json.loads(result2) == [
        {
            "payload": {"output": "100", "script_name": "script.py"},
            "type": "script-output",
        },
        {
            "payload": {
                "correct": True,
                "message": "Great! Let's try to do some calculations with this variable now!",
            },
            "type": "sct",
        },
    ]
