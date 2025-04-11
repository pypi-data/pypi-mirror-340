#!/usr/bin/env python3
# coding=utf-8


import sys
import re
import argparse
import functools
import inspect
from typing import Callable, Optional, TypeVar
import importlib
import textwrap

import argcomplete
import rich

from .libargparse import RichArgParser
from .liblogging import fastLogger


F = TypeVar("F", bound=Callable[..., any])

logger = fastLogger("easyarg")


class EasyArg:
    """
    Used to generate subparsers for target functions by decorating `@instance.command()`
    Then, call `instance.parse` to run corresponding function based on CLI command
    """

    def __init__(self, description: str = ""):
        """
        Initialize:
            - argparse.ArgumentParser & its subparsers
            - functions holder

        Last Update: @2024-11-23 14:35:26
        """
        self.parser = RichArgParser(description=description)
        self.subparsers = self.parser.add_subparsers(dest='command', help='Execute functions from CLI commands directly')
        self.functions = {}

    def command(self, name="", desc="", alias="", defaults: None | dict = None, choicess: None | dict = dict()) -> Callable[[F], F]:
        """
        A function decorator, used to generate a subparser and arguments based on the function signature

        :param defaults: Set specific default values for arguments under cmd invocation
        :param choicess: Set specific choices for arguments under cmd invocation

        ---------------------------------
        Last Update: @2025-04-10 18:36:40
        """
        if choicess is None:
            choicess = {}
        if defaults is None:
            defaults = {}

        def decorator(func: F) -> F:
            # @ Prepare
            # @ .handle-names
            # print(f">> Handling function: {func.__name__}")
            cmd_name = name if name else func.__name__
            cmd_name = cmd_name.replace("_", "-")
            if alias:
                aliases = [alias]
            else:
                aliases = []
            # @ .get-short-description
            if not desc and func.__doc__ is not None:
                desc2 = re.split(r'\n *\n', func.__doc__)[0].strip()  # Use the first paragraph
            else:
                desc2 = desc

            # @ .refine-long-doc | and save argument information
            argInfos = {}
            choicess_implicit = {}
            if func.__doc__ is not None:
                doc = textwrap.dedent(func.__doc__).strip()
                argLines = re.findall(r":param ([0-9a-zA-Z_]+): +(.*)", doc)
                for an, ai in argLines:  # @ exp | arg-name, arg-info
                    if an not in choicess:
                        rerst = re.match(r"(\{.*?\}) .*", ai)
                        if rerst:
                            elements = re.findall(r"\w+", rerst.group(1))
                            choicess_implicit[an] = elements
                            ai = re.sub(r"\{.*?\}", "", ai)
                    argInfos[an] = ai.strip()

                doc = re.sub(r':param [0-9a-zA-Z_]+: .*', '', doc)
                doc = re.sub(r':return ?: .*', '', doc)
                doc = re.sub(r'\n+', '\n', doc, flags=re.M)
                doc = doc.strip()
            else:
                doc = desc2

            # @ .create-subparser
            parser = self.subparsers.add_parser(cmd_name, aliases=aliases, help=desc2, description=doc)  # @ exp | Add a subparser with command the same as function name
            # parser._main_parser = self.parser

            # @ Main | Add arguments with proper attributes
            shortname_recorded = set()
            sig = inspect.signature(func)
            for param_name, param in sig.parameters.items():
                # @ .retrieve-type | From annotations, take the first type for the compound types, e.g. get `str`` for `typing.Union[str, float]`
                param_name_opt = param_name.replace("_", "-")
                cmdType, nargs = EasyArg.search_cmdType(param.annotation)
                assert cmdType, f"Failed to find cmd type for {param_name}: {param.annotation}"

                if param_name in choicess_implicit:  # @ exp | apply implicit choices according to param type
                    choicess[param_name] = [cmdType(e) for e in choicess_implicit[param_name]]

                # @ .get-attribute
                required = param.default == inspect._empty
                if param_name in defaults:
                    default = defaults[param_name]
                    required = False
                else:
                    default = None if required else param.default
                # logger.debug(f"{param_name=}, default={default}")

                # @ .add-argument | Only support intrinsic types: int, float, str & bool
                # @ - Use the first letter as short-name if no conflict
                if cmdType == inspect.Parameter.empty:
                    raise TypeError(f"Parameter '{param_name}' in function '{func.__name__}' missing type hint")

                elif cmdType in (int, float, str, bool):
                    short_name = param_name[0]
                    assert short_name.isalpha()
                    option_strings = ["--" + param_name_opt]
                    if short_name not in shortname_recorded:
                        option_strings.append("-" + short_name)
                        shortname_recorded.add(short_name)

                    if cmdType is bool:
                        parser.add_argument(*option_strings, dest=param_name, action="store_true", required=required, default=default, help=argInfos.get(param_name, ""))
                    else:
                        kwargs = dict(type=cmdType, required=required, default=default, choices=choicess.get(param_name), help=argInfos.get(param_name, ""))
                        if nargs:
                            kwargs["nargs"] = nargs
                        # print(option_strings, kwargs)
                        parser.add_argument(*option_strings, **kwargs)
                # elif cmdType == bool:
                #     # @ ..handle-bool-specifically
                #     short_name = param_name[0]
                #     assert short_name.isalpha()
                #     if required:
                #         parser.required_bool_pair.append(param_name)
                #     if short_name not in shortname_recorded:
                #         parser.add_argument(f"--{param_name_opt}", f"-{short_name}", dest=param_name, action="store_true", default=default, help=argInfos.get(param_name, ""))
                #         shortname_recorded.add(short_name)
                #     else:
                #         parser.add_argument(f"--{param_name_opt}", dest=param_name, action="store_true", default=default, help=argInfos.get(param_name, ""))
                #     parser.add_argument(f"--no-{param_name_opt}", dest=param_name, action="store_false", default=None if default is None else not default, help=argInfos.get(param_name, ""))
                else:
                    raise TypeError(f"easyarg only supports types: int, float, str & bool, now is {cmdType}")

            # @ Post
            self.functions[cmd_name] = func
            for al in aliases:
                self.functions[al] = func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper  # type: ignore
        return decorator

    def parse(self, args: Optional[list[str]] = None):
        """
        Last Update: @2024-11-23 14:40:31
        ---------------------------------
        Parse arguments and call corresponding function
        """
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args(args)
        kwargs = {key: value for key, value in vars(args).items() if key != 'command' and value is not None}

        if args.command is None:
            self.parser.print_help()
            return
        # print(self.functions)
        func = self.functions[args.command]
        func(**kwargs)

    @staticmethod
    def search_cmdType(annotation) -> tuple[type | None, str]:
        """
        Search appropriate type in command line arguments, i.e., str | int | float | bool

        Last Update: @2025-02-28 13:34:50
        """
        from typing import types

        if isinstance(annotation, type):
            if annotation in (str, int, float, bool):
                return annotation, ""
        elif isinstance(annotation, types.UnionType):
            # @ exp | e.g., list[str], tuple[int]
            for a in annotation.__args__:
                rst, _ = EasyArg.search_cmdType(a)
                if rst:
                    return rst, ""
        elif isinstance(annotation, types.GenericAlias):
            orig = annotation.__origin__
            if orig in (list, tuple):
                rst, _ = EasyArg.search_cmdType(annotation.__args__[0])
                return rst, "*"

        return None, ""
