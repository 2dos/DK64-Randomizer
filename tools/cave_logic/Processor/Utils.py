import ast
import inspect
import json
from copy import deepcopy
from tools.cave_logic.ast_logic import ast_to_json

def try_parse_ast(req_str):
    try:
        req = ast.parse(req_str)
    except SyntaxError as e:
        if "was never closed" in str(e):
            req_str += ")"
            req = try_parse_ast(req_str)
        else:
            raise e
    return req


def parse_ast_by_separator(source, separator, backup_separator="logic=lambda l: "):
    req_str = inspect.getsource(source)
    if separator is None:
        req_str = req_str.split("#")[0].strip().strip(",").strip(")")
    elif separator in req_str:
        req_str = separator + \
            req_str.split(separator)[1].split(
                "#")[0].strip().strip(",").strip(")")
    else:
        req_str = backup_separator + \
            req_str.split(backup_separator)[1].split(
                "#")[0].strip().strip(",").strip(")")
    # req_str = separator + req_str.split(separator)[1].strip().strip(",").strip(")")
    req = try_parse_ast(req_str)
    return req


def parse_ast_to_dict(source, separator):
    req = parse_ast_by_separator(source, separator)
    req_ast = req.body[0].value
    req2 = ast_to_json(req_ast, {"direct": True})

    return req2["Requires"] if req2 is not None else True
