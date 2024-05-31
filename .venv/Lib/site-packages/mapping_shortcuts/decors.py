
from typing import Callable, Type, TypeVar, Union, cast

KT = TypeVar('KT')
VT = TypeVar('VT')
WrapType = Callable[[VT], VT]
DecoratorType = Callable[[KT], WrapType[VT]]
CollectionType = dict[KT, VT]

ClassDecoratorType = Callable[[Union[KT, VT]], Union[VT, Callable[[VT], VT]]]
ClassCollectionType = dict[KT, VT]


def create_collector(
    raise_on_duplicate: bool = True,
) -> tuple[DecoratorType[KT, VT], CollectionType[KT, VT]]:
    def decor(key: KT) -> WrapType[VT]:
        def wrap(func: VT) -> VT:
            if key in collection and raise_on_duplicate:
                raise ValueError(f'Duplication for key {key}')
            collection[key] = func
            return func
        return wrap
    collection = {}  # type: CollectionType[KT, VT]
    return decor, collection


def create_class_collector(
    raise_on_duplicate: bool = True,
    key_getter: Callable[[Type[VT]], KT] = lambda x: x.__name__  # type: ignore[assignment,return-value]
) -> tuple[ClassDecoratorType[KT, Type[VT]], CollectionType[KT, Type[VT]]]:
    def decor(cls: Union[KT, Type[VT]]) -> Union[Type[VT], Callable[[Type[VT]], Type[VT]]]:

        def wrap(cls: Type[VT]) -> Type[VT]:
            if key in collection and raise_on_duplicate:
                raise ValueError(f'Duplication for key {key}')
            collection[key] = cls
            return cls

        if isinstance(cls, type):
            cls = cast(Type[VT], cls)
            key = key_getter(cls)  # type: KT
            return wrap(cls)

        key = cls
        return wrap

    collection = {}  # type: CollectionType[KT, Type[VT]]
    return decor, collection
