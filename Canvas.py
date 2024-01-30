from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class Canvas:
    """
    A class representing a matplotlib canvas embedded in a PyQt5 layout.

    Attributes:
    - layout (QVBoxLayout): The vertical layout to which the canvas and navigation toolbar are added.
    - ax (Axes): The current axes of the matplotlib figure.
    """

    def __init__(self, layout):
        """
        Initializes the Canvas object.

        Parameters:
        - layout (QVBoxLayout): The vertical layout to which the canvas and navigation toolbar are added.
        """
        self.layout = layout
        figure = Figure()
        canvas = FigureCanvas(figure)
        self.layout.addWidget(NavigationToolbar(canvas))
        self.layout.addWidget(canvas)
        self.ax = figure.subplots()

    def clear(self):
        """
        Clears the content of the canvas.
        """
        self.ax.clear()
