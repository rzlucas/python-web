
from typing import Union

from .cli import CMD_HANDLERS, cli_handler
from . import consts


@cli_handler('help', desc='see this cool msg again')
def help_handler(args: dict[str, Union[str, bool]]) -> None:
    rows = []
    for handler in CMD_HANDLERS.values():
        rows.append(f'\t{handler.cmd} - {handler.desc}')
        if handler.model:
            rows.extend(
                [
                    f'\t\t{key} - {value.get("description", "")}'
                    for key, value in handler.model.schema()['properties'].items()
                ]
            )

    txt = consts.HELP_TEMPLATE.format(
        header=consts.HELP_MSG_TEMPLATE_HEADER,
        run_cmd=consts.HELP_MSG_RUN_CMD,
        commands='\n'.join(rows),
    )
    print(txt)
