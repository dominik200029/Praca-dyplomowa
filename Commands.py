from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def execute(self):
        pass


class AddSignalCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller

    def execute(self):
        self.receiver.add_signal_to_list(self.signals_handler, self.controller)
        self.gui.update_label(self.gui.signal_label, self.signals_handler.get_text())


class UpdatePlotsCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller, canvas):
        super().__init__(receiver)
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller
        self.canvas = canvas

    def execute(self):
        if self.gui.wave_from_file.isChecked():
            self.receiver.update_plots_from_file(self.controller, self.signals_handler, self.canvas)
        else:
            self.receiver.update_plots(self.controller, self.signals_handler, self.canvas)


class DeleteSignalCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.controller = controller
        self.signals_handler = signals_handler
        self.gui = gui

    def execute(self):
        self.receiver.delete_signal(self.signals_handler, self.controller)
        self.gui.update_label(self.gui.signal_label, self.signals_handler.get_text())


class UpdateSignalCommand(Command):
    def __init__(self, receiver, signals_handler, gui, controller):
        super().__init__(receiver)
        self.receiver = receiver
        self.signals_handler = signals_handler
        self.gui = gui
        self.controller = controller

    def execute(self):
        self.receiver.update_signal(self.signals_handler, self.controller)
        self.gui.update_label(self.gui.signal_label, self.signals_handler.get_text())


class ChooseFileCommand(Command):
    def __init__(self, receiver, gui):
        super().__init__(receiver)
        self.gui = gui

    def execute(self):
        self.receiver.choose_file(self.gui)


class CreateWindowCommand(Command):
    def __init__(self, receiver, name):
        super().__init__(receiver)
        self.name = name

    def execute(self):
        self.receiver.create_figure(self.name)
