from warnings import warn
import json
from pyodide_backend import PyodideExercise
from .fixtures.get_course_exercises import get_course_exercises


def _normalize_outputs(outputs):
    return json.dumps(
        [
            (
                {**output, "payload": "<graph-data-removed>"}
                if output.get("type") == "graph"
                else output
            )
            for output in json.loads(outputs)
        ]
    )


def _test_course_exercises(course_slug: str, snapshot):
    exercises = get_course_exercises(course_slug)

    if not exercises:
        warn(f"Skipping {course_slug} check.")
        return

    # Ensure we're loading all exercises correctly
    snapshot.assert_match(json.dumps(exercises), "_exercises.json")

    for ex in exercises:
        print(f"{ex['chapter']} - {ex['name']}")
        pyodide_exercise = PyodideExercise(
            pec=ex["pec"], solution=ex["solution"], sct=ex["sct"]
        )
        pyodide_exercise.run_init()

        code_result = pyodide_exercise.run_code(ex["solution"])
        normalized_code_result = _normalize_outputs(code_result)
        snapshot.assert_match(normalized_code_result, f"{ex['key']}_code_result.json")

        submit_result = pyodide_exercise.run_submit(ex["solution"])
        normalized_submit_result = _normalize_outputs(submit_result)
        snapshot.assert_match(
            normalized_submit_result, f"{ex['key']}_submit_result.json"
        )


def test_intro_to_python(snapshot):
    _test_course_exercises("courses-introduction-to-python", snapshot)


def test_intermediate_python(snapshot):
    _test_course_exercises("courses-intermediate-python", snapshot)
