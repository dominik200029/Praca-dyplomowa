import sys
from PyQt5.QtWidgets import QApplication
from Canvas import Canvas
from Controllers import MainWindowController, DFTWindowController, DCTWindowController
from Invoker import Invoker
from Receiver import Receiver
from Receiver2D import Receiver2D
from SignalsHandler import SineHandler, Sine2DHandler
from Commands import (ChooseWavFileCommand, AddSignalCommand, DeleteSignalCommand, UpdateSignalCommand,
                      CreateWindowCommand, FilterFFTCommand, ResetFFTCommand, HandleFiltersListCommand,
                      FilterDCTCommand, HandleFileCheckBoxCommand, ResetDCTCommand, UpdatePlotsFromFileCommand,
                      UpdatePlotsCommand, ChooseJpgFileCommand, UpdatePlotsFromJpgFileCommand)


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        # Signals handler to store wave information
        self.signals_handler = SineHandler()
        self.signals_2d_handler = Sine2DHandler()

        # Windows
        self.main_window = MainWindowController()
        self.dft_window = DFTWindowController()
        self.dct_window = DCTWindowController()

        # Canvases
        self.signal_canvas = Canvas(self.main_window.signal_layout)
        self.dft_canvas = Canvas(self.dft_window.dft_layout)
        self.dct_canvas = Canvas(self.dct_window.dct_layout)
        self.idft_canvas = Canvas(self.dft_window.idft_layout)
        self.idct_canvas = Canvas(self.dct_window.idct_layout)

        self.signal_2d_canvas = Canvas(self.main_window.signal_layout_2d)

        # Business logic class
        self.receiver = Receiver()
        self.receiver_2d = Receiver2D()

        # Commands
        self.choose_wav_file_command = ChooseWavFileCommand(self.receiver, self.main_window)
        self.choose_jpg_file_command = ChooseJpgFileCommand(self.receiver_2d, self.main_window)
        self.add_signal_command = AddSignalCommand(self.receiver, self.signals_handler, self.main_window)
        self.update_plots_command = UpdatePlotsCommand(self.receiver, self.signals_handler,
                                                       self.main_window, self.signal_canvas,
                                                       self.dft_canvas, self.idft_canvas, self.dct_canvas,
                                                       self.idct_canvas)
        self.delete_signal_command = DeleteSignalCommand(self.receiver, self.signals_handler, self.main_window)
        self.update_signal_command = UpdateSignalCommand(self.receiver, self.signals_handler, self.main_window)
        self.create_dft_window_command = CreateWindowCommand(self.receiver, self.dft_window)
        self.create_dct_window_command = CreateWindowCommand(self.receiver, self.dct_window)
        self.fft_filter_command = FilterFFTCommand(self.receiver, self.dft_window,
                                                   self.dft_canvas, self.idft_canvas)
        self.reset_dct_command = ResetDCTCommand(self.receiver, self.dct_canvas, self.idct_canvas)
        self.reset_fft_command = ResetFFTCommand(self.receiver, self.dft_canvas, self.idft_canvas)
        self.handle_dft_filters_list_command = HandleFiltersListCommand(self.receiver, self.dft_window)
        self.dct_filter_command = FilterDCTCommand(self.receiver, self.dct_window,
                                                   self.dct_canvas, self.idct_canvas)
        self.handle_dct_filters_list_command = HandleFiltersListCommand(self.receiver, self.dct_window)
        self.handle_file_check_box_command = HandleFileCheckBoxCommand(self.receiver, self.main_window)
        self.update_plots_from_file_command = UpdatePlotsFromFileCommand(self.receiver, self.signals_handler,
                                                                         self.main_window, self.signal_canvas,
                                                                         self.dft_canvas, self.idft_canvas,
                                                                         self.dct_canvas, self.idct_canvas)
        self.update_plots_from_jpg_file_command = UpdatePlotsFromJpgFileCommand(self.receiver_2d, self.main_window,
                                                                                self.signals_2d_handler,
                                                                                self.signal_2d_canvas)

        # Invokers
        self.choose_file_button_invoker = Invoker()
        self.choose_jpg_file_button_invoker = Invoker()
        self.add_button_invoker = Invoker()
        self.add_function_invoker = Invoker()
        self.update_plots_invoker = Invoker()
        self.update_plots_from_file_invoker = Invoker()
        self.delete_signal_invoker = Invoker()
        self.update_signal_invoker = Invoker()
        self.create_dft_window_invoker = Invoker()
        self.create_dct_window_invoker = Invoker()
        self.fft_filter_invoker = Invoker()
        self.dct_filter_invoker = Invoker()
        self.reset_fft_invoker = Invoker()
        self.reset_dct_invoker = Invoker()
        self.handle_dft_filters_list_invoker = Invoker()
        self.handle_dct_filters_list_invoker = Invoker()
        self.handle_file_check_box_invoker = Invoker()
        self.update_plots_jpg_invoker = Invoker()

        # Connect buttons to commands
        self.set_button_command(self.main_window.choose_file_button, self.choose_file_button_invoker,
                                self.choose_wav_file_command)
        self.set_button_command(self.main_window.choose_image_file_button, self.choose_jpg_file_button_invoker,
                                self.choose_jpg_file_command)
        self.set_button_command(self.main_window.add_button, self.add_button_invoker, self.add_signal_command)
        self.set_button_command(self.main_window.add_button, self.add_function_invoker, self.update_plots_command)
        self.set_button_command(self.main_window.delete_signal_button, self.delete_signal_invoker,
                                self.delete_signal_command)
        self.set_button_command(self.main_window.dft_button, self.create_dft_window_invoker,
                                self.create_dft_window_command)
        self.set_button_command(self.main_window.dct_button, self.create_dct_window_invoker,
                                self.create_dct_window_command)
        self.set_button_command(self.dft_window.reset_button, self.reset_fft_invoker, self.reset_fft_command)
        self.set_button_command(self.dct_window.reset_button, self.reset_dct_invoker, self.reset_dct_command)
        self.set_button_command(self.main_window.delete_signal_button, self.update_plots_invoker,
                                self.update_plots_command)

        # Connect edit lanes to commands
        self.set_edit_lane_command(self.main_window.sampling_frequency_edit, self.update_plots_invoker,
                                   self.update_plots_command)
        self.set_edit_lane_command(self.main_window.samples_number_edit, self.update_plots_invoker,
                                   self.update_plots_command)
        self.set_edit_lane_command(self.main_window.amplitude_edit, self.update_signal_invoker,
                                   self.update_signal_command)
        self.set_edit_lane_command(self.main_window.amplitude_edit, self.update_plots_invoker,
                                   self.update_plots_command)
        self.set_edit_lane_command(self.main_window.frequency_edit, self.update_signal_invoker,
                                   self.update_signal_command)
        self.set_edit_lane_command(self.main_window.frequency_edit, self.update_plots_invoker,
                                   self.update_plots_command)
        self.set_edit_lane_command(self.main_window.phase_edit, self.update_plots_invoker, self.update_plots_command)
        self.set_edit_lane_command(self.main_window.phase_edit, self.update_signal_invoker, self.update_signal_command)
        self.set_edit_lane_command(self.dft_window.cut_off_edit, self.fft_filter_invoker, self.fft_filter_command)
        self.set_edit_lane_command(self.dft_window.high_cut_off, self.fft_filter_invoker, self.fft_filter_command)
        self.set_edit_lane_command(self.dft_window.low_cut_off, self.fft_filter_invoker, self.fft_filter_command)

        self.set_edit_lane_command(self.dct_window.cut_off_edit, self.dct_filter_invoker, self.dct_filter_command)
        self.set_edit_lane_command(self.dct_window.high_cut_off, self.dct_filter_invoker, self.dct_filter_command)
        self.set_edit_lane_command(self.dct_window.low_cut_off, self.dct_filter_invoker, self.dct_filter_command)

        # Connect ComboBox to commands
        self.set_combo_box_command(self.dft_window.filters_list, self.handle_dft_filters_list_invoker,
                                   self.handle_dft_filters_list_command)
        self.set_combo_box_command(self.dct_window.filters_list, self.handle_dct_filters_list_invoker,
                                   self.handle_dct_filters_list_command)

        # Connect CheckBox to commands
        self.set_check_box_command(self.main_window.file_check_box, self.handle_file_check_box_invoker,
                                   self.handle_file_check_box_command)
        self.set_check_box_command(self.main_window.file_check_box, self.update_plots_from_file_invoker,
                                   self.update_plots_from_file_command)
        self.set_check_box_command(self.main_window.image_file_checkBox, self.update_plots_jpg_invoker,
                                   self.update_plots_from_jpg_file_command)

    @staticmethod
    def set_button_command(button, invoker: Invoker, command):
        invoker.store_command(command)
        button.clicked.connect(invoker.execute)

    @staticmethod
    def set_edit_lane_command(edit_lane, invoker: Invoker, command):
        invoker.store_command(command)
        edit_lane.valueChanged.connect(invoker.execute)

    @staticmethod
    def set_combo_box_command(combo_box, invoker: Invoker, command):
        invoker.store_command(command)
        combo_box.currentIndexChanged.connect(invoker.execute)

    @staticmethod
    def set_check_box_command(check_box, invoker: Invoker, command):
        invoker.store_command(command)
        check_box.stateChanged.connect(invoker.execute)


if __name__ == '__main__':
    app = App(sys.argv)
    app.main_window.show()
    sys.exit(app.exec_())
