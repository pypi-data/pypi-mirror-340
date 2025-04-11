import json
import typing


def tojson(obj: typing.Any, indent: int = 2) -> str:
    return json.dumps(obj, indent=indent, ensure_ascii=False, default=str)


def fromjson(text: str) -> typing.Any:
    return json.loads(text)


def check(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False
