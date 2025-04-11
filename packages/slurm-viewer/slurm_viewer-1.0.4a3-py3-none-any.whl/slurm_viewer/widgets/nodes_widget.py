from __future__ import annotations

import csv
import datetime
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Any, Iterable

from loguru import logger
from rich.style import Style
from rich.text import Text
from textual import on, work
# noinspection PyProtectedMember
from textual._two_way_dict import TwoWayDict
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.css.query import NoMatches
from textual.reactive import reactive
from textual.widgets import Checkbox, Static
from textual.widgets.data_table import RowKey
from textual_sortable_datatable import SortableDataTable

from slurm_viewer.data.config import Config
from slurm_viewer.data.models import SlurmError
from slurm_viewer.data.node_model import Node
from slurm_viewer.data.slurm_communication import SlurmPermissionDenied
from slurm_viewer.data.slurm_protocol import SlurmProtocol
from slurm_viewer.widgets.loading import Loading
from slurm_viewer.widgets.screens.detail_screen import DetailScreen
from slurm_viewer.widgets.screens.select_columns_screen import SelectColumnsScreen
from slurm_viewer.widgets.table_formatting import format_value
from slurm_viewer.widgets.widget_types import AutoUpdate

COLUMN_NAME_BIDICT = TwoWayDict({
    'node_name': 'Name',
    'state': 'State',
    'gpu_tot': 'GPU (Tot)',
    'gpu_alloc': 'GPU (Alloc)',
    'gpu_avail': 'GPU (Avail)',
    'gpu_type': 'GPU (Type)',
    'gpu_mem': 'GPU (Mem)',
    'cpu_tot': 'CPU (Tot)',
    'cpu_alloc': 'CPU (Alloc)',
    'cpu_avail': 'CPU (Avail)',
    'mem_tot': 'Mem (Tot)',
    'mem_alloc': 'Mem (Alloc)',
    'mem_avail': 'Mem (Avail)',
    'cpu_gpu': 'CPUs/GPU',
    'mem_gpu': 'Mem/GPU',
    'load_norm': 'Load (Norm.)',
})


@dataclass
class FilterOptions:
    gpu: bool
    gpu_available: bool
    partition: list[str] | None


def filter_nodes(nodes: list[Node], node_filter: FilterOptions) -> list[Node]:
    result = []
    for node in nodes:
        if node_filter.gpu and node.gpu_tot == 0:
            continue

        if node_filter.gpu_available and node.gpu_avail == 0:
            continue

        if node_filter.partition and len(set(node_filter.partition) & set(node.partitions)) == 0:
            continue

        result.append(node)
    return result


def sort_column(value: Any) -> Any:
    if value is None:
        return ''

    if isinstance(value, Text):
        value = value.plain

    if isinstance(value, str):
        if value.endswith(' GB'):
            return float(value[:-len(' GB')])
        if value == '-':
            return 0

    try:
        return float(value)
    except ValueError:
        pass

    return value


def _translate_columns(node_columns: Iterable[str], inverse: bool = False) -> list[str]:
    """ Translate column names from variable names to 'human' readable and vice versa. """
    if inverse:
        return [COLUMN_NAME_BIDICT.get_key(x) or x for x in node_columns]

    return [COLUMN_NAME_BIDICT.get(x) or x for x in node_columns]


class NodesWidget(Static):
    CSS_PATH = Path(__file__) / 'slurm_viewer.tcss'

    BINDINGS = [
        Binding('c', 'columns', 'Select Columns'),
        Binding('d', 'details', 'Details'),
        Binding('g', 'gpu_only', 'GPU only', show=False),
        Binding('a', 'gpu_available', 'GPU available', show=False),
        Binding('shift+left', 'move_left', 'Column Left', show=False),
        Binding('shift+right', 'move_right', 'Column Right', show=False),
    ]

    config: reactive[Config] = reactive(Config, layout=True, always_update=True)

    def __init__(self, _slurm: SlurmProtocol, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.slurm = _slurm
        self.cluster_info: list[Node] = []
        self._map: dict[RowKey, Node] = {}

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal(id='nodes_horizontal'):
                yield Checkbox(label='GPU only', id='nodes_show_gpu')
                yield Checkbox(label='GPU available', id='nodes_show_gpu_available')
                yield Static(id='horizontal_spacer')
                yield Checkbox(label=f'Auto refresh ({self.config.ui.refresh_interval} s)', id='nodes_auto_refresh_switch',
                               value=False)
            with ScrollableContainer(id='nodes_scrollable_container'):
                table = SortableDataTable(id='nodes_data_table')
                table.sort_function = sort_column
                yield table

    @work(name='nodes_widget_watch_config')
    async def watch_config(self, _: Config, __: Config) -> None:
        if not self.is_mounted:
            return

        checkbox = self.query_one('#nodes_auto_refresh_switch', Checkbox)
        checkbox.label.styled(f'Auto refresh ({self.config.ui.refresh_interval} s)')
        checkbox.value = self.config.ui.auto_refresh

        with Loading(self):
            await self.timer_update()

    def copy_to_clipboard(self) -> None:
        with StringIO() as fp:
            fieldnames = list(self.cluster_info[0].model_dump().keys())
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for node in self.cluster_info:
                writer.writerow(node.model_dump())

        # noinspection PyUnresolvedReferences
        self.app.copy_to_clipboard(fp.getvalue())
        self.app.notify('Copied nodes to clipboard')

    async def timer_update(self) -> None:
        try:
            last_update_time = datetime.datetime.now().strftime('%A %H:%M:%S')
            self.cluster_info = await self.slurm.nodes()
            self.query_one(SortableDataTable).border_subtitle = f'Last update: {last_update_time}'
            await self.update_cluster_info()
        except SlurmPermissionDenied as e:
            self.app.notify(message=str(e), title='Permission Denied!', severity='error', timeout=20)
        except SlurmError as e:
            cluster_name = self.slurm.cluster().name
            logger.error(f'{cluster_name}, {e.func}')
            self.app.notify(title=f'[scontrol] Error retrieving data from cluster "{cluster_name}"',
                            message='Could not retrieve data from the cluster\n'
                                    f'See {(Path.cwd() / "slurm_viewer.log").absolute()} for more information',
                            severity='error', timeout=15)

    @on(Checkbox.Changed, '#nodes_auto_refresh_switch')
    def on_auto_refresh(self, event: Checkbox.Changed) -> None:
        self.post_message(AutoUpdate.Changed(event.control.value))

    @on(Checkbox.Changed, '#nodes_show_gpu')
    @on(Checkbox.Changed, '#nodes_show_gpu_available')
    async def show_gpu(self, _: Checkbox.Changed) -> None:
        await self.update_cluster_info()

    def _checkbox_values(self) -> dict[str, bool]:
        return {x.label.plain: x.value for x in self.query(Checkbox).nodes}

    async def update_cluster_info(self) -> None:
        try:
            data_table = self.query_one(SortableDataTable)
        except NoMatches:
            return

        old_sort_label = data_table.sort_column_label
        old_sort_direction = data_table.sort_column.direction

        data_table.cursor_type = 'row'
        data_table.clear(columns=True)
        data_table.zebra_stripes = True
        data_table.add_columns(*_translate_columns(self.config.ui.node_columns))

        checkboxes = self._checkbox_values()
        options = FilterOptions(gpu=checkboxes['GPU only'], gpu_available=checkboxes['GPU available'],
                                partition=self.slurm.cluster().partitions)
        self._update_data_table(filter_nodes(self.cluster_info, options), data_table)

        if old_sort_label is not None:
            data_table.sort_on_column(old_sort_label, direction=old_sort_direction)

    def _update_data_table(self, nodes: list[Node], table: SortableDataTable) -> None:
        self._map.clear()
        table.border_title = f'{len(nodes)} nodes'
        for node in nodes:
            row_data = []
            for x in self.config.ui.node_columns:
                try:
                    row_data.append(format_value(node, x))
                except AttributeError:
                    row_data.append(Text('Unknown column', style=Style(bgcolor='red')))
            row_key = table.add_row(*row_data)
            self._map[row_key] = node

    def action_details(self) -> None:
        data_table = self.query_one(SortableDataTable)
        selected = data_table.coordinate_to_cell_key(data_table.cursor_coordinate).row_key
        node = self._map[selected]
        self.app.push_screen(DetailScreen(node))

    async def action_columns(self) -> None:
        async def check_result(selected: list[str] | None) -> None:
            if selected is None:
                return

            self.config.ui.node_columns = _translate_columns(selected, inverse=True)
            await self.update_cluster_info()

        current_columns = [x.label.plain for x in self.query_one('#nodes_data_table', SortableDataTable).columns.values()]
        current_columns = _translate_columns(current_columns, inverse=True)

        # noinspection PyUnresolvedReferences
        all_columns = list(Node.model_fields.keys())
        all_columns.extend([name for name, value in vars(Node).items() if isinstance(value, property)])

        remaining_columns = sorted(set(all_columns) - set(current_columns))

        await self.app.push_screen(
            SelectColumnsScreen(_translate_columns(current_columns),
                                _translate_columns(remaining_columns)), check_result)

    async def action_move_left(self) -> None:
        table = self.query_one('#nodes_data_table', SortableDataTable)
        if table.cursor_column == 0:
            return

        self.config.ui.node_columns.insert(table.cursor_column - 1, self.config.ui.node_columns.pop(table.cursor_column))
        old_pos = table.cursor_coordinate

        await self.update_cluster_info()

        table.cursor_coordinate = old_pos.left()

    async def action_move_right(self) -> None:
        table = self.query_one('#nodes_data_table', SortableDataTable)
        if table.cursor_column == len(table.columns) - 1:
            return

        self.config.ui.node_columns.insert(table.cursor_column + 1, self.config.ui.node_columns.pop(table.cursor_column))
        old_pos = table.cursor_coordinate

        await self.update_cluster_info()

        table.cursor_coordinate = old_pos.right()

    async def action_gpu_only(self) -> None:
        checkbox = self.query_one('#nodes_show_gpu', Checkbox)
        checkbox.value = not checkbox.value

    async def action_gpu_available(self) -> None:
        checkbox = self.query_one('#nodes_show_gpu_available', Checkbox)
        checkbox.value = not checkbox.value
