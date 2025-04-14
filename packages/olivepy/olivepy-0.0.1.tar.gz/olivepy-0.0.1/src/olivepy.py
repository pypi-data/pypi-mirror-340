#!/usr/bin/env python3

import argparse
import sys
import ctypes
from os import geteuid


parser = argparse.ArgumentParser(
    prog="Olivepy", description="Python inline tool", epilog=""
)

parser.add_argument(
    "-t",
    "--input-type",
    choices=["str", "int", "float", "complex", "bool", "smart"],
    default="str",
    help="The type the input should be interpreted as (default: str)",
)

parser.add_argument(
    "-e", "--input-encoding", default="utf8", help="The input encoding (default: utf8)"
)
# parser.add_argument('-E', '--output-encoding', default='utf8')

parser.add_argument(
    "-l", "--line", action="store_true", help="Parse input line by line"
)
parser.add_argument(
    "-a", "--all-imports", action="store_true", help="Attempt to run all imports"
)
parser.add_argument(
    "-i",
    "--import",
    dest="_import",
    help="Specify imports. Comma separated list. Use : to import from and ! to import as (ex: re,numpy!np,json:loads!jld)",
)
parser.add_argument(
    "--list",
    action="store_true",
    help="Parse each line as a list of the type specified by -t with a delimiter specified by -d",
)
parser.add_argument(
    "-d",
    "--list-delimiter",
    default=" ",
    help="The delimiter used to split each line when parsing input as a list with --list (default: ' ')",
)
parser.add_argument(
    "-f",
    "--def",
    dest="_def",
    action="store_true",
    help="Use def instead of lambda. Allows more complex functionality but needs to manually specify return to get result",
)
parser.add_argument(
    "-m",
    "--main",
    action="store_true",
    help="Run code in main body instead of lambda. Allows more complex code and does not print results if not explicitly printed",
)
parser.add_argument(
    "--pre",
    help="Code to run before starting the main command execution. Can be used for variable setup. Useful with --line.",
)
parser.add_argument(
    "--post",
    help="Code to run after the main command execution. Can be used to display results. Useful with --line.",
)
parser.add_argument(
    "--allow-priv-user-dangerous",
    action="store_true",
    help="Allow high privilege users to run this tool. This can be dangerous flag and should be treated with caution",
)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose")
parser.add_argument(
    "cmd", nargs=argparse.REMAINDER, help="Python syntax to run on the input"
)

args = parser.parse_args()

if args.cmd == []:
    args.cmd = ["_"]


def check_elevated_privileges():
    try:
        has_high_privs = geteuid() == 0
    except AttributeError:
        has_high_privs = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return has_high_privs


def parse_import(_import):
    from_start = _import.find(":")
    as_start = _import.find("!")
    if from_start == -1 and as_start == -1:
        return _import, None, None
    if from_start != -1 and as_start == -1:
        return _import[:from_start], _import[from_start + 1 :], None
    if from_start == -1 and as_start != -1:
        return _import[:as_start], None, _import[as_start + 1 :]
    return (
        _import[:from_start],
        _import[from_start + 1 : as_start],
        _import[as_start + 1 :],
    )


def smart_cast(x):
    if x.lower() == "true":
        return True
    if x.lower() == "false":
        return False
    try:
        return int(x)
    except:
        pass
    try:
        return float(x)
    except:
        pass
    try:
        return complex(x)
    except:
        pass
    return str(x)


if not args.allow_priv_user_dangerous and check_elevated_privileges():
    print(
        "You are running this script with high privileges, this is dangerous and should be treated with caution"
    )
    print(
        "If you still want to run as a high privilege user, use the --allow-priv-user-dangerous flag"
    )
    exit()


if args.line:
    reader = lambda: sys.stdin.buffer.readline().strip(b"\n")
else:
    reader = sys.stdin.buffer.read

if args.all_imports:
    for m in sys.modules.keys():
        cmd = f"import {m}"
        if args.verbose:
            print(cmd)
        exec(cmd)

if args._import:
    for _import in args._import.split(","):
        elems = parse_import(_import)
        cmd = (
            f"from {elems[0]} import {elems[1]}" if elems[1] else f"import {elems[0]}"
        ) + (f" as {elems[2]}" if elems[2] else "")
        if args.verbose:
            print(cmd)
        exec(cmd)

if args.pre:
    exec(args.pre)

while _ := reader():

    if args.input_encoding != "raw":
        _ = _.decode(args.input_encoding)

    cast_function = str

    if args.input_type == "str":
        cast_function = str
    if args.input_type == "int":
        cast_function = lambda x: int(x, 0)
    if args.input_type == "float":
        cast_function = float
    if args.input_type == "complex":
        cast_function = complex
    if args.input_type == "bool":
        cast_function = lambda x: bool(False if x.lower() in ["false"] else x)
    if args.input_type == "smart":
        cast_function = smart_cast

    if args.list:
        list_delimiter = bytes(args.list_delimiter, "utf-8").decode("unicode_escape")
        _ = [cast_function(_) for _ in _.strip().split(list_delimiter)]
    else:
        _ = cast_function(_)

    if args._def:
        cmd = f"""def __f__(_): {" ".join(args.cmd)}"""
        if args.verbose:
            print(cmd)
        exec(cmd)
        _ = __f__(_)
        print(_)
    elif args.main:
        cmd = " ".join(args.cmd)
        if args.verbose:
            print(cmd)
        exec(cmd)
    else:
        cmd = f'_ = (lambda _: {" ".join(args.cmd)})(_)'
        if args.verbose:
            print(cmd)
        exec(cmd)
        print(_)

if args.post:
    exec(args.post)
