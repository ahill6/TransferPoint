# bugFolder
__author__ = 'Afsoon Afzal'

import logging

# LIBCLANG_PATH = '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib/libclang.dylib'
LIBCLANG_PATH = '/home/afsoon/llvm/build/lib/libclang.so'
# LIBCLANG_PATH = '/Users/afsoona/llvm/build/lib/libclang.dylib'

GENERATE_DB_PATH = '/home/ahill6/codeflaws/bugFolder'

Z3_COMMAND = '/home/afsoon/z3/build/z3'

LARGEST_SNIPPET = 7
SMALLEST_SNIPPET = 1

TIMEOUT = 7500

DATABASE = {
    'db_name': 'andy-test3', # switch back
    'user': 'ahill6',
    'password': None
}

ALL_PATCHES = False

LOGGING = {
    'filename': 'logs/repair.log',
    'level': logging.DEBUG
}

logging.basicConfig(**LOGGING)

MAX_SUSPICIOUS_LINES = 10

VALID_TYPES = ['int', 'short', 'long', 'char', 'float', 'double', 'long long', 'size_t']

TESTS_LIST = "/home/ahill6/codeflaws/bugFolder/tests_list.txt"
TEST_SCRIPT = "/home/ahill6/codeflaws/bugFolder/test-searchrepair.sh "
TEST_SCRIPT_TYPE = "/bin/bash"
COMPILE_SCRIPT = "cd /home/ahill6/codeflaws/bugFolder/ && make -f Makefile"
FAULTY_CODE = "/home/ahill6/codeflaws/bugFolder/buggyFile.c"
BUG_TYPE = "bugType"

COMPILE_EXTRA_ARGS = []

MAKE_OUTPUT = "/home/ahill6/codeflaws/bugFolder/makeout"

METHOD_RANGE = (1, 50)

SOSREPAIR = False
