
import importlib
import logging
import os
import pathlib
from typing import Iterable, Optional, Union


def get_submodules(
    path: Union[str, pathlib.Path]
) -> Iterable[str]:
    if isinstance(path, str):
        path = pathlib.Path(path)

    filenames = os.listdir(path)  # type: list[str]
    for filename in filenames:
        file = path.joinpath(filename)
        if file.is_dir():
            yield from get_submodules(file)
        if file.is_file():
            if not any(file.name.startswith(x) for x in '._') and file.name.endswith('.py'):
                yield str(file)[:-3].replace('/', '.')  # 3 == len('.py')


def load_package(
    path: str,
    logger: Optional[logging.Logger] = None,
    raise_on_error: bool = False,
) -> None:
    """
        Load python package in RAM
    """
    logger = logger or logging.getLogger(__name__)
    for module_name in get_submodules(path.replace('.', '/')):
        try:
            logger.info('importing "%s"', module_name)
            importlib.import_module(module_name)
        except Exception as ex:
            if raise_on_error:
                raise ex from ex
            logger.exception('importing package "%s"', ex)
