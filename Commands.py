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
    - receiver: The receiver instance.
    - signals_handler: The SignalsHandler instance.
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
    - receiver: The receiver instance.
    - signals_handler: The SignalsHandler instance.
    - controller: The controller instance.
    - canvases: The canvas instances.
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
    """
    Command to update plots based on the selected option in the GUI using data from a file.

    Attributes:
    - receiver: The receiver instance.
    - signals_handler: The SignalsHandler instance.
    - controller: The controller instance.
    - canvases: The canvas instances.
    """

    def __init__(self, receiver, signals_handler, controller, *canvases):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.controller = controller
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to update plots based on the selected option in the GUI using data from a file.
        """
        self.receiver.update_plots_from_file(self.controller, self.signals_handler, *self.canvases)


class UpdatePlotsFromJpgFileCommand(Command):
    """
    Command to update plots from a JPG file.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    - signals_handler: The SignalsHandler instance.
    - canvases: The canvas instances.
    """

    def __init__(self, receiver, controller, signals_handler, *canvases):
        super().__init__(receiver)
        self.controller = controller
        self.signals_handler = signals_handler
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to update plots from a JPG file.
        """
        self.receiver.update_plots_from_jpg_file(self.controller, self.signals_handler, *self.canvases)


class FilterFFTCommand(Command):
    """
    Command to apply FFT filtering.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    - canvases: The canvas instances.
    """

    def __init__(self, receiver, controller, *canvases):
        super().__init__(receiver)
        self.controller = controller
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to apply FFT filtering.
        """
        self.receiver.filter_fft(self.controller)
        self.receiver.filtered_fft_plot(*self.canvases)


class FilterDCTCommand(Command):
    """
    Command to apply DCT filtering.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    - canvases: The canvas instances.
    """

    def __init__(self, receiver, controller, *canvases):
        super().__init__(receiver)
        self.controller = controller
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to apply DCT filtering.
        """
        self.receiver.filter_dct(self.controller)
        self.receiver.filtered_dct_plot(*self.canvases)


class ResetFFTCommand(Command):
    """
    Command to reset FFT plots.

    Attributes:
    - receiver: The receiver instance.
    - canvases: The canvas instances.
    """

    def __init__(self, receiver, *canvases):
        super().__init__(receiver)
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to reset FFT plots.
        """
        self.receiver.update_fft_plot(self.canvases[0])
        self.receiver.update_ifft_plot(self.canvases[1])


class ResetDCTCommand(Command):
    """
    Command to reset DCT plots.

    Attributes:
    - receiver: The receiver instance.
    - canvases: The canvas instances.
    """

    def __init__(self, receiver, *canvases):
        super().__init__(receiver)
        self.canvases = canvases

    def execute(self):
        """
        Execute the command to reset DCT plots.
        """
        self.receiver.update_dct_plot(self.canvases[0])
        self.receiver.update_idct_plot(self.canvases[1])


class HandleFiltersListCommand(Command):
    """
    Command to handle the list of filters.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Execute the command to handle the list of filters.
        """
        self.receiver.handle_list_of_filters(self.controller)


class DeleteSignalCommand(Command):
    """
    Command to delete a signal from the SignalsHandler.

    Attributes:
    - receiver: The receiver instance.
    - signals_handler: The SignalsHandler instance.
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
    - receiver: The receiver instance.
    - signals_handler: The SignalsHandler instance.
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
    Command to open a file dialog and choose a WAV file.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Execute the command to open a file dialog and choose a WAV file.
        """
        self.receiver.choose_wav_file(self.controller)


class ChooseJpgFileCommand(Command):
    """
    Command to open a file dialog and choose a JPG file.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Execute the command to open a file dialog and choose a JPG file.
        """
        self.receiver.choose_jpg_file(self.controller)


class CreateWindowCommand(Command):
    """
    Command to create and display a new figure window.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Execute the command to create and display a new figure window.
        """
        self.receiver.show_window(self.controller)


class HandleFileCheckBoxCommand(Command):
    """
    Command to handle the file checkbox.

    Attributes:
    - receiver: The receiver instance.
    - controller: The controller instance.
    """

    def __init__(self, receiver, controller):
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Execute the command to handle the file checkbox.
        """
        self.receiver.set_main_window_inactive(self.controller.wav_file_check_box_state, self.controller)
