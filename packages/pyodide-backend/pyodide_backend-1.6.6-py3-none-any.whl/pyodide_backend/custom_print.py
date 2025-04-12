import builtins


def custom_print(*args, **kwargs):
    try:
        from pandas import DataFrame
    except ImportError:
        DataFrame = None

    def format_arg(arg):
        if DataFrame is not None and isinstance(arg, DataFrame):
            return arg.to_string(max_cols=20, line_width=800)
        return arg

    formatted_args = [format_arg(arg) for arg in args]
    builtins.print(*formatted_args, **kwargs)
