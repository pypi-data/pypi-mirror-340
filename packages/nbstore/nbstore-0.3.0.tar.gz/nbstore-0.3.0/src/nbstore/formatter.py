from __future__ import annotations

import base64
import io
import tempfile
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from IPython.lib.pretty import RepresentationPrinter
    from matplotlib.figure import Figure
    from seaborn.objects import Plot


def matplotlib_figure_to_pgf(fig: Figure, rp: RepresentationPrinter, cycle) -> None:
    name = str(uuid.uuid4())

    with tempfile.TemporaryDirectory() as dirname:
        directory = Path(dirname)
        filename = f"{name}.pgf"
        path = directory / filename
        fig.savefig(path, format="pgf", bbox_inches="tight")
        text = path.read_text(encoding="utf-8")

        imagenames = [x.name for x in directory.iterdir() if x.name != filename]
        if not imagenames:
            return rp.text(text)

        for name in imagenames:
            text = text.replace(name, _encode_pgf_text(name, directory))

        return rp.text(text)


def _encode_pgf_text(name: str, directory: Path) -> str:
    ext = name.rsplit(".", 1)[-1]
    data = (directory / name).read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:image/{ext};base64,{b64}"


def matplotlib_figure_to_pdf(fig: Figure) -> bytes:
    with io.BytesIO() as fp:
        fig.savefig(fp, format="pdf", bbox_inches="tight")
        return fp.getvalue()


def matplotlib_figure_to_svg(fig: Figure) -> str:
    with io.StringIO() as fp:
        fig.savefig(fp, format="svg", bbox_inches="tight")
        return fp.getvalue()


def seaborn_plot_to_pgf(plot: Plot, rp: RepresentationPrinter, cycle) -> None:
    from seaborn._core.plot import theme_context

    plotter = plot.plot()
    with theme_context(plotter._theme):  # type: ignore
        return matplotlib_figure_to_pgf(plotter._figure, rp, cycle)  # type: ignore


def seaborn_plot_to_pdf(plot: Plot) -> bytes:
    from seaborn._core.plot import theme_context

    plotter = plot.plot()
    with theme_context(plotter._theme):  # type: ignore
        return matplotlib_figure_to_pdf(plotter._figure)  # type: ignore


def seaborn_plot_to_svg(plot: Plot) -> str:
    from seaborn._core.plot import theme_context

    plotter = plot.plot()
    with theme_context(plotter._theme):  # type: ignore
        return matplotlib_figure_to_svg(plotter._figure)  # type: ignore


MIMES: dict[str, str] = {
    "pgf": "text/plain",
    "pdf": "application/pdf",
    "svg": "image/svg+xml",
}

MODULE_CLASSES: dict[str, list[tuple[str, str]]] = {
    "matplotlib": [("matplotlib.figure", "Figure")],
    "seaborn": [("seaborn._core.plot", "Plot")],
}

FUNCTIONS: dict[tuple[str, str], dict[str, Callable]] = {
    ("matplotlib.figure", "Figure"): {
        "pgf": matplotlib_figure_to_pgf,
        "pdf": matplotlib_figure_to_pdf,
        "svg": matplotlib_figure_to_svg,
    },
    ("seaborn._core.plot", "Plot"): {
        "pgf": seaborn_plot_to_pgf,
        "pdf": seaborn_plot_to_pdf,
        "svg": seaborn_plot_to_svg,
    },
}


try:
    from holoviews.ipython.display_hooks import display_hook, image_display

    @display_hook
    def pgf_display(element, max_frames):
        """Used to render elements to PGF if requested in the display formats."""
        return image_display(element, max_frames, fmt="pgf")

except ModuleNotFoundError:  # no cov
    pgf_display = None  # type: ignore


def set_formatter_holoviews(fmt: str) -> None:
    from holoviews.core.dimension import LabelledData
    from holoviews.core.options import Store

    if fmt not in Store.display_formats:
        Store.display_formats.append(fmt)

    if fmt == "pgf" and pgf_display:
        Store.set_display_hook(fmt, LabelledData, pgf_display)


def set_formatter(module: str, fmt: str, ip=None) -> None:
    if module == "holoviews":
        set_formatter_holoviews(fmt)
        return

    try:
        from IPython.core.getipython import get_ipython
    except ModuleNotFoundError:  # no cov
        msg = "IPython is not installed"
        raise ModuleNotFoundError(msg) from None

    if not ip and not (ip := get_ipython()):
        return

    if not (mime := MIMES.get(fmt)):
        raise NotImplementedError

    formatter = ip.display_formatter.formatters[mime]  # type:ignore

    if module_classes := MODULE_CLASSES.get(module):
        for module_class in module_classes:
            if function := FUNCTIONS.get(module_class, {}).get(fmt):
                formatter.for_type_by_name(*module_class, function)
