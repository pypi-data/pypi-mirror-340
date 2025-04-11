import contextlib
import re
import typing
import unicodedata

from gadify import const


def strip(string: str, clean: bool = True, chars: str = const.SYMBOL_EMPTY) -> str:
    return string.strip(chars) if clean else string


def normalized(string: str, clean: bool = True) -> str:
    return (
        unicodedata.normalize(const.UNICODE_NORMALIZATION_FORM, strip(string, clean))
        .encode(const.ENCODING_ASCII, const.ENCODING_ERROR_IGNORE)
        .decode(const.ENCODING_ASCII)
    )


def compact(string: str, clean: bool = True) -> str:
    return const.SYMBOL_WHITESPACE.join(strip(string, clean).split())


def truncate(string: str, length: int, clean: bool = True) -> str:
    string = strip(string, clean)
    if len(string) <= length:
        return string
    return string[: length - len(const.SYMBOL_TRUNCATION)] + const.SYMBOL_TRUNCATION


def remove(string: str, prefix: str = None, suffix: str = None, clean: bool = True) -> str:
    string = strip(string, clean)
    if prefix:
        string = string.removeprefix(prefix)
    if suffix:
        string = string.removesuffix(suffix)
    return string


def empty(string: str, clean: bool = True) -> bool:
    return not bool(strip(string, clean))


def number(string: str, clean: bool = True) -> bool:
    with contextlib.suppress(ValueError):
        float(strip(string, clean))
        return True
    return False


def count(string: str, clean: bool = True) -> int:
    return len(strip(string, clean))


def lower(string: str, clean: bool = True) -> str:
    return strip(string, clean).lower()


def upper(string: str, clean: bool = True) -> str:
    return strip(string, clean).upper()


def title(string: str, clean: bool = True) -> str:
    return strip(string, clean).title()


def capitalize(string: str, clean: bool = True) -> str:
    return strip(string, clean).capitalize()


def sentence(string: str, clean: bool = True) -> str:
    string = strip(string, clean)
    if words := re.split(const.REGEXP_NON_ALPHANUMERIC, string):
        return const.SYMBOL_WHITESPACE.join([capitalize(words[0])] + [lower(word) for word in words[1:] if word])
    else:
        return string


def acronym(string: str, clean: bool = True) -> str:
    words = re.split(const.REGEXP_NON_ALPHANUMERIC, strip(string, clean))
    return const.SYMBOL_EMPTY.join(upper(word[0]) for word in words if word)


def snake(string: str, clean: bool = True) -> str:
    words = re.split(const.REGEXP_NON_ALPHANUMERIC, strip(string, clean))
    return const.SYMBOL_LOWER_HYPHEN.join(lower(word) for word in words if word)


def camel(string: str, clean: bool = True) -> str:
    string = strip(string, clean)
    if words := re.split(const.REGEXP_NON_ALPHANUMERIC, strip(string, clean)):
        return lower(words[0]) + const.SYMBOL_EMPTY.join(capitalize(word) for word in words[1:] if word)
    else:
        return string


def pascal(string: str, preserve: bool = True, clean: bool = True) -> str:
    string = strip(string, clean)
    if words := re.split(const.REGEXP_NON_ALPHANUMERIC, string):
        result = []
        for word in words:
            if not word:
                continue
            if preserve and word.isupper():
                result.append(word)
            else:
                result.append(word.capitalize())
        return const.SYMBOL_EMPTY.join(result)
    else:
        return string


def kebab(string: str, clean: bool = True) -> str:
    words = re.split(const.REGEXP_NON_ALPHANUMERIC, strip(string, clean))
    return const.SYMBOL_HYPHEN.join(lower(word) for word in words if word)


def words(string: str, clean: bool = True) -> typing.List[str]:
    return [word for word in re.split(const.REGEXP_NON_ALPHANUMERIC, strip(string, clean)) if word]


def split(string: str, separator: str = const.SYMBOL_WHITESPACE, clean: bool = True) -> typing.List[str]:
    return strip(string, clean).split(separator)


def join(words: typing.List[str], separator: str = const.SYMBOL_WHITESPACE, clean: bool = True) -> str:
    return separator.join([strip(word, clean) for word in words])


def splitlines(string: str, clean: bool = True) -> typing.List[str]:
    return strip(string, clean).splitlines()
