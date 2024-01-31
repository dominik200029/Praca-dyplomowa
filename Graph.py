import matplotlib.pyplot as plt
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
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        self.x = x
        self.y = y
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title

    @abstractmethod
    def create(self, figure):
        """
        Abstract method for creating the graph on a provided figure.

        Parameters:
        - figure: matplotlib.figure.Figure, the figure on which the graph will be created
        """
        pass

    @abstractmethod
    def create_on_canvas(self, canvas: Canvas):
        """
        Abstract method for creating the graph on a provided canvas.

        Parameters:
        - canvas: Canvas, the canvas on which the graph will be created
        """
        pass


class Plot(Graph):
    """
    Class for creating a line plot.

    Inherits from Graph.

    Methods:
    - create: Create a line plot on a given figure.
    - create_on_canvas: Create a line plot on a given canvas.
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        super().__init__(x, y, xlabel, ylabel, title)

    def create(self, figure):
        """
        Create a line plot on a given figure.

        Parameters:
        - figure: matplotlib.figure.Figure, the figure on which the line plot will be created
        """
        ax = figure.gca()
        ax.plot(self.x, self.y)
        plt.draw()

    def create_on_canvas(self, canvas: Canvas):
        """
        Create a line plot on a given canvas.

        Parameters:
        - canvas: Canvas, the canvas on which the line plot will be created
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
    - create: Create a stem plot on a given figure.
    - create_on_canvas: Create a stem plot on a given canvas.
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        super().__init__(x, y, xlabel, ylabel, title)

    def create(self, figure):
        """
        Create a stem plot on a given figure.

        Parameters:
        - figure: matplotlib.figure.Figure, the figure on which the stem plot will be created
        """
        ax = figure.gca()
        ax.stem(self.x, self.y)
        ax.set_xlabel(self.xlabel)
        ax.set_ylabel(self.ylabel)
        ax.set_title(self.title)
        ax.figure.canvas.draw()

    def create_on_canvas(self, canvas: Canvas):
        """
        Create a stem plot on a given canvas.

        Parameters:
        - canvas: Canvas, the canvas on which the stem plot will be created
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


class ImagePlot(Graph):
    """
    Class for creating an image plot.

    Inherits from Graph.

    Methods:
    - create: Placeholder method for creating an image plot on a given figure.
    - create_on_canvas: Create an image plot on a given canvas.
    """

    def __init__(self, x, y, xlabel, ylabel, title):
        super().__init__(x, y, xlabel, ylabel, title)

    def create(self, figure):
        """
        Placeholder method for creating an image plot on a given figure.

        Parameters:
        - figure: matplotlib.figure.Figure, the figure on which the image plot will be created
        """
        pass

    def create_on_canvas(self, canvas: Canvas):
        """
        Create an image plot on a given canvas.

        Parameters:
        - canvas: Canvas, the canvas on which the image plot will be created
        """
        canvas.ax.imshow(self.y)
        canvas.ax.set_title(self.title)
        canvas.ax.axis('off')  # Turn off axis labels
        canvas.ax.figure.canvas.draw()
