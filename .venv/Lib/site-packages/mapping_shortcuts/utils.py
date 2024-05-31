
from typing import Iterator, TypeVar, Union, Type, Callable, Any

T = TypeVar('T')

ParsedArgsType = dict[str, Union[str, bool, list[Union[str, bool]]]]


def parse_args(args: list[str]) -> ParsedArgsType:
    res = {}  # type: ParsedArgsType

    def insert(data: ParsedArgsType, key: str, value: Union[str, bool]) -> ParsedArgsType:
        if key in data:
            data[key] = [res[key], value]  # type: ignore[list-item]
        else:
            data[key] = value
        return data

    for st in args:
        if st.startswith('-'):
            if '=' in st:
                key, *value = st.split('=')
                res = insert(res, key, '='.join(value))
            else:
                res = insert(res, st, True)
    return res


def first(itr: Iterator[T]) -> Union[T, None]:
    try:
        return next(itr)
    except StopIteration:
        return None


def get_arg_types(func: Callable[..., Any]) -> Iterator[Type[T]]:
    annonations = getattr(func, '__annotations__', None) or {}  # type: dict[str, Type[T]]
    annonations.pop('return', None)
    yield from annonations.values()
