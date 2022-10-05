from enum import IntFlag


class FuncOption(IntFlag):
    declare_function2_reserved = 128
    preload_global = 64
    preload_parent = 32
    preload_root = 16
    suppress_super = 8
    preload_super = 4
    suppress_arguments = 2
    preload_arguments = 1
    # suppress_this
    # preload_this
