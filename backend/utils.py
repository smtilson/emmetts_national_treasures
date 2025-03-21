import logging
import functools
import inspect

def log_method_calls(cls=None, logger=None):
    """
    Class decorator that adds logging to all methods of a class.
    Can be used as @log_method_calls or @log_method_calls(logger=custom_logger)
    """
    def decorator(cls):
        # If no logger is provided, create one based on the class module
        log = logger or logging.getLogger(cls.__module__)
        
        # Get all methods defined in the class
        for name, method in inspect.getmembers(cls, inspect.isfunction):
            # Skip private methods (starting with _)
            if name.startswith('_'):
                continue
                
            @functools.wraps(method)
            def wrapped(self, *args, **kwargs):
                method_name = f"{cls.__name__}.{method.__name__}"
                debug_msg = f"Executing {method_name} with params:"
                for arg in args:
                    debug_msg += f"\n- {arg}"
                for key, value in kwargs.items():
                    debug_msg += f"\n- {key}: {value}"
                log.debug(debug_msg)
                try:
                    result = method(self, *args, **kwargs)
                    log.debug(f"Exiting {method_name}")
                    return result
                except Exception as e:
                    log.error(f"Exception in {method_name}: {str(e)}", exc_info=True)
                    raise
                    
            setattr(cls, name, wrapped.__get__(None, cls))
        return cls
        
    # Handle both @log_method_calls and @log_method_calls()
    if cls is None:
        return decorator
    return decorator(cls)


def log_function(func=None, logger=None):
    """
    Function decorator that adds logging to a function.
    Can be used as @log_function or @log_function(logger=custom_logger)
    """
    def decorator(func):
        # If no logger is provided, create one based on the function's module
        log = logger or logging.getLogger(func.__module__)
        
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            func_name = func.__name__
            debug_msg = f"Executing {func_name} with params:"
            for arg in args:
                debug_msg += f"\n- {arg}"
            for key, value in kwargs.items():
                debug_msg += f"\n- {key}: {value}"
            log.debug(debug_msg)    
            try:
                result = func(*args, **kwargs)
                log.debug(f"Exiting {func_name}")
                return result
            except Exception as e:
                log.error(f"Exception in {func_name}: {str(e)}", exc_info=True)
                raise
                
        return wrapped
        
    # Handle both @log_function and @log_function()
    if func is None:
        return decorator
    return decorator(func)
