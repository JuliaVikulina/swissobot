# coding=utf-8

import logging
from collections import namedtuple
from typing import Optional

log = logging.getLogger(__name__)

BOT_NAME = '@DnJTodoBot'
SEPARATOR = ';'

Command = namedtuple('Command', 'name, max_operands, format, example')

MONEY_COMMAND = Command(name='money', max_operands=3, format='/money сумма [; цель; дата]',
                        example='/money 100; котята; 02-23')

MONEY_LIST_COMMAND = Command(name='moneylist', max_operands=1, format='/moneylist [дата]',
                             example='/moneylist 02-23')

TASK_DELETE_COMMAND = Command(name='taskdelete', max_operands=1, format='/taskdelete [id]',
                             example='/taskdelete 76')

MONEY_EDIT_COMMAND = Command(name='moneyedit', max_operands=5, format='/moneyedit id[; дата; категория; сумма; цель]',
                        example='/moneyedit 100; 02-23; Подарки; 200; котята')

DIARY_COMMAND = Command(name='diary', max_operands=1, format='/diary text',
                        example='/diary what a great day today!')


def get_operands(command: Command, message: str) -> list:
    """Parses message string and retrieves command operands

    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot 100; test; 02-15")
    ['100', 'test', '02-15']
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot 100; test")
    ['100', 'test', None]
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot 100; test; ")
    ['100', 'test', None]
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot 100; ; 02-15")
    ['100', None, '02-15']
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot 100; ; ")
    ['100', None, None]
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot  ; ; ")
    [None, None, None]
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot  ; ")
    [None, None, None]
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot")
    [None, None, None]
    >>> get_operands(MONEY_COMMAND, "")
    [None, None, None]
    >>> get_operands(MONEY_COMMAND, "/money@DnJTodoBot asdf;asdf;asdf;asdf")
    Traceback (most recent call last):
    ...
    ValueError: Too many arguments
    >>> get_operands('WOW', "")
    Traceback (most recent call last):
    ...
    ValueError: Illegal argument types: expected 'Command', actual 'str'
    >>> get_operands(None, "")
    Traceback (most recent call last):
    ...
    ValueError: Illegal argument types: expected 'Command', actual 'NoneType'
    """

    if not isinstance(command, Command):
        raise ValueError("Illegal argument types: "
                         "expected '{type_expected}', "
                         "actual '{type_actual}'".format(type_expected=Command.__name__,
                                                         type_actual=type(command).__name__))
    operands = message.replace('/{}'.format(command.name), '').replace(BOT_NAME, '').strip().split(SEPARATOR)
    result = []

    if len(operands) > command.max_operands:
        raise ValueError("Too many arguments")

    for i, _ in enumerate(operands):
        result.append(operands[i].strip())
        if result[i] is "":
            result[i] = None

    while len(result) < command.max_operands:
        result.append(None)

    return result


def handle_error(bot, update, command: Optional[Command], custom_msg: str ='', exception: Exception = None):
    if command is None:
        msg = 'An error occurred'
    else:
        msg = '{custom_msg}\n{format}\n{example}'.format(custom_msg=custom_msg,
                                                         format=command.format,
                                                         example=command.example)
    if exception is not None:
        log.error(exception)
        msg += "\n{}".format(str(exception))

    bot.sendMessage(chat_id=update.message.chat_id, text=msg)

if __name__ == "__main__":
    import doctest

    doctest.testmod()
