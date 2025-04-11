from __future__ import annotations

from typing import Any, Callable

from rich.style import Style
from rich.text import Text

from slurm_viewer.data.node_model import State, Node
from slurm_viewer.data.queue_model import Queue


def format_func(value: Any, style: Style) -> Text:
    if isinstance(value, float):
        return Text(f'{value:.2f}', style=style, justify='right')

    return Text(str(value), style=style, justify='right')


UNAVAILABLE_NODES = {State.DRAIN, State.DOWN, State.MAINTENANCE, State.REBOOT_REQUESTED, State.PLANNED}
AVAILABLE_NODES = {State.MIXED, State.IDLE}


# pylint: disable=too-many-return-statements
def style_func(name: str, model: Node | Queue) -> Style:
    if name == 'node_name':
        return Style(bold=True, italic=True)

    if name == 'load_norm' and isinstance(model, Node):
        if model.load_norm < 1.0:  # type: ignore
            return Style(bgcolor='dark_green')
        if model.load_norm < 2.0:  # type: ignore
            return Style(bgcolor='orange_red1')
        return Style(bgcolor='red')

    if name == 'state' and isinstance(model, Node):
        states = model.states
        if not UNAVAILABLE_NODES.isdisjoint(states):
            # Nodes not accepting new jobs until reboot
            return Style(bgcolor='red')
        if not AVAILABLE_NODES.isdisjoint(states):
            # Nodes with available resources
            return Style(bgcolor='dark_green')
        if State.ALLOCATED in states:
            # Nodes with NO available resources
            return Style(bgcolor='orange_red1')

    return Style()


# pylint: enable=too-many-return-statements
def format_value(model: Node | Queue, key: str, _format_func: Callable[[Any, Style], Text] = format_func,
                 _style_func: Callable[[str, Node | Queue], Style] = style_func) -> Text:
    try:
        value = getattr(model, key)
    except AttributeError:
        return Text(f'Unknown key {key}')

    style = _style_func(key, model)

    if value is None:
        return _format_func('', style)

    if isinstance(value, list):
        return _format_func(','.join(map(str, value)), style)

    return _format_func(value, style)
