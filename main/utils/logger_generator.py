import inspect
import os
import main
import logging
from main.utils.naming_management import change_slash_and_dot

main_folder = os.path.dirname(main.__file__)


def get_logger(path=''):
    """
    Generate logger for each file where this method's caller located in.
    This help developer experience without having to respecifiy the name of
    the logger.

    Example:

    caller filename:
    '/ifml-angular-pwa/main/core/react/interpreter/base.py'

    main module location:
    '/ifml-angular-pwa/main'

    logger created from filename:
    'core.react.interpreter.base'

    :param path: specify the valid path.
    :return: logger from logging module.
    """
    if not path:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        path = module.__file__

    intersect = os.path.commonpath([path, main_folder])
    my_relative_path = change_slash_and_dot(path[len(intersect) + 1:-3],
                                            '.')

    return logging.getLogger(my_relative_path)
