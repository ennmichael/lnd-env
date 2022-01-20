import typing as t
import json

def pretty_print(obj: t.Any) -> None:
    if isinstance(obj, str):
        print(obj)
    else:
        print(json.dumps(obj, indent=1))
