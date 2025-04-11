from . import rspx
from .rspx import *


__doc__ = rspx.__doc__
if hasattr(rspx, "__all__"):
    __all__ = rspx.__all__


def sum(a, b):
    return rspx.sum_as_string(a, b)


def fib(n):
    return rspx.fib(n)
