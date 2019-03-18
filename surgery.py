import ctypes
import functools
from inspect import iscode
from types import FunctionType


def surgery(test=True):
    def surgery_core(f):
        def get_root_arg_info(f):
            return {argname: num for num, argname in enumerate(f.__code__.co_varnames[:f.__code__.co_argcount])}

        def make_closure(f, co_const, *args):
            arg_dict = get_root_arg_info(f)

            arg_pos = []
            for freevar in co_const.co_freevars:
                if freevar in arg_dict:
                    arg_pos.append(arg_dict[freevar])

            PyCellNew = ctypes.pythonapi.PyCell_New
            PyCellNew.argtypes = [ctypes.py_object]
            PyCellNew.restype = ctypes.py_object
            cells = tuple(PyCellNew(arg) for pos, arg in enumerate(args) if pos in arg_pos)
            return cells

        def make_inner_f_cores(f, *args):
            f_list = []
            for co_const in f.__code__.co_consts:
                if iscode(co_const) and co_const.co_freevars:
                    f_list.append(FunctionType(co_const, f.__globals__, name=co_const.co_name, closure=make_closure(f, co_const, *args)))
                elif iscode(co_const) and not co_const.co_freevars:
                    f_list.append(FunctionType(co_const, f.__globals__, name=co_const.co_name))

            return f_list

        @functools.wraps(f)
        def core(*args):
            inner_f_names = [co_const.co_name for co_const in f.__code__.co_consts if iscode(co_const)]
            inner_f_cores = make_inner_f_cores(f, *args)
            inner_f_dict = dict(zip(inner_f_names, inner_f_cores))
            return inner_f_dict

        @functools.wraps(f)
        def pass_f(*args, **kwargs):
            return f(*args, **kwargs)

        if test:
            return core 
        else:
            return pass_f

    return surgery_core

