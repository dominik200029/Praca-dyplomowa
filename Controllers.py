from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi

from Canvas import Canvas
from Graph import EmptyPlot


class Window(QMainWindow):
    """
    Base class representing a window.

    Attributes:
        None

    Methods:
        update_label(label, text): Updates the text content of a QLabel.
        print_error(message): Displays an error message in a QMessageBox.
        plot_warning(canvas): Clears the canvas and plots a warning message.
    """

    def __init__(self):
        """
        Initializes a Window instance.
        """
        super().__init__()

    @staticmethod
    def update_label(label, text):
        """
        Updates the text content of a QLabel.

        Parameters:
            label (QLabel): The QLabel to be updated.
            text (str): The new text content.

        Returns:
            None
        """
        label.setPlainText(text)

    @staticmethod
    def print_error(message):
        """
        Displays an error message in a QMessageBox.

        Parameters:
            message (str): The error message to be displayed.

        Returns:
            None
        """
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()

    @staticmethod
    def plot_warning(canvas):
        """
        Clears the canvas and plots a warning message.

        Parameters:
            canvas: The canvas to plot the warning on.

        Returns:
            None
        """
        canvas.clear()
        empty_plot = EmptyPlot('Dodaj sygnał, aby wyświetlić wykres')
        empty_plot.create_on_canvas(canvas)


class MainWindowController(Window):
    """
    Controller class for the main window.

    Attributes:
        None

    Methods:
        get_amplitude(): Gets the amplitude value.
        get_frequency(): Gets the frequency value.
        get_phase(): Gets the phase value.
        get_time_step(): Gets the time step value.
        get_sampling_frequency(): Gets the sampling frequency value.
        get_samples_number(): Gets the number of samples value.
        get_signal_number(): Gets the signal number value.
        get_wav_file(): Gets the WAV file path.
        wav_file_check_box_state(): Checks the state of the WAV file check box.
        jpg_file_check_box_state(): Checks the state of the JPG file check box.
        get_jpg_file(): Gets the JPG file path.
        get_frequency_x(): Gets the spatial frequency value.
        get_angle(): Gets the angle value.
    """

    def __init__(self):
        """
        Initializes a MainWindowController instance.
        """
        super().__init__()
        loadUi('main_window.ui', self)
        self.signal_canvas = Canvas(self.signal_layout)
        self.plot_warning(self.signal_canvas)
        self.image_canvas = Canvas(self.image_layout)
        self.plot_warning(self.image_canvas)

    def get_amplitude(self) -> float:
        """Gets the amplitude value."""
        return self.amplitude_spinBox.value()

    def get_frequency(self) -> float:
        """Gets the frequency value."""
        return self.frequency_spinBox.value()

    def get_phase(self) -> float:
        """Gets the phase value."""
        return self.phase_spinBox.value()

    def get_time_step(self) -> float:
        """Gets the time step value."""
        return self.time_step_spinBox.value()

    def get_sampling_frequency(self) -> float:
        """Gets the sampling frequency value."""
        return self.sampling_frequency_spinBox.value()

    def get_samples_number(self) -> int:
        """Gets the number of samples value."""
        return self.samples_number_spinBox.value()

    def get_signal_number(self) -> int:
        """Gets the signal number value."""
        if self.signal_number_checkBox.isChecked():
            return self.signal_number_spinBox.value()

    def get_wav_file(self):
        """Gets the WAV file path."""
        filepath = self.file_name.toPlainText()
        if filepath:
            return filepath
        else:
            self.print_error('Wybierz plik dźwiękowy')
            return None

    def wav_file_check_box_state(self) -> bool:
        """Checks the state of the WAV file check box."""
        return self.file_checkBox.isChecked()

    def jpg_file_check_box_state(self) -> bool:
        """Checks the state of the JPG file check box."""
        return self.image_file_checkBox.isChecked()

    def get_jpg_file(self):
        """Gets the JPG file path."""
        filepath = self.image_file_name.toPlainText()
        if filepath:
            return filepath
        else:
            self.print_error('Wybierz plik JPG')
            return None

    def get_frequency_x(self) -> float:
        """Gets the x-axis frequency value."""
        return self.frequency_x.value()

    def get_angle(self) -> float:
        """Gets the angle value."""
        return self.angle.value()


class DFTWindowController(Window):
    """
    Controller class for the DFT window.

    Attributes:
        None

    Methods:
        get_cut_off_frequency(): Gets the cut-off frequency value.
        get_low_cut_off_frequency(): Gets the low cut-off frequency value.
        get_high_cut_off_frequency(): Gets the high cut-off frequency value.
        get_filters_list_index(): Gets the index of the selected filter from the filters list.
        set_spinBoxes_access(): Sets the accessibility of spin boxes based on arguments.
    """

    def __init__(self):
        """
        Initializes a DFTWindowController instance.
        """
        super().__init__()
        loadUi('dft_window.ui', self)
        self.dft_canvas = Canvas(self.dft_layout)
        self.plot_warning(self.dft_canvas)
        self.idft_canvas = Canvas(self.idft_layout)
        self.plot_warning(self.idft_canvas)

    def get_cut_off_frequency(self) -> float:
        """Gets the cut-off frequency value."""
        return self.cut_off_frequency_spinBox.value()

    def get_low_cut_off_frequency(self) -> float:
        """Gets the low cut-off frequency value."""
        return self.low_cut_off_frequency_spinBox.value()

    def get_high_cut_off_frequency(self) -> float:
        """Gets the high cut-off frequency value."""
        return self.high_cut_off_frequency_spinBox.value()

    def get_filters_list_index(self) -> int:
        """Gets the index of the selected filter from the filters list."""
        return self.filters_list.currentIndex()

    def set_spinBoxes_access(self, low_cut_off_frequency_access: bool, high_cut_off_frequency_access: bool,
                             cut_off_frequency_access: bool) -> None:
        """
        Sets the accessibility of spin boxes based on arguments.

        Parameters:
            low_cut_off_frequency_access (bool): Accessibility status for low cut-off frequency spin box.
            high_cut_off_frequency_access (bool): Accessibility status for high cut-off frequency spin box.
            cut_off_frequency_access (bool): Accessibility status for cut-off frequency spin box.

        Returns:
            None
        """


class DCTWindowController(DFTWindowController):
    """
    Controller class for the DCT window.

    Attributes:
        None

    Methods:
        None
    """

    def __init__(self):
        """
        Initializes a DCTWindowController instance.
        """
        super().__init__()
        loadUi('dct_window.ui', self)
        self.dct_canvas = Canvas(self.dct_layout)
        self.plot_warning(self.dct_canvas)
        self.idct_canvas = Canvas(self.idct_layout)
        self.plot_warning(self.idct_canvas)


class DFT2DWindowController(Window):
    """
    Controller class for the 2D DFT window.

    Attributes:
        None

    Methods:
        get_column(): Gets the column value.
        get_row(): Gets the row value.
        get_filters_list_index(): Gets the index of the selected filter from the filters list.
    """

    def __init__(self):
        """
        Initializes a DFT2DWindowController instance.
        """
        super().__init__()
        loadUi('2d_dft_window.ui', self)
        self.dft2D_canvas = Canvas(self.dft2D_layout)
        self.idft2D_canvas = Canvas(self.idft2D_layout)

    def get_column(self) -> int:
        """Gets the column value."""
        return self.column.value()

    def get_row(self) -> int:
        """Gets the row value."""
        return self.row.value()

    def get_filters_list_index(self) -> int:
        """Gets the index of the selected filter from the filters list."""
        return self.filters_list.currentIndex()


class DCT2DWindowController(DFT2DWindowController):
    """
    Controller class for the 2D DCT window.

    Attributes:
        None

    Methods:
        None
    """

    def __init__(self):
        """
        Initializes a DCT2DWindowController instance.
        """
        super().__init__()
        loadUi('2d_dct_window.ui', self)
        self.dct2D_canvas = Canvas(self.dct2D_layout)
        self.idct2D_canvas = Canvas(self.idct2D_layout)
