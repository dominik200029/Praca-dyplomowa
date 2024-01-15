import sys
from PyQt5.QtWidgets import QApplication
from Commands import AddSignalCommand, UpdatePlotsCommand, DeleteSignalCommand, UpdateSignalCommand, ChooseFileCommand
from Invoker import Invoker
from Receiver import Receiver
from Gui import Gui
from Controller import Controller
from SignalsHandler import SignalsHandler


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)

        self.gui = Gui()
        self.signals_handler = SignalsHandler()
        self.controller = Controller(self.gui, self.signals_handler)
        self.receiver = Receiver()

        # Invoker for ChooseFileCommand
        self.choose_file_command = ChooseFileCommand(self.receiver, self.gui, self.controller)
        self.invoker_choose_file = Invoker()
        self.invoker_choose_file.store_command(self.choose_file_command)
        self.gui.choose_file_button.clicked.connect(self.invoker_choose_file.execute)

        # Invoker for AddSignalCommand
        self.add_signal_command = AddSignalCommand(self.receiver, self.signals_handler, self.gui, self.controller)
        self.invoker_add_signal = Invoker()
        self.invoker_add_signal.store_command(self.add_signal_command)
        self.gui.add_button.clicked.connect(self.invoker_add_signal.execute)

        self.update_plots_command = UpdatePlotsCommand(self.receiver, self.signals_handler, self.gui,
                                                       self.controller)
        self.invoker_update_plots = Invoker()
        self.invoker_update_plots.store_command(self.update_plots_command)
        self.gui.sampling_frequency_edit.valueChanged.connect(self.invoker_update_plots.execute)
        self.gui.samples_number_edit.valueChanged.connect(self.invoker_update_plots.execute)
        self.gui.print_button.clicked.connect(self.invoker_update_plots.execute)

        # Invoker for DeleteSignalCommand
        self.delete_signal_command = DeleteSignalCommand(self.receiver, self.signals_handler, self.gui, self.controller)
        self.invoker_delete_signal = Invoker()
        self.invoker_delete_signal.store_command(self.delete_signal_command)
        self.gui.delete_signal_button.clicked.connect(self.invoker_delete_signal.execute)

        # Invoker for UpdateSignalCommand
        self.update_signal_command = UpdateSignalCommand(self.receiver, self.signals_handler, self.gui, self.controller)
        self.invoker_update_signal = Invoker()
        self.invoker_update_signal.store_command(self.update_signal_command)
        self.gui.amplitude_edit.valueChanged.connect(self.invoker_update_signal.execute)
        self.gui.amplitude_edit.valueChanged.connect(self.invoker_update_plots.execute)
        self.gui.frequency_edit.valueChanged.connect(self.invoker_update_signal.execute)
        self.gui.frequency_edit.valueChanged.connect(self.invoker_update_plots.execute)
        self.gui.phase_edit.valueChanged.connect(self.invoker_update_signal.execute)
        self.gui.phase_edit.valueChanged.connect(self.invoker_update_plots.execute)

        # Show the main window
        self.gui.show()


# Main entry point
if __name__ == '__main__':
    # Create the application and start the event loop
    app = App(sys.argv)
    sys.exit(app.exec_())
