import functools
import inspect
import logging


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # # create the logging file handler
    # fh = logging.FileHandler("/path/to/test.log")
    #
    # fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # formatter = logging.Formatter(fmt)
    # fh.setFormatter(formatter)
    #
    # # add handler to logger object
    # logger.addHandler(fh)
    return logger


def handle_errors(raise_types: tuple = (Exception,), accept_types: tuple = ()):
    def log_errors_decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except raise_types as e:
                create_error_log(args, kwargs)
                raise
            except accept_types as e:
                create_error_log(args, kwargs)

        def create_error_log(args, kwargs):
            logger = create_logger()
            selected_args = get_selected_args_from_method(args, kwargs)
            err_msg = f"There was an exception in method: {function.__name__}, args was: {selected_args}"
            logger.exception(err_msg)

        def get_selected_args_from_method(args, kwargs):
            args_name = inspect.getfullargspec(function)[0]
            args_dict = dict(zip(args_name, args))
            args_dict.pop("cls", None)
            args_dict.pop("self", None)
            return args_dict

        return wrapper

    return log_errors_decorator
