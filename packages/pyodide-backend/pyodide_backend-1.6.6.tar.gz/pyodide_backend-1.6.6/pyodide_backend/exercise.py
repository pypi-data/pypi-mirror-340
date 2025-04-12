import json
import warnings

from .interactive_shell import FILENAME
from .process import WasmProcess
from .task import TaskNoOutput, TaskCaptureCodeExecutionOutput


class PyodideExercise:
    def __init__(self, pec: str, solution: str, sct: str):
        self.pec = pec
        self.solution = solution
        self.sct = sct

        self.user_process = None
        self.solution_process = None

        # Ignore warnings like package deprecation warnings
        warnings.filterwarnings("ignore")

    def run_init(self, height: int = 320, width: int = 320):
        self.user_process = WasmProcess()

        result, _raw_output = self.user_process.executeTask(
            TaskCaptureCodeExecutionOutput([self.pec])
        )

        return json.dumps(result)

    def run_code(self, code: str, height: int = 320, width: int = 320):
        if self.user_process is None:
            self.user_process = WasmProcess()
            output, _ = self.user_process.executeTask(
                TaskCaptureCodeExecutionOutput([self.pec, code], height, width)
            )
            return json.dumps(output)

        output, _ = self.user_process.executeTask(
            TaskCaptureCodeExecutionOutput([code], height, width)
        )
        return json.dumps(output)

    def map_output(self, output):
        if output["type"] in ["error", "graph"]:
            return {
                "payload": output["payload"],
                "type": output["type"],
            }

        return {
            "payload": {
                "output": output["payload"],
                "script_name": FILENAME,
            },
            "type": "script-output",
        }

    def run_submit(self, code: str, height: int = 320, width: int = 320):
        if self.solution_process is None:
            self.solution_process = WasmProcess()
            self.solution_process.executeTask(TaskNoOutput([self.pec, self.solution]))

        submit_process = WasmProcess()
        submit_process.shell.displayhook.returns_result = False

        outputs, raw_output = submit_process.executeTask(
            TaskCaptureCodeExecutionOutput([self.pec, code], height, width)
        )

        # Delay importing pythonwhat until it's needed, so that it doesn't slow
        # down initial pyodide setup. This means the first code submission will
        # be slower. This should be a good tradeoff, since code submissions are
        # already much faster than mux, while initial pyodide load is much slower.
        from pythonwhat import test_exercise

        test_result = test_exercise(
            sct=self.sct,
            student_code=code,
            solution_code=self.solution,
            pre_exercise_code=self.pec,
            student_process=submit_process,
            solution_process=self.solution_process,
            raw_student_output=raw_output["output_stream"],
            ex_type="CodingExercise",
            error=raw_output["error"],
        )

        result = [self.map_output(output) for output in outputs] + [
            {"payload": test_result, "type": "sct"},
        ]

        return json.dumps(result)
