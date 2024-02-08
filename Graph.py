from Canvas import Canvas
from abc import ABC, abstractmethod


class Graph(ABC):
    """
    Abstract base class for creating graphs.

    Attributes:
    - x: List or array-like, x-axis data
    - y: List or array-like, y-axis data
    - xlabel: str, label for x-axis
    - ylabel: str, label for y-axis
    - title: str, title of the graph

    Methods:
    - create_on_canvas(self, canvas: Canvas): Abstract method for creating the graph on a provided canvas.
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        """
        Initialize a Graph instance.

        Parameters:
            x: List or array-like, x-axis data
            y: List or array-like, y-axis data
            xlabel: str, label for x-axis
            ylabel: str, label for y-axis
            title: str, title of the graph
        """
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

    @abstractmethod
    def create_on_canvas(self, canvas: Canvas):
        """
        Abstract method for creating the graph on a provided canvas.

        Parameters:
            canvas (Canvas): The canvas on which the graph will be created.
        """
        pass


class Plot(Graph):
    """
    Class for creating a line plot.

    Inherits from Graph.

    Methods:
    - create_on_canvas(self, canvas: Canvas): Create a line plot on a given canvas.
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        """
        Initialize a Plot instance.

        Parameters:
            x: List or array-like, x-axis data
            y: List or array-like, y-axis data
            xlabel: str, label for x-axis
            ylabel: str, label for y-axis
            title: str, title of the graph
        """
        super().__init__(x, y, xlabel, ylabel, title)

    def create_on_canvas(self, canvas: Canvas):
        """
        Create a line plot on a given canvas.

        Parameters:
            canvas (Canvas): The canvas on which the line plot will be created.
        """
        if self.x is None:
            canvas.ax.plot(self.y)
        else:
            canvas.ax.plot(self.x, self.y)
        canvas.ax.axhline(y=0, color='r', linestyle='-', linewidth=2)
        canvas.ax.set_xlabel(self.xlabel)
        canvas.ax.set_ylabel(self.ylabel)
        canvas.ax.set_title(self.title)
        canvas.ax.grid(True)
        canvas.ax.figure.canvas.draw()


class StemPlot(Graph):
    """
    Class for creating a stem plot.

    Inherits from Graph.

    Methods:
    - create_on_canvas(self, canvas: Canvas): Create a stem plot on a given canvas.
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        """
        Initialize a StemPlot instance.

        Parameters:
            x: List or array-like, x-axis data
            y: List or array-like, y-axis data
            xlabel: str, label for x-axis
            ylabel: str, label for y-axis
            title: str, title of the graph
        """
        super().__init__(x, y, xlabel, ylabel, title)

    def create_on_canvas(self, canvas: Canvas):
        """
        Create a stem plot on a given canvas.

        Parameters:
            canvas (Canvas): The canvas on which the stem plot will be created.
        """
        if self.x is None:
            canvas.ax.stem(self.y)
        else:
            canvas.ax.stem(self.x, self.y)
        canvas.ax.axhline(y=0, color='r', linestyle='-', linewidth=2)
        canvas.ax.set_xlabel(self.xlabel)
        canvas.ax.set_ylabel(self.ylabel)
        canvas.ax.set_title(self.title)
        canvas.ax.grid(True)
        canvas.ax.figure.canvas.draw()


class EmptyPlot(Graph):
    """
    Class for creating an empty plot with a title.

    Inherits from Graph.

    Methods:
    - create_on_canvas(self, canvas: Canvas): Create an empty plot on a given canvas with a title.
    """

    def __init__(self, title):
        """
        Initialize an EmptyPlot instance.

        Parameters:
            title: str, title of the empty plot
        """
        super().__init__(None, None, None, None, title)

    def create_on_canvas(self, canvas: Canvas):
        """
        Create an empty plot on a given canvas with a title.

        Parameters:
            canvas (Canvas): The canvas on which the empty plot will be created.
        """
        canvas.ax.set_title(self.title)
        canvas.ax.figure.canvas.draw()


class ImagePlot(Graph):
    """
    Class for creating an image plot.

    Inherits from Graph.

    Methods:
    - create_on_canvas(self, canvas: Canvas): Create an image plot on a given canvas.
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        """
        Initialize an ImagePlot instance.

        Parameters:
            x: List or array-like, x-axis data
            y: List or array-like, y-axis data
            xlabel: str, label for x-axis
            ylabel: str, label for y-axis
            title: str, title of the image plot
        """
        super().__init__(x, y, xlabel, ylabel, title)

    def create_on_canvas(self, canvas: Canvas):
        """
        Create an image plot on a given canvas.

        Parameters:
            canvas (Canvas): The canvas on which the image plot will be created.
        """
        canvas.ax.imshow(self.y, cmap='gray')
        canvas.ax.set_title(self.title)
        canvas.ax.figure.canvas.draw()
