from abc import ABC, abstractmethod


class Command(ABC):
    """
    Abstract base class for command objects.

    Attributes:
    - receiver: The receiver object that the command operates on.

    Methods:
    - execute(): Execute the command.
    """

    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        """
        Abstract method to be implemented by concrete command classes.
        """
        pass


class AddSignalCommand(Command):
    """
    Command to add a signal to the SignalsHandler.

    Attributes:
    - signals_handler: The SignalsHandler instance.
    - gui: The GUI instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller

    def execute(self):
        """
        Execute the command to add a signal to the SignalsHandler and update the GUI label.
        """
        self.receiver.add_signal_to_list(self.signals_handler, self.controller)
        self.gui.update_label(self.gui.signal_label, self.signals_handler.get_text())


class UpdatePlotsCommand(Command):
    """
    Command to update plots based on the selected option in the GUI.

    Attributes:
    - signals_handler: The SignalsHandler instance.
    - gui: The GUI instance.
    - controller: The controller instance.
    - canvas: The canvas instance.
    """

    def __init__(self, receiver, signals_handler, gui, controller, canvas):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller
        self.canvas = canvas

    def execute(self):
        """
        Execute the command to update plots based on the selected option in the GUI.
        """
        if self.gui.wave_from_file.isChecked():
            self.receiver.update_plots_from_file(self.controller, self.signals_handler, self.canvas)
        else:
            self.receiver.update_plots(self.controller, self.signals_handler, self.canvas)


class DeleteSignalCommand(Command):
    """
    Command to delete a signal from the SignalsHandler.

    Attributes:
    - signals_handler: The SignalsHandler instance.
    - gui: The GUI instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.controller = controller
        self.signals_handler = signals_handler
        self.gui = gui

    def execute(self):
        """
        Execute the command to delete a signal from the SignalsHandler and update the GUI label.
        """
        self.receiver.delete_signal(self.signals_handler, self.controller)
        self.gui.update_label(self.gui.signal_label, self.signals_handler.get_text())


class UpdateSignalCommand(Command):
    """
    Command to update the parameters of a signal in the SignalsHandler.

    Attributes:
    - signals_handler: The SignalsHandler instance.
    - gui: The GUI instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller

    def execute(self):
        """
        Execute the command to update the parameters of a signal in the SignalsHandler and update the GUI label.
        """
        self.receiver.update_signal(self.signals_handler, self.controller)
        self.gui.update_label(self.gui.signal_label, self.signals_handler.get_text())


class ChooseFileCommand(Command):
    """
    Command to open a file dialog and choose a file.

    Attributes:
    - gui: The GUI instance.
    """

    def __init__(self, receiver, gui):
        super().__init__(receiver)
        self.gui = gui

    def execute(self):
        """
        Execute the command to open a file dialog and choose a file.
        """
        self.receiver.choose_file(self.gui)


class CreateWindowCommand(Command):
    """
    Command to create and display a new figure window.

    Attributes:
    - name (str): The title of the figure window.
    """

    def __init__(self, receiver, name):
        super().__init__(receiver)
        self.name = name

    def execute(self):
        """
        Execute the command to create and display a new figure window.
        """
        self.receiver.create_figure(self.name)
