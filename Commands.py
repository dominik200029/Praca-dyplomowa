from abc import ABC, abstractmethod
from Signal import Signal


class Command(ABC):
    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass


class AddSignalCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller

    def execute(self):
        data = self.controller.collect_signal_data()
        if data:
            signal = Signal(data['amplitude'], data['frequency'], data['phase'])
            self.receiver.add_signal_to_list(self.signals_handler, signal)
            self.gui.update_signals_label(self.signals_handler.signals_labels)


class UpdatePlotsCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller

    def execute(self):
        data = self.controller.collect_axis_data()
        if data:
            if self.gui.wave_from_file.isChecked():
                self.receiver.update_plots_from_file(self.controller.filename, self.signals_handler, data, self.gui)
            else:
                self.receiver.update_plots(self.gui, data, self.signals_handler)


class DeleteSignalCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.controller = controller
        self.signals_handler = signals_handler
        self.gui = gui

    def execute(self):
        data = self.controller.collect_signal_number()
        if data:
            element_index = data - 1
            self.receiver.delete_signal(self.signals_handler, element_index)
            self.gui.update_signals_label(self.signals_handler.signals_labels)


class UpdateSignalCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller

    def execute(self):
        signal_number = self.controller.collect_signal_number()
        data = self.controller.collect_signal_data()
        if signal_number and data:
            signal_index = signal_number - 1
            self.receiver.update_signal(self.signals_handler, data, signal_index)
            self.gui.update_signals_label(self.signals_handler.signals_labels)


class ChooseFileCommand(Command):
    def __init__(self, receiver, gui, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.gui = gui
        self.controller = controller

    def execute(self):
        self.receiver.choose_file(self.gui, self.controller)
