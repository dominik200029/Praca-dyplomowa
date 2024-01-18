import sys
from PyQt5.QtWidgets import QApplication
from Canvas import Canvas
from Commands import (ChooseFileCommand, AddSignalCommand, DeleteSignalCommand, UpdateSignalCommand, UpdatePlotsCommand,
                      CreateWindowCommand)
from Controller import Controller
from Gui import Gui
from Invoker import Invoker
from Receiver import Receiver
from SignalsHandler import SignalsHandler


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.gui = Gui()
        self.signals_handler = SignalsHandler()
        self.controller = Controller(self.gui)
        self.receiver = Receiver()
        self.canvas = Canvas(self.gui.layout1)

        # Commands
        self.choose_file_command = ChooseFileCommand(self.receiver, self.gui)
        self.add_signal_command = AddSignalCommand(self.receiver, self.signals_handler, self.gui, self.controller)
        self.update_plots_command = UpdatePlotsCommand(self.receiver, self.signals_handler,
                                                       self.gui, self.controller, self.canvas)
        self.delete_signal_command = DeleteSignalCommand(self.receiver, self.signals_handler, self.gui, self.controller)
        self.update_signal_command = UpdateSignalCommand(self.receiver, self.signals_handler, self.gui, self.controller)
        self.create_dft_window_command = CreateWindowCommand(self.receiver, 'DFT')
        self.create_dct_window_command = CreateWindowCommand(self.receiver, 'DCT')
        self.create_idft_window_command = CreateWindowCommand(self.receiver, 'IDFT')
        self.create_idct_window_command = CreateWindowCommand(self.receiver, 'IDCT')

        # Invokers
        self.choose_file_button_invoker = Invoker()
        self.add_button_invoker = Invoker()
        self.update_plots_invoker = Invoker()
        self.delete_signal_invoker = Invoker()
        self.update_signal_invoker = Invoker()
        self.create_dft_window_invoker = Invoker()
        self.create_dct_window_invoker = Invoker()
        self.create_idft_window_invoker = Invoker()
        self.create_idct_window_invoker = Invoker()

        # Connect buttons to commands
        self.set_button_command(self.gui.choose_file_button, self.choose_file_button_invoker, self.choose_file_command)
        self.set_button_command(self.gui.add_button, self.add_button_invoker, self.add_signal_command)
        self.set_button_command(self.gui.delete_signal_button, self.delete_signal_invoker,
                                self.delete_signal_command)
        self.set_button_command(self.gui.dft_button, self.create_dft_window_invoker, self.create_dft_window_command)
        self.set_button_command(self.gui.dct_button, self.create_dct_window_invoker, self.create_dct_window_command)
        self.set_button_command(self.gui.idft_button, self.create_idft_window_invoker, self.create_idft_window_command)
        self.set_button_command(self.gui.idct_button, self.create_idct_window_invoker, self.create_idct_window_command)
        self.set_button_command(self.gui.print_button, self.update_plots_invoker, self.update_plots_command)

        # Connect edit lanes to commands
        self.set_edit_lane_command(self.gui.sampling_frequency_edit, self.update_plots_invoker,
                                   self.update_plots_command)
        self.set_edit_lane_command(self.gui.samples_number_edit, self.update_plots_invoker, self.update_plots_command)
        self.set_edit_lane_command(self.gui.amplitude_edit, self.update_signal_invoker, self.update_signal_command)
        self.set_edit_lane_command(self.gui.amplitude_edit, self.update_plots_invoker, self.update_plots_command)
        self.set_edit_lane_command(self.gui.frequency_edit, self.update_signal_invoker, self.update_signal_command)
        self.set_edit_lane_command(self.gui.frequency_edit, self.update_plots_invoker, self.update_plots_command)
        self.set_edit_lane_command(self.gui.phase_edit, self.update_plots_invoker, self.update_plots_command)
        self.set_edit_lane_command(self.gui.phase_edit, self.update_signal_invoker, self.update_signal_command)

    @staticmethod
    def set_button_command(button, invoker: Invoker, command):
        invoker.store_command(command)
        button.clicked.connect(invoker.execute)

    @staticmethod
    def set_edit_lane_command(edit_lane, invoker: Invoker, command):
        invoker.store_command(command)
        edit_lane.valueChanged.connect(invoker.execute)


if __name__ == '__main__':
    app = App(sys.argv)
    app.gui.show()
    sys.exit(app.exec_())
