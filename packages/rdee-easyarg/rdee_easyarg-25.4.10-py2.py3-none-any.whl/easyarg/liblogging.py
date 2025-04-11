# coding=utf-8

"""
Library for the customized logger
"""


# *********************************************************
# Import
# *********************************************************
# ----- STL
import sys
import os
import logging
import json
from typing import Optional, Union


# *********************************************************
# Add custom logging level VERBOSE (15) and IMPORTANT (25)
# i.e., DEBUG < VERBOSE < INFO < IMPORTANT < WARNING < ...
# *********************************************************
VERBOSE = 15
logging.addLevelName(VERBOSE, "VERBOSE")
IMPORTANT = 25
logging.addLevelName(IMPORTANT, "IMPORTANT")
logging.VERBOSE = VERBOSE
logging.IMPORTANT = IMPORTANT


def _verbose(self, message, *args, **kws):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, stacklevel=2, **kws)


def _important(self, message, *args, **kws):
    if self.isEnabledFor(IMPORTANT):
        self._log(IMPORTANT, message, args, stacklevel=2, **kws)


logging.Logger.verbose = _verbose
logging.Logger.important = _important


# *********************************************************
# fastLogger with customized format and filter
# *********************************************************
class ColorFormatter(logging.Formatter):
    """
    Colorful format for logging text

    reference: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output

    ---------------------------------
    Last Update: @2025-02-19 11:34:32
    """

    FORMATS = {
        logging.DEBUG: "\033[38;5;51m%(name)s:\033[0m \033[4m%(asctime)s\033[0m (\033[38;5;51m%(funcName)s\033[38;5;251m:%(lineno)d\033[0m) \033[35m[%(levelname)s]\033[0m %(message)s",
        logging.VERBOSE: "\033[38;5;51m%(name)s:\033[0m \033[4m%(asctime)s\033[0m (\033[38;5;51m%(funcName)s\033[38;5;251m:%(lineno)d\033[0m) \033[32m[%(levelname)s]\033[0m %(message)s",
        logging.INFO: "\033[38;5;51m%(name)s:\033[0m \033[4m%(asctime)s\033[0m (\033[38;5;51m%(funcName)s\033[38;5;251m:%(lineno)d\033[0m) \033[36m[%(levelname)s]\033[0m %(message)s",
        logging.IMPORTANT: "\033[38;5;51m%(name)s:\033[0m \033[4m%(asctime)s\033[0m (\033[38;5;51m%(funcName)s\033[38;5;251m:%(lineno)d\033[0m) \033[38;5;226m[%(levelname)s]\033[0m %(message)s",
        logging.WARNING: "\033[38;5;51m%(name)s:\033[0m \033[4m%(asctime)s\033[0m (\033[38;5;51m%(funcName)s\033[38;5;251m:%(lineno)d\033[0m) \033[33m[%(levelname)s]\033[0m %(message)s",
        logging.ERROR: "\033[38;5;51m%(name)s:\033[0m \033[4m%(asctime)s\033[0m (\033[38;5;51m%(funcName)s\033[38;5;251m:%(lineno)d\033[0m) \033[31m[%(levelname)s]\033[0m %(message)s",
        logging.CRITICAL: "\033[38;5;51m%(name)s:\033[0m \033[4m%(asctime)s\033[0m (\033[38;5;51m%(funcName)s\033[38;5;251m:%(lineno)d\033[0m) \033[31;1m[%(levelname)s]\033[0m %(message)s"
    }

    def format(self, record):  # @| required method for class logging.Formatter
        log_fmt = self.FORMATS.get(record.levelno)
        if os.getenv("PYTHON_LOGGING_TIME") == "DATETIME":
            date_format = "%Y-%m-%d %H:%M:%S"
        else:
            date_format = "%H:%M:%S"
        formatter = logging.Formatter(log_fmt, datefmt=date_format)
        return formatter.format(record)


def _get_llspec_from_env() -> Optional[dict]:
    """
    Get log level specification from environment variable:
        - $env:PYTHON_LLSPEC_JSON
            Use a json file
        - $env:PYTHON_LLSPEC_COMMA
            Use a comma-sep string directly

    ---------------------------------
    Last Update: @2025-01-20 11:13:33
    """
    llspec = None

    jsf = os.getenv("PYTHON_LLSPEC_JSON")
    if jsf:
        try:
            with open(jsf) as f:
                llspec = json.load(f)
        except:
            raise RuntimeError("env:PYTHON_LLSPEC_JSON points to an invalid json file")
    else:
        spec_commas = os.getenv("PYTHON_LLSPEC_COMMA")
        if spec_commas:
            llspec = dict(item.split("=") for item in spec_commas.split(","))

    if llspec:
        llspec = {k: _v2ll(v) for k, v in llspec.items()}

    return llspec


class EnvFilter(logging.Filter):
    """
    This class provides a subclass of logging.Filter, aiming to set logging level by functions.
    It stores the logger instance for retrieving llspec afterwards.
    Don't consider top-level log by now

    ---------------------------------
    Last Update: @2024-08-30 14:52:38
    """

    def __init__(self, logger: logging.Logger):
        super().__init__()
        self.logger: logging.Logger = logger

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno >= logging.WARNING:
            return True
        llspec = self.logger.llspec

        target_name = record.funcName if record.funcName != "<module>" else record.module  # @ exp | For compatiability with module-level statements

        baselevel = logging.INFO if "base" not in llspec else llspec["base"]
        if target_name in llspec:
            return record.levelno >= llspec[target_name]
        else:
            return record.levelno >= baselevel


def fastLogger(name="root", level: Union[str, int, None] = None) -> logging.Logger:
    """
    Get a logging.Logger with flexible logging level setting via several environment variables

    including :
        - env:  PYTHON_LLSPEC_JSON
            - A json file for specific level settings, i.e., {"base": "INFO", "a_func_name":"DEBUG"}
        - env:  PYTHON_LLSPEC_COMMA
            - A string for specific level settings (can be considered as a serialization for PYTHON_LLSPEC_JSON content), e.g., "base=INFO,a_func_name=DEBUG"
        - env:  arg(level)
            - Just set the level for the whole logger
            - Support name, name in UPPERCASE, both with optional prefix LOGLEVEL_

    :param name: logger name
    :param level: used to set level for the whole logger

    ---------------------------------
    Last Update: @2025-01-20 11:28:05
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        llspec = _get_llspec_from_env()
        if llspec is not None:
            logger.setLevel(logging.DEBUG)
            logger.llspec = llspec
            logger.addFilter(EnvFilter(logger))
        else:
            if level is None:
                level = name
            logger.setLevel(_v2ll(level))

        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(ColorFormatter())
        logger.addHandler(sh)
        logger.propagate = False
    return logger


def _v2ll(v: Union[str, int, None]) -> int:
    """
    Parses a variable to logging Level flexibly

    including:
        - direct int, e.g., 10 -> debug, 20 -> info, ...
        - string match, e.g., "info", "debug", ...
        - environment variable, i.e., [LOGLEVEL_]name, or [LOGLEVEL_]NAME

    ---------------------------------
    Last Update: @2025-01-20 11:27:44
    """

    # ~~~~~~~~~~~~~~~~~~ default
    if v is None:
        return logging.INFO

    # ~~~~~~~~~~~~~~~~~~ int
    if isinstance(v, int):
        return v

    # ~~~~~~~~~~~~~~~~~~ string
    if isinstance(v, str):
        # ----- int-string
        try:
            v_int = int(v)
            return _v2ll(v_int)
        except:
            pass

        # ----- level-string
        vU = v.upper()
        if vU.startswith("INFO"):
            return logging.INFO
        if vU.startswith("VERBOSE"):
            return logging.VERBOSE
        if vU.startswith("IMPORTANT"):
            return logging.IMPORTANT
        if vU.startswith("DEBUG"):
            return logging.DEBUG
        if vU.startswith("WARN"):
            return logging.WARNING
        if vU.startswith("ERROR"):
            return logging.ERROR
        if vU.startswith("FATAL"):
            return logging.FATAL

        # ----- environment-variable
        evvs = [f"LOGLEVEL_{v.upper()}", f"LOGLEVEL_{v}", v.upper(), v]
        for ev in evvs:
            envval = os.getenv(ev)
            if envval:
                return _v2ll(envval)

        return logging.INFO

    raise TypeError(f"Error! Unkown value for log-level type: {type(v)}")
