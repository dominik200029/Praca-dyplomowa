from abc import ABC, abstractmethod


class Command(ABC):
    """
    Abstract base class for commands.

    Attributes:
        receiver: The receiver object that performs the actual action.
    """

    def __init__(self, receiver):
        """
        Initializes a Command instance with a receiver object.

        Parameters:
            receiver: The receiver object that performs the actual action.
        """
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        """
        Abstract method to execute the command.
        """
        pass


class CreateWindowCommand(Command):
    """
    Command to create a window.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a CreateWindowCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to create a window.
        """
        self.receiver.show_window(self.controller)


class AddSignalCommand(Command):
    """
    Command to add a signal.
    """

    def __init__(self, receiver, signals_handler, controller):
        """
        Initializes an AddSignalCommand instance with specified receiver, signals_handler, and controller.

        Parameters:
            receiver: The receiver object.
            signals_handler: The signals_handler object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.controller = controller

    def execute(self):
        """
        Executes the command to add a signal.
        """
        self.receiver.add_signal_to_list(self.signals_handler, self.controller)
        self.controller.update_label(self.controller.signal_label, self.signals_handler.get_text())


class DeleteSignalCommand(Command):
    """
    Command to delete a signal.
    """

    def __init__(self, receiver, signals_handler, controller):
        """
        Initializes a DeleteSignalCommand instance with specified receiver, signals_handler, and controller.

        Parameters:
            receiver: The receiver object.
            signals_handler: The signals_handler object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller
        self.signals_handler = signals_handler

    def execute(self):
        """
        Executes the command to delete a signal.
        """
        self.receiver.delete_signal(self.signals_handler, self.controller)
        self.controller.update_label(self.controller.signal_label, self.signals_handler.get_text())


class UpdateSignalCommand(Command):
    """
    Command to update a signal.
    """

    def __init__(self, receiver, signals_handler, controller):
        """
        Initializes an UpdateSignalCommand instance with specified receiver, signals_handler, and controller.

        Parameters:
            receiver: The receiver object.
            signals_handler: The signals_handler object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.receiver = receiver
        self.signals_handler = signals_handler
        self.controller = controller

    def execute(self):
        """
        Executes the command to update a signal.
        """
        self.receiver.update_signal(self.signals_handler, self.controller)
        self.controller.update_label(self.controller.signal_label, self.signals_handler.get_text())


class UpdateSignalPlotCommand(Command):
    """
    Command to update the signal plot.
    """

    def __init__(self, receiver, signals_handler, controller):
        """
        Initializes an UpdateSignalPlotCommand instance with specified receiver, signals_handler, and controller.

        Parameters:
            receiver: The receiver object.
            signals_handler: The signals_handler object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.controller = controller

    def execute(self):
        """
        Executes the command to update the signal plot.
        """
        if self.receiver.is_signal_from_file and self.receiver.wav_filepath is not None:
            self.receiver.collect_data_from_file(self.signals_handler)
        else:
            self.receiver.collect_data(self.controller)
            self.receiver.calculate_time_axis()
            self.receiver.calculate_discrete_time_axis()
            self.receiver.calculate_dft_axis()
            self.receiver.calculate_dct_axis()
            self.receiver.calculate_wave(self.signals_handler)

        self.receiver.update_signal_plot(self.controller.signal_canvas)


class UpdateDFTPlotCommand(Command):
    """
    Command to update the DFT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes an UpdateDFTPlotCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to update the DFT plot.
        """
        self.receiver.perform_dft()
        self.receiver.perform_idft()
        self.receiver.update_dft_plot(self.controller.dft_canvas)
        self.receiver.update_idft_plot(self.controller.idft_canvas)


class UpdateDCTPlotCommand(Command):
    """
    Command to update the DCT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes an UpdateDCTPlotCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to update the DCT plot.
        """
        self.receiver.perform_dct()
        self.receiver.perform_idct()
        self.receiver.update_dct_plot(self.controller.dct_canvas)
        self.receiver.update_idct_plot(self.controller.idct_canvas)


class FilterDFTCommand(Command):
    """
    Command to filter the DFT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a FilterDFTCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to filter the DFT plot.
        """
        self.receiver.filter_dft(self.controller)
        self.receiver.filter_idft()
        if self.controller.get_filters_list_index() != 0:
            self.receiver.filtered_dft_plot(self.controller.dft_canvas)
            self.receiver.filtered_idft_plot(self.controller.idft_canvas)


class FilterDCTCommand(Command):
    """
    Command to filter the DCT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a FilterDCTCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to filter the DCT plot.
        """
        self.receiver.filter_dct(self.controller)
        self.receiver.filter_idct()
        if self.controller.get_filters_list_index() != 0:
            self.receiver.filtered_dct_plot(self.controller.dct_canvas)
            self.receiver.filtered_idct_plot(self.controller.idct_canvas)


class ResetDFTCommand(Command):
    """
    Command to reset the DFT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a ResetDFTCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to reset the DFT plot.
        """
        self.receiver.update_dft_plot(self.controller.dft_canvas)
        self.receiver.update_idft_plot(self.controller.idft_canvas)


class ResetDCTCommand(Command):
    """
    Command to reset the DCT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a ResetDCTCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to reset the DCT plot.
        """
        self.receiver.update_dct_plot(self.controller.dct_canvas)
        self.receiver.update_idct_plot(self.controller.idct_canvas)


class HandleFiltersListCommand(Command):
    """
    Command to handle the list of filters.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a HandleFiltersListCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to handle the list of filters.
        """
        self.receiver.handle_list_of_filters(self.controller)


class ChooseWavFileCommand(Command):
    """
    Command to choose a WAV file.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a ChooseWavFileCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to choose a WAV file.
        """
        self.receiver.choose_wav_file(self.controller)


class ChooseJpgFileCommand(Command):
    """
    Command to choose a JPG file.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a ChooseJpgFileCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to choose a JPG file.
        """
        self.receiver.choose_jpg_file(self.controller)


class HandleFileCheckBoxCommand(Command):
    """
    Command to handle the file check box.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a HandleFileCheckBoxCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to handle the file check box.
        """
        self.receiver.dft_data = None
        self.receiver.set_main_window_inactive(self.controller.wav_file_check_box_state(), self.controller)


# 2D Commands
class UpdateImagePlotCommand(Command):
    """
    Command to update the image plot.
    """

    def __init__(self, receiver, controller, signals_handler):
        """
        Initializes an UpdateImagePlotCommand instance with specified receiver, controller, and signals_handler.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
            signals_handler: The signals_handler object.
        """
        super().__init__(receiver)
        self.controller = controller
        self.signals_handler = signals_handler

    def execute(self):
        """
        Executes the command to update the image plot.
        """
        self.receiver.set_image(self.controller, self.signals_handler)
        self.receiver.plot_image(self.controller.image_canvas)


class UpdateSineImagePlotCommand(Command):
    """
    Command to update the sine image plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes an UpdateSineImagePlotCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to update the sine image plot.
        """
        self.receiver.calculate_image(self.controller)
        self.receiver.plot_image(self.controller.image_canvas)


class UpdateDFT2DPlotsCommand(Command):
    """
    Command to update the 2D DFT plots.
    """

    def __init__(self, receiver, controller):
        """
        Initializes an UpdateDFT2DPlotsCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to update the 2D DFT plots.
        """
        self.receiver.perform_2d_dft()
        self.receiver.plot_2d_dft(self.controller.dft2D_canvas, self.controller)
        self.receiver.perform_2d_idft()
        self.receiver.plot_2d_idft(self.controller.idft2D_canvas)


class FilterFFT2DCommand(Command):
    """
    Command to filter the 2D FFT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a FilterFFT2DCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to filter the 2D FFT plot.
        """
        self.receiver.filter_2d_dft(self.controller)
        self.receiver.filter_2d_idft()
        if self.controller.get_filters_list_index() != 0:
            self.receiver.plot_filtered_2d_dft(self.controller.dft2D_canvas, self.controller)
            self.receiver.plot_filtered_2d_idft(self.controller.idft2D_canvas)


class UpdateDCT2DPlotsCommand(Command):
    """
    Command to update the 2D DCT plots.
    """

    def __init__(self, receiver, controller):
        """
        Initializes an UpdateDCT2DPlotsCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to update the 2D DCT plots.
        """
        self.receiver.perform_2d_dct()
        self.receiver.plot_2d_dct(self.controller.dct2D_canvas, self.controller)
        self.receiver.perform_2d_idct()
        self.receiver.plot_2d_idct(self.controller.idct2D_canvas)


class ResetDFT2DCommand(Command):
    """
    Command to reset the 2D DFT plots.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a ResetDFT2DCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to reset the 2D DFT plots.
        """
        self.receiver.plot_2d_dft(self.controller.dft2D_canvas, self.controller)
        self.receiver.plot_2d_idft(self.controller.idft2D_canvas)


class FilterDCT2DCommand(Command):
    """
    Command to filter the 2D DCT plot.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a FilterDCT2DCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to filter the 2D DCT plot.
        """
        self.receiver.filter_2d_dct(self.controller)
        self.receiver.filter_2d_idct()
        if self.controller.get_filters_list_index() != 0:
            self.receiver.plot_filtered_2d_dct(self.controller.dct2D_canvas, self.controller)
            self.receiver.plot_filtered_2d_idct(self.controller.idct2D_canvas)


class ResetDCT2DCommand(Command):
    """
    Command to reset the 2D DCT plots.
    """

    def __init__(self, receiver, controller):
        """
        Initializes a ResetDCT2DCommand instance with specified receiver and controller.

        Parameters:
            receiver: The receiver object.
            controller: The controller object.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command to reset the 2D DCT plots.
        """
        self.receiver.plot_2d_dct(self.controller.dct2D_canvas, self.controller)
        self.receiver.plot_2d_idct(self.controller.idct2D_canvas)


class ChangeDFT2DScaleCommand(Command):
    """
    A command class for changing the scale of a 2D Discrete Fourier Transform (DFT) plot.

    This command allows switching between different scale representations
    of a 2D DFT plot based on the current state of the receiver.

    Attributes:
            receiver : The receiver object responsible for business logic.
            controller (Controller): The controller object managing the GUI.

    Methods:
        execute(): Executes the command, plotting the appropriate 2D DFT based on the receiver's state.
    """

    def __init__(self, receiver, controller):
        """
        Initializes the ChangeDFT2DScaleCommand.

        Args:
            receiver : The receiver object responsible for business logic.
            controller (Controller): The controller object managing the GUI.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command.

        Depending on the state of the receiver, plots either the filtered 2D DFT
        or the regular 2D DFT using the provided controller's canvas.
        """
        if self.receiver.filtered_plot_dft:
            self.receiver.plot_filtered_2d_dft(self.controller.dft2D_canvas, self.controller)
        else:
            self.receiver.plot_2d_dft(self.controller.dft2D_canvas, self.controller)


class ChangeDCT2DScaleCommand(Command):
    """
    A command class for changing the scale of a 2D Discrete Cosine Transform (DCT) plot.

    This command allows switching between different scale representations
    of a 2D DCT plot based on the current state of the receiver.

    Attributes:
            receiver : The receiver object responsible for business logic.
            controller (Controller): The controller object managing the GUI.

    Methods:
        execute(): Executes the command, plotting the appropriate 2D DCT based on the receiver's state.
    """

    def __init__(self, receiver, controller):
        """
        Initializes the ChangeDCT2DScaleCommand.

        Args:
            receiver : The receiver object responsible for business logic.
            controller (Controller): The controller object managing the GUI.
        """
        super().__init__(receiver)
        self.controller = controller

    def execute(self):
        """
        Executes the command.

        Depending on the state of the receiver, plots either the filtered 2D DCT
        or the regular 2D DCT using the provided controller's canvas.
        """
        if self.receiver.filtered_plot_dct:
            self.receiver.plot_filtered_2d_dct(self.controller.dct2D_canvas, self.controller)
        else:
            self.receiver.plot_2d_dct(self.controller.dct2D_canvas, self.controller)
