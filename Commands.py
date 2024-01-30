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

    def __init__(self, receiver, signals_handler, controller):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.controller = controller

    def execute(self):
        """
        Execute the command to add a signal to the SignalsHandler and update the GUI label.
        """
        self.receiver.add_signal_to_list(self.signals_handler, self.controller)
        self.controller.update_label(self.controller.signal_label, self.signals_handler.get_text())


class UpdatePlotsCommand(Command):
    """
    Command to update plots based on the selected option in the GUI.

    Attributes:
    - signals_handler: The SignalsHandler instance.
    - gui: The GUI instance.
    - controller: The controller instance.
    - canvas: The canvas instance.
    """

    def __init__(self, receiver, signals_handler, controller, *canvases):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.controller = controller
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to update plots based on the selected option in the GUI.
        """
        self.receiver.calculate_axis(self.controller)
        self.receiver.calculate_wave(self.signals_handler)
        self.receiver.calculate_fft()
        self.receiver.calculate_dct()

        self.receiver.update_signal_plot(self.canvases[0])
        self.receiver.update_fft_plot(self.canvases[1])
        self.receiver.update_ifft_plot(self.canvases[2])
        self.receiver.update_dct_plot(self.canvases[3])
        self.receiver.update_idct_plot(self.canvases[4])


class UpdatePlotsFromFileCommand(Command):
    def __init__(self, receiver, signals_handler, controller, *canvases):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.controller = controller
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to update plots based on the selected option in the GUI.
        """
        self.receiver.update_plots_from_file(self.controller, self.signals_handler, *self.canvases)


class UpdatePlotsFromJpgFileCommand(Command):
    def __init__(self, receiver, controller, signals_handler, *canvases):
        super().__init__(receiver)
        self.controller = controller
        self.signals_handler = signals_handler
        self.canvases = canvases

    def execute(self):
        self.receiver.update_plots_from_jpg_file(self.controller, self.signals_handler, *self.canvases)


class FilterFFTCommand(Command):
    def __init__(self, receiver, controller, *canvases):
        super().__init__(receiver)
        self.controller = controller
        self.canvases = canvases

    def execute(self):
        self.receiver.filter_fft(self.controller)
        self.receiver.filtered_fft_plot(*self.canvases)


class FilterDCTCommand(Command):
    def __init__(self, receiver, controller, *canvases):
        super().__init__(receiver)
        self.controller = controller
        self.canvases = canvases

    def execute(self):
        self.receiver.filter_dct(self.controller)
        self.receiver.filtered_dct_plot(*self.canvases)


class ResetFFTCommand(Command):
    def __init__(self, receiver, *canvases):
        super().__init__(receiver)
        self.canvases = canvases

    def execute(self):
        self.receiver.update_fft_plot(self.canvases[0])
        self.receiver.update_ifft_plot(self.canvases[1])


class ResetDCTCommand(Command):
    def __init__(self, receiver, *canvases):
        super().__init__(receiver)
        self.canvases = canvases

    def execute(self):
        self.receiver.update_dct_plot(self.canvases[0])
        self.receiver.update_idct_plot(self.canvases[1])


class HandleFiltersListCommand(Command):
    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        self.receiver.handle_list_of_filters(self.controller)


class DeleteSignalCommand(Command):
    """
    Command to delete a signal from the SignalsHandler.

    Attributes:
    - signals_handler: The SignalsHandler instance.
    - gui: The GUI instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, signals_handler, controller):
        super().__init__(receiver)
        self.controller = controller
        self.signals_handler = signals_handler

    def execute(self):
        """
        Execute the command to delete a signal from the SignalsHandler and update the GUI label.
        """
        self.receiver.delete_signal(self.signals_handler, self.controller)
        self.controller.update_label(self.controller.signal_label, self.signals_handler.get_text())


class UpdateSignalCommand(Command):
    """
    Command to update the parameters of a signal in the SignalsHandler.

    Attributes:
    - signals_handler: The SignalsHandler instance.
    - gui: The GUI instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, signals_handler, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.signals_handler = signals_handler
        self.controller = controller

    def execute(self):
        """
        Execute the command to update the parameters of a signal in the SignalsHandler and update the GUI label.
        """
        self.receiver.update_signal(self.signals_handler, self.controller)
        self.controller.update_label(self.controller.signal_label, self.signals_handler.get_text())


class ChooseWavFileCommand(Command):
    """
    Command to open a file dialog and choose a file.

    Attributes:
    - gui: The GUI instance.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Execute the command to open a file dialog and choose a file.
        """
        self.receiver.choose_wav_file(self.controller)


class ChooseJpgFileCommand(Command):
    """
    Command to open a file dialog and choose a file.

    Attributes:
    - gui: The GUI instance.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Execute the command to open a file dialog and choose a file.
        """
        self.receiver.choose_jpg_file(self.controller)


class CreateWindowCommand(Command):
    """
    Command to create and display a new figure window.

    Attributes:
    - name (str): The title of the figure window.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        self.receiver.show_window(self.controller)


class HandleFileCheckBoxCommand(Command):
    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        self.receiver.set_main_window_inactive(self.controller.wav_file_check_box_state, self.controller)
