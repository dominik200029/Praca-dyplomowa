from matplotlib import pyplot as plt


class Figure:
    """
    A class for creating and managing matplotlib figures.

    Attributes:
    - title: str, the title of the figure
    - figure: matplotlib.figure.Figure or None, the created figure object

    Methods:
    - create: Create a new matplotlib figure with the specified title.
    - show: Display all figures.
    - get_figure_by_name: Retrieve a figure by its title.
    """

    def __init__(self, title):
        """
        Initialize a Figure instance.

        Parameters:
        - title: str, the title of the figure
        """
        self.title = title
        self.figure = None

    def create(self):
        """
        Create a new matplotlib figure with the specified title.
        """
        self.figure = plt.figure(self.title)

    @staticmethod
    def show():
        """
        Display all figures.
        """
        plt.show()

    @staticmethod
    def get_figure_by_name(title):
        """
        Retrieve a figure by its title.

        Parameters:
        - title: str, the title of the figure to retrieve

        Returns:
        - matplotlib.figure.Figure or None, the retrieved figure object, or None if not found
        """
        for fig_num in plt.get_fignums():
            fig = plt.figure(fig_num)
            if fig.canvas.manager.get_window_title() == title:
                return fig
        return None

