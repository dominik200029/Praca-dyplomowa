from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

""" Class responsible for plotting in GUI """


class Canvas:
    def __init__(self, layout):
        """ initializing Canvas in GUI """
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(NavigationToolbar(self.canvas, None))
        layout.addWidget(self.canvas)
        self.ax = self.figure.subplots()

    def plot(self, x, y, title, plot_type, x_label, y_label):
        """
            x - Horizontal Axis Data
            y - Vertical Axis Data
            title - name shown on the top of a plot
            plot_type - plot for continuous-time plotting
                        stem for discrete-time plotting
            x_label - name shown as X axis title
            y_label - name shown as Y axis title """
        if plot_type == 'stem':
            self.ax.stem(x, y)
        elif plot_type == 'plot':
            self.ax.plot(x, y)
        else:
            raise Exception('Plot type can be either "plot" or "stem"')
        # Set labels and title, then draw the canvas
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_title(title)
        self.ax.figure.canvas.draw()

    def clear_canvas(self):
        """ Clear one canvas """
        self.ax.clear()
