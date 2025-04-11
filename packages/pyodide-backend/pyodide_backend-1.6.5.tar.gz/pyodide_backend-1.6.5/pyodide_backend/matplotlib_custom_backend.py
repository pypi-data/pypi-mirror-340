from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib._pylab_helpers import Gcf
from matplotlib.backend_bases import FigureManagerBase
from matplotlib.figure import Figure

from .process import trigger_matplotlib_show_callback


def draw_if_interactive():
    pass


def show():
    fig_manager = Gcf.get_active()
    if fig_manager is not None:
        trigger_matplotlib_show_callback(fig_manager.canvas)
        Gcf.destroy_all()


def new_figure_manager(num, *args, **kwargs):
    FigureClass = kwargs.pop("FigureClass", Figure)
    thisFig = FigureClass(*args, **kwargs)
    return new_figure_manager_given_figure(num, thisFig)


def new_figure_manager_given_figure(num, figure):
    canvas = FigureCanvasSVG(figure)
    manager = FigureManagerBase(canvas, num)
    return manager


FigureCanvas = FigureCanvasSVG
