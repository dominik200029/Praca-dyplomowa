import sys
from PyQt5.QtWidgets import QApplication
from Controllers import MainWindowController, DFTWindowController, DCTWindowController, DFT2DWindowController, \
    DCT2DWindowController
from Invoker import Invoker
from Receiver import Receiver
from Receiver2D import Receiver2D
from SignalsHandler import SineHandler, Sine2DHandler
from Commands import (ChooseWavFileCommand, AddSignalCommand, DeleteSignalCommand, UpdateSignalCommand,
                      CreateWindowCommand, FilterDFTCommand, ResetDFTCommand, HandleFiltersListCommand,
                      FilterDCTCommand, HandleFileCheckBoxCommand, ResetDCTCommand,
                      UpdateSignalPlotCommand, UpdateDFTPlotCommand, UpdateDCTPlotCommand, ChooseJpgFileCommand,
                      UpdateImagePlotCommand, UpdateDFT2DPlotsCommand, FilterFFT2DCommand, UpdateDCT2DPlotsCommand,
                      ResetDFT2DCommand, FilterDCT2DCommand, ResetDCT2DCommand, UpdateSineImagePlotCommand)


class App(QApplication):
    """
        Main application class responsible for managing windows and commands.

        Attributes:
            signals_handler: Instance of the signal handler for 1D signals.
            signals_2d_handler: Instance of the signal handler for 2D signals.
            main_window: Instance of the main window controller.
            dft_window: Instance of the DFT window controller.
            dct_window: Instance of the DCT window controller.
            dft_2d_window: Instance of the 2D DFT window controller.
            dct_2d_window: Instance of the 2D DCT window controller.
            receiver: Instance of the receiver for 1D signals.
            receiver_2d: Instance of the receiver for 2D signals.

        Methods:
            connect_invoker_to_button: Connects a button's clicked signal to an invoker's execute method.
            execute_if_checked: Executes an invoker if a checkbox is checked.
            connect_invoker_to_spin_box: Connects a spin box's value changed signal to an invoker's execute method.
            connect_invoker_to_spin_box_if_checked: Connects a spin box's value changed signal to an invoker's execute
             method if a checkbox is checked.
            connect_invoker_to_combo_box: Connects a combo box's current index changed signal to an invoker's execute
             method.
            connect_invoker_to_check_box: Connects a checkboxes state changed signal to an invoker's execute method.
        """
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        # Signals handler to store wave information
        self.signals_handler = SineHandler()
        self.signals_2d_handler = Sine2DHandler()

        # Windows
        self.main_window = MainWindowController()
        self.dft_window = DFTWindowController()
        self.dct_window = DCTWindowController()
        self.dft_2d_window = DFT2DWindowController()
        self.dct_2d_window = DCT2DWindowController()

        # Business logic class
        self.receiver = Receiver()
        self.receiver_2d = Receiver2D()

        # Commands
        self.add_signal_command = AddSignalCommand(self.receiver, self.signals_handler, self.main_window)
        self.delete_signal_command = DeleteSignalCommand(self.receiver, self.signals_handler, self.main_window)
        self.update_signal_command = UpdateSignalCommand(self.receiver, self.signals_handler, self.main_window)

        self.create_dft_window_command = CreateWindowCommand(self.receiver, self.dft_window)
        self.create_dct_window_command = CreateWindowCommand(self.receiver, self.dct_window)
        self.create_2d_dft_window_command = CreateWindowCommand(self.receiver_2d, self.dft_2d_window)
        self.create_2d_dct_window_command = CreateWindowCommand(self.receiver_2d, self.dct_2d_window)

        self.choose_wav_file_command = ChooseWavFileCommand(self.receiver, self.main_window)
        self.choose_jpg_file_command = ChooseJpgFileCommand(self.receiver_2d, self.main_window)

        self.update_signal_plot_command = UpdateSignalPlotCommand(self.receiver, self.signals_handler, self.main_window)
        self.update_dft_plot_command = UpdateDFTPlotCommand(self.receiver, self.dft_window)
        self.update_dct_plot_command = UpdateDCTPlotCommand(self.receiver, self.dct_window)
        self.update_image_command = UpdateImagePlotCommand(self.receiver_2d, self.main_window, self.signals_2d_handler)
        self.update_2d_dft_command = UpdateDFT2DPlotsCommand(self.receiver_2d, self.dft_2d_window)
        self.update_2d_dct_command = UpdateDCT2DPlotsCommand(self.receiver_2d, self.dct_2d_window)
        self.update_sine_image_command = UpdateSineImagePlotCommand(self.receiver_2d, self.main_window)

        self.handle_dft_filters_list_command = HandleFiltersListCommand(self.receiver, self.dft_window)
        self.handle_dct_filters_list_command = HandleFiltersListCommand(self.receiver, self.dct_window)

        self.handle_file_check_box_command = HandleFileCheckBoxCommand(self.receiver, self.main_window)

        self.dft_filter_command = FilterDFTCommand(self.receiver, self.dft_window)
        self.dct_filter_command = FilterDCTCommand(self.receiver, self.dct_window)
        self.dft_2d_filter_command = FilterFFT2DCommand(self.receiver_2d, self.dft_2d_window)
        self.dct_2d_filter_command = FilterDCT2DCommand(self.receiver_2d, self.dct_2d_window)

        self.reset_dct_command = ResetDCTCommand(self.receiver, self.dct_window)
        self.reset_dft_command = ResetDFTCommand(self.receiver, self.dft_window)
        self.reset_2d_dft_command = ResetDFT2DCommand(self.receiver_2d, self.dft_2d_window)
        self.reset_2d_dct_command = ResetDCT2DCommand(self.receiver_2d, self.dct_2d_window)

        # Invokers
        self.choose_file_button_invoker = Invoker()
        self.choose_file_button_invoker.store_commands(self.choose_wav_file_command)
        self.connect_invoker_to_button(self.main_window.choose_file_button, self.choose_file_button_invoker)

        self.choose_jpg_file_button_invoker = Invoker()
        self.choose_jpg_file_button_invoker.store_commands(self.choose_jpg_file_command)
        self.connect_invoker_to_button(self.main_window.choose_image_file_button, self.choose_jpg_file_button_invoker)

        self.add_button_invoker = Invoker()
        self.add_button_invoker.store_commands(self.add_signal_command, self.update_signal_command,
                                               self.update_signal_plot_command,
                                               self.update_dft_plot_command, self.update_dct_plot_command)
        self.connect_invoker_to_button(self.main_window.add_button, self.add_button_invoker)

        self.delete_button_invoker = Invoker()
        self.delete_button_invoker.store_commands(self.delete_signal_command,
                                                  self.update_signal_plot_command, self.update_dft_plot_command,
                                                  self.update_dct_plot_command)
        self.connect_invoker_to_button(self.main_window.delete_signal_button, self.delete_button_invoker)

        self.dft_button_invoker = Invoker()
        self.dft_button_invoker.store_commands(self.create_dft_window_command)
        self.connect_invoker_to_button(self.main_window.dft_button, self.dft_button_invoker)

        self.dct_button_invoker = Invoker()
        self.dct_button_invoker.store_commands(self.create_dct_window_command)
        self.connect_invoker_to_button(self.main_window.dct_button, self.dct_button_invoker)

        self.amplitude_spin_box_invoker = Invoker()
        self.amplitude_spin_box_invoker.store_commands(self.update_signal_command, self.update_signal_plot_command,
                                                       self.update_dft_plot_command, self.update_dct_plot_command)
        self.connect_invoker_to_spin_box_if_checked(self.main_window.amplitude_spinBox, self.amplitude_spin_box_invoker,
                                                    self.main_window.signal_number_checkBox)

        self.frequency_spin_box_invoker = Invoker()
        self.frequency_spin_box_invoker.store_commands(self.update_signal_command, self.update_signal_plot_command,
                                                       self.update_dft_plot_command, self.update_dct_plot_command)
        self.connect_invoker_to_spin_box_if_checked(self.main_window.frequency_spinBox, self.frequency_spin_box_invoker,
                                                    self.main_window.signal_number_checkBox)

        self.phase_spin_box_invoker = Invoker()
        self.phase_spin_box_invoker.store_commands(self.update_signal_command, self.update_signal_plot_command,
                                                   self.update_dft_plot_command, self.update_dct_plot_command)
        self.connect_invoker_to_spin_box_if_checked(self.main_window.phase_spinBox, self.amplitude_spin_box_invoker,
                                                    self.main_window.signal_number_checkBox)

        self.sampling_frequency_spin_box_invoker = Invoker()
        self.sampling_frequency_spin_box_invoker.store_commands(self.update_signal_plot_command,
                                                                self.update_dft_plot_command,
                                                                self.update_dct_plot_command)
        self.connect_invoker_to_spin_box(self.main_window.sampling_frequency_spinBox,
                                         self.sampling_frequency_spin_box_invoker)

        self.samples_number_spin_box_invoker = Invoker()
        self.samples_number_spin_box_invoker.store_commands(self.update_signal_plot_command,
                                                            self.update_dft_plot_command,
                                                            self.update_dct_plot_command)
        self.connect_invoker_to_spin_box(self.main_window.samples_number_spinBox, self.samples_number_spin_box_invoker)

        self.file_check_box_invoker = Invoker()
        self.file_check_box_invoker.store_commands(self.handle_file_check_box_command, self.update_signal_plot_command,
                                                   self.update_dft_plot_command, self.update_dct_plot_command)
        self.connect_invoker_to_check_box(self.main_window.file_checkBox, self.file_check_box_invoker)

        self.dft_filters_list_invoker = Invoker()
        self.dft_filters_list_invoker.store_commands(self.handle_dft_filters_list_command)
        self.connect_invoker_to_combo_box(self.dft_window.filters_list, self.dft_filters_list_invoker)

        self.dft_apply_button_invoker = Invoker()
        self.dft_apply_button_invoker.store_commands(self.dft_filter_command)
        self.connect_invoker_to_button(self.dft_window.apply_button, self.dft_apply_button_invoker)

        self.dft_reset_button_invoker = Invoker()
        self.dft_reset_button_invoker.store_commands(self.reset_dft_command)
        self.connect_invoker_to_button(self.dft_window.reset_button, self.dft_reset_button_invoker)

        self.dct_filters_list_invoker = Invoker()
        self.dct_filters_list_invoker.store_commands(self.handle_dct_filters_list_command)
        self.connect_invoker_to_combo_box(self.dct_window.filters_list, self.dct_filters_list_invoker)

        self.dct_apply_button_invoker = Invoker()
        self.dct_apply_button_invoker.store_commands(self.dct_filter_command)
        self.connect_invoker_to_button(self.dct_window.apply_button, self.dct_apply_button_invoker)

        self.dct_reset_button_invoker = Invoker()
        self.dct_reset_button_invoker.store_commands(self.reset_dct_command)
        self.connect_invoker_to_button(self.dct_window.reset_button, self.dct_reset_button_invoker)

        self.dft_2d_button_invoker = Invoker()
        self.dft_2d_button_invoker.store_commands(self.create_2d_dft_window_command)
        self.connect_invoker_to_button(self.main_window.dft_2d_button, self.dft_2d_button_invoker)

        self.image_from_file_check_box_invoker = Invoker()
        self.image_from_file_check_box_invoker.store_commands(self.update_image_command, self.update_2d_dft_command,
                                                              self.update_2d_dct_command)
        self.connect_invoker_to_check_box(self.main_window.image_file_checkBox, self.image_from_file_check_box_invoker)

        self.dft_2d_apply_button_invoker = Invoker()
        self.dft_2d_apply_button_invoker.store_commands(self.dft_2d_filter_command)
        self.connect_invoker_to_button(self.dft_2d_window.apply_button, self.dft_2d_apply_button_invoker)

        self.dct_2d_button_invoker = Invoker()
        self.dct_2d_button_invoker.store_commands(self.create_2d_dct_window_command)
        self.connect_invoker_to_button(self.main_window.dct_2d_button, self.dct_2d_button_invoker)

        self.dft_2d_reset_button_invoker = Invoker()
        self.dft_2d_reset_button_invoker.store_commands(self.reset_2d_dft_command)
        self.connect_invoker_to_button(self.dft_2d_window.reset_button, self.dft_2d_reset_button_invoker)

        self.dct_2d_apply_button_invoker = Invoker()
        self.dct_2d_apply_button_invoker.store_commands(self.dct_2d_filter_command)
        self.connect_invoker_to_button(self.dct_2d_window.apply_button, self.dct_2d_apply_button_invoker)

        self.dct_2d_reset_button_invoker = Invoker()
        self.dct_2d_reset_button_invoker.store_commands(self.reset_2d_dct_command)
        self.connect_invoker_to_button(self.dct_2d_window.reset_button, self.dct_2d_reset_button_invoker)

        self.draw_button_invoker = Invoker()
        self.draw_button_invoker.store_commands(self.update_sine_image_command, self.update_2d_dft_command,
                                                self.update_2d_dct_command)
        self.connect_invoker_to_button(self.main_window.draw_button, self.draw_button_invoker)

    @staticmethod
    def connect_invoker_to_button(button, invoker: Invoker):
        """
        Connects a button's clicked signal to an invoker's execute method.

        Parameters:
            button: The button object to connect.
            invoker: The invoker object whose execute method will be connected to the button.

        Returns:
            None
        """
        button.clicked.connect(invoker.execute)

    @staticmethod
    def execute_if_checked(check_box, invoker: Invoker):
        """
        Executes an invoker if a checkbox is checked.

        Parameters:
            check_box: The checkbox object to check.
            invoker: The invoker object to execute if the checkbox is checked.

        Returns:
            None
        """
        if check_box.isChecked():
            invoker.execute()

    @staticmethod
    def connect_invoker_to_spin_box(spin_box, invoker: Invoker):
        """
        Connects a spin box's value changed signal to an invoker's execute method.

        Parameters:
            spin_box: The spin box object to connect.
            invoker: The invoker object whose execute method will be connected to the spin box.

        Returns:
            None
        """
        spin_box.valueChanged.connect(invoker.execute)

    @staticmethod
    def connect_invoker_to_spin_box_if_checked(spin_box, invoker: Invoker, check_box):
        """
        Connects a spin box's value changed signal to an invoker's execute method if a checkbox is checked.

        Parameters:
            spin_box: The spin box object to connect.
            invoker: The invoker object whose execute method will be connected to the spin box.
            check_box: The checkbox object to check before executing the invoker.

        Returns:
            None
        """
        spin_box.valueChanged.connect(lambda: App.execute_if_checked(check_box, invoker))

    @staticmethod
    def connect_invoker_to_combo_box(combo_box, invoker: Invoker):
        """
        Connects a combo box's current index changed signal to an invoker's execute method.

        Parameters:
            combo_box: The combo box object to connect.
            invoker: The invoker object whose execute method will be connected to the combo box.

        Returns:
            None
        """
        combo_box.currentIndexChanged.connect(invoker.execute)

    @staticmethod
    def connect_invoker_to_check_box(check_box, invoker: Invoker):
        """
        Connects a checkboxes state changed signal to an invoker's execute method.

        Parameters:
            check_box: The checkbox object to connect.
            invoker: The invoker object whose execute method will be connected to the checkbox.

        Returns:
            None
        """
        check_box.stateChanged.connect(invoker.execute)


if __name__ == '__main__':
    app = App(sys.argv)
    app.main_window.show()
    sys.exit(app.exec_())
