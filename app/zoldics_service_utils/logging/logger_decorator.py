from typing import List, Optional
from .base_logger import APP_LOGGER


class LogExecution:
    def __init__(self, vars_to_log: Optional[List[str]] = None) -> None:
        self.vars_to_log = vars_to_log

    def __call__(self, func):
        def wrapper(instance, *args, **kwargs):
            class_name = instance.__class__.__name__
            function_name = func.__name__
            APP_LOGGER.info(f"Executing {function_name} method of class {class_name}.")
            try:
                result = func(instance, *args, **kwargs)
                instance_variables = (
                    {
                        var: getattr(instance, var)
                        for var in self.vars_to_log
                        if hasattr(instance, var)
                    }
                    if self.vars_to_log
                    else None
                )
                if result or instance_variables:
                    APP_LOGGER.info(
                        {
                            "instance_variables": instance_variables,
                            "result": result,
                        }
                    )
                return result
            except Exception:
                raise

        return wrapper
