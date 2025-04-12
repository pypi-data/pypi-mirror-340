import code
from contextlib import redirect_stdout
import sys

from .display_hook import DisplayHook
from .custom_print import custom_print


FILENAME = "script.py"


class InteractiveShell(code.InteractiveConsole):
    def __init__(self, locals=None):
        super().__init__(locals)

        self.displayhook = DisplayHook()
        self.locals["print"] = custom_print

    def _handle_ipython_help_query(self, code_str):
        stripped = code_str.strip()
        if stripped.startswith("?"):
            target_name = stripped[1:].strip()
            try:
                target = eval(target_name, self.locals)

                import inspect

                try:
                    signature = inspect.signature(target)
                except Exception:
                    signature = None
                if signature is not None:
                    print(f"Signature: {target.__name__}{signature}")
                doc = target.__doc__
                if doc:
                    print("Docstring:")
                    print(doc)
                else:
                    print("No docstring available.")
                print("Type:      " + type(target).__name__)
            except Exception:
                print(f"Object `{target_name}` not found.")
            return True
        return False

    def run_cell(self, code_str):
        import textwrap

        code_str = textwrap.dedent(code_str)

        new_lines = []
        for line in code_str.splitlines():
            if line.strip().startswith("?"):
                self._handle_ipython_help_query(line)
            else:
                new_lines.append(line)
        code_str = "\n".join(new_lines)
        if not code_str.strip():
            return None

        try:
            # Split the cell into lines; if there is more than one line,
            # attempt to treat the final non-comment line as an expression.
            lines = code_str.rstrip("\n").split("\n")
            while lines and (
                not lines[-1].strip() or lines[-1].strip().startswith("#")
            ):
                lines.pop()
            if len(lines) > 1:
                try:
                    last_expr_code = compile(lines[-1], f"<{FILENAME}>", "eval")
                except SyntaxError:
                    last_expr_code = None
                if last_expr_code is not None:
                    pre_code = "\n".join(lines[:-1])
                    if pre_code.strip():
                        exec(compile(pre_code, f"<{FILENAME}>", "exec"), self.locals)
                    result = eval(last_expr_code, self.locals)
                    self.displayhook(result)
                    return None
            # Fallback: try to compile the whole cell as an expression.
            try:
                code_obj = compile(code_str, f"<{FILENAME}>", "eval")
                result = eval(code_obj, self.locals)
                self.displayhook(result)
            except SyntaxError:
                code_obj = compile(code_str, f"<{FILENAME}>", "exec")
                exec(code_obj, self.locals)
            return None
        except Exception as e:
            # Return the exception to be handled by the caller.
            return e

    def reset(self):
        self.locals.clear()
        self.displayhook.result = []

    @property
    def user_ns(self):
        return self.locals
