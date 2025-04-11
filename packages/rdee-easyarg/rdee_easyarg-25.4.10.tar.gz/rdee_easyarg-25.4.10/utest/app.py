#!/usr/bin/env python3
# coding=utf-8

import easyarg

ea = easyarg.EasyArg()


@ea.command(defaults={"y": 3}, choicess=dict(x=(1, 2, 3)))
def add(x: int, y: int, z: int = 0) -> int:
    """Add two numbers"""
    print(f"{x + y + z=}")


@ea.command()
def mul(a: float | str, B: float, c: float = 1.0) -> float:
    """
    Multiply numbers

    Last Update: @2025-01-15 22:09:36
    """
    print(f"{(a * B * c)=}")


@ea.command(desc="divide calculation")
def div(q1: float | str, Q2: float, q3: float = 1.0) -> float:
    print(f"{(q1 / Q2 / q3)=}")


@ea.command(alias="d2")
def div2(q1: float | str, Q2: float, flag2: bool, q3: float = 1.0, flag1: bool = True) -> float:
    """
    a test div2 function

    :param flag2: required bool flag
    :param Q2: required float Q2
    """
    print(f"{(q1 / Q2 / q3)=}")


@ea.command()
def vtks2ver(ifiles: list[str], version: str = "5.1", odir: str = ".", binary: bool = True, gtonly: bool = False):
    """
    debug @2025-04-10
    """
    print(f"{ifiles=}")
    print(f"{version=}")
    print(f"{odir=}")
    print(f"{binary=}")
    print(f"{gtonly=}")


if __name__ == "__main__":
    ea.parse()
