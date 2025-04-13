from collections.abc import Callable
import TotalLog.TotalLog
from TotalLog import Print
from TotalLog import utils
import traceback

def error_log(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            stack = traceback.extract_stack()
            line = stack[-2].lineno
            error = f"Error in function: [{func.__name__}]\narguments: [args: {args}, kwargs: {kwargs}]\nerror:\n{e}"
            self = Print.Loger
            if self.filename:
                utils.add_log(error, "SYSTEM\n%(message)s", self.filename, "SYSTEM", line, self.log_format)
            print(error)
    return wrapper

def if_active(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        if Print.Loger.active:
            result = func(*args, **kwargs)
            return result
    return wrapper
