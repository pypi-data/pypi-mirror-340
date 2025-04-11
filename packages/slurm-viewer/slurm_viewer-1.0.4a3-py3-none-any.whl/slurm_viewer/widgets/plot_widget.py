import csv
import datetime
from datetime import date, timedelta
from io import StringIO
from pathlib import Path
from typing import Any

from loguru import logger
from textual import on, work
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.events import Show
from textual.reactive import reactive
from textual.widgets import Static
from textual_plotext import PlotextPlot

from slurm_viewer.data.config import Config
from slurm_viewer.data.job_model import Job
from slurm_viewer.data.models import SlurmError
from slurm_viewer.data.queue_model import JobStateCodes
from slurm_viewer.data.slurm_communication import SlurmPermissionDenied
from slurm_viewer.data.slurm_protocol import SlurmProtocol
from slurm_viewer.widgets.loading import Loading


def _filter_data(data: list[Job]) -> tuple[list[Job], list[Job]]:
    filtered_data = []
    errors = []
    for job in data:
        if job.AllocTRES.gpu is None:
            continue

        if not job.TRESUsageInMax.gpu_mem or not job.TRESUsageInMax.gpu_mem.value:
            continue

        if job.TRESUsageInMax.gpu_mem.GB < 1:
            continue

        if job.Elapsed < timedelta(seconds=60):
            continue

        if job.TRESUsageInMax.gpu_util is not None and job.TRESUsageInMax.gpu_util > 100:
            errors.append(job)
            continue

        if job.State not in (JobStateCodes.COMPLETED, JobStateCodes.CANCELLED):
            continue

        filtered_data.append(job)
    return filtered_data, errors


class PlotWidget(Static):
    DEFAULT_CSS = """
    PlotextPlot {
        border: $foreground 80%;
    }
    """
    CSS_PATH = Path(__file__) / 'slurm_viewer.tcss'

    config: reactive[Config] = reactive(Config, layout=True, always_update=True)

    def __init__(self, _slurm: SlurmProtocol, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.slurm = _slurm
        self.gpu_usage: list[Job] = []
        self.gpu_history = 4  # weeks

    def compose(self) -> ComposeResult:
        with Vertical():
            yield PlotextPlot(id='gpu_mem_plot')
            yield PlotextPlot(id='gpu_util_plot')

    @work
    async def watch_config(self, _: Config, __: Config) -> None:
        if not self.is_mounted:
            return

        await self.timer_update()

    @on(Show)
    async def _first_show(self, _: Show) -> None:
        if len(self.gpu_usage) == 0:
            await self.timer_update()

    async def timer_update(self) -> None:
        if not self.is_on_screen:
            return

        with Loading(self):
            try:
                self.gpu_usage = await self.slurm.jobs(self.gpu_history, self.config.ui.user_only)
                self.update_plot(self.config.ui.user_only)
            except SlurmPermissionDenied as e:
                self.app.notify(message=str(e), title='Permission Denied!', severity='error', timeout=20)
            except SlurmError as e:
                cluster_name = self.slurm.cluster().name
                logger.error(f'{cluster_name}, {e.func}')
                self.app.notify(title=f'[sacct] Error retrieving data from cluster "{cluster_name}"',
                                message='Could not retrieve data from the cluster\n'
                                        f'See {(Path.cwd() / "slurm_viewer.log").absolute()} for more information',
                                severity='error', timeout=15)

    def copy_to_clipboard(self) -> None:
        with StringIO() as fp:
            data, _ = _filter_data(self.gpu_usage)

            if len(data) == 0:
                self.app.notify('No data to copy')
                return

            fieldnames = list(data[0].model_dump().keys())
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for node in data:
                writer.writerow(node.model_dump())

        # noinspection PyUnresolvedReferences
        self.app.copy_to_clipboard(fp.getvalue())
        self.app.notify('Copied GPU info to clipboard')

    @work
    async def update_plot(self, user_only: bool) -> None:
        last_update_time = datetime.datetime.now().strftime('%A %H:%M:%S')

        data, errors = _filter_data(self.gpu_usage)
        if len(errors) > 0:
            self.notify(f'{len(errors)} unreliable jobs found (caused by nvidia-smi). This data has been excluded.')

        end = date.today()
        start = end - timedelta(weeks=self.gpu_history)
        time_string = f'from {start:%A %d %B} until {end:%A %d %B}'

        gpu_mem_data = [job.TRESUsageInMax.gpu_mem.GB for job in data]  # type: ignore
        plotextplot = self.query_one('#gpu_mem_plot', PlotextPlot)
        plotextplot.border_subtitle = f'Last update: {last_update_time}'
        plt = plotextplot.plt
        plt.clear_figure()
        bins = 24
        plt.hist(gpu_mem_data, bins)
        plt.title(f'GPU memory histogram {time_string} ({len(gpu_mem_data)} jobs for {"User" if user_only else "All"})')
        plt.xlabel('GPU Mem (GB)')
        plt.ylabel('# jobs')
        plotextplot.refresh()

        gpu_util_data = [job.TRESUsageInMax.gpu_util for job in data]
        plotextplot = self.query_one('#gpu_util_plot', PlotextPlot)
        plotextplot.border_subtitle = f'Last update: {last_update_time}'
        plt = plotextplot.plt
        plt.clear_figure()
        bins = 25
        plt.hist(gpu_util_data, bins)
        plt.title(f'GPU utilization histogram {time_string} ({len(gpu_util_data)} jobs)')
        plt.xlabel('GPU utilization (%)')
        plt.ylabel('# jobs')
        plotextplot.refresh()
