from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.uic import loadUi


class MainWindowController(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main_window.ui', self)

    @staticmethod
    def update_label(label, text):
        """
        Updates the text content of a QLabel.

        Parameters:
        - label (QLabel): The QLabel to be updated.
        - text (str): The new text content.

        Returns:
        - None
        """
        label.setPlainText(text)

    @staticmethod
    def print_error(message):
        """
        Displays an error message in a QMessageBox.

        Parameters:
        - message (str): The error message to be displayed.

        Returns:
        - None
        """
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.exec_()

    def get_from_line_edit(self, line_edit, error_message, value_to_return):
        """
                Get a float value from a QLineEdit.

                Parameters:
                    line_edit: The QLineEdit widget.
                    error_message: The error message to be displayed if the input is not valid.
                    value_to_return: 'float' or 'int' depends on the variable to return

                Returns: float or int or None: The float value if value == float, int if value == int, or None if
                there was an error.
        """
        text = line_edit.text()
        if text:
            try:
                if value_to_return == 'float':
                    return float(text)
                elif value_to_return == 'int':
                    return int(text)
                else:
                    raise ValueError
            except ValueError:
                self.print_error('Invalid input. Please enter a valid number.')
        else:
            self.print_error(error_message)

    def get_amplitude(self):
        """
        Get the amplitude from the GUI.

        Returns:
            float or None: The amplitude if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.amplitude_edit, 'Enter amplitude', 'float')

    def get_frequency(self):
        """
        Get the frequency from the GUI.

        Returns:
            float or None: The frequency if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.frequency_edit, 'Enter frequency', 'float')

    def get_phase(self):
        """
        Get the phase from the GUI.

        Returns:
            float or None: The phase if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.phase_edit, 'Enter phase', 'float')

    def get_time_step(self):
        """
        Get the time step from the GUI.

        Returns: float or None: The time step if successful and greater than 0, or None if there was an error or the
        value is <= 0.
        """
        time_step = self.get_from_line_edit(self.time_step_edit, 'Enter time step', 'float')

        if time_step is not None and time_step > 0:
            return time_step
        else:
            return None

    def get_sampling_frequency(self):
        """
        Get the sampling frequency from the GUI.

        Returns:
            float or None: The sampling frequency if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.sampling_frequency_edit, 'Enter sampling frequency', 'float')

    def get_samples_number(self):
        """
        Get the number of samples from the GUI.

        Returns:
            float or None: The number of samples if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.samples_number_edit, 'Enter samples number', 'int')

    def get_signal_number(self):
        """
        Get the signal number from the GUI.

        Returns:
            float or None: The signal number if successful, or None if there was an error.
        """
        if self.signal_number.isChecked():
            return self.get_from_line_edit(self.signal_number_edit, 'Enter signal number', 'int')
        else:
            return None

    def get_wav_file(self):
        """
        Get the filename from the GUI.

        Returns:
            str or None: The filename if successful, or None if there was an error.
        """
        filename = self.file_name.toPlainText()
        if filename:
            return filename
        else:
            self.print_error('Wybierz plik dźwiękowy')
            return None

    def wav_file_check_box_state(self) -> bool:
        return self.file_check_box.isChecked()

    def jpg_file_check_box_state(self) -> bool:
        return self.image_file_checkBox.isChecked()

    def get_jpg_file(self):
        file = self.image_file_name.toPlainText()
        if file:
            return file
        else:
            self.print_error('Wybierz plik JPG')
            return None


class DFTWindowController(MainWindowController):
    def __init__(self):
        super().__init__()
        loadUi('dft_window.ui', self)

    def get_cut_off_frequency(self) -> float:
        return self.cut_off_edit.value()

    def get_low_cut_off_frequency(self) -> float:
        return self.low_cut_off.value()

    def get_high_cut_off_frequency(self) -> float:
        return self.high_cut_off.value()

    def apply_check_box_state(self) -> bool:
        return self.apply_check_box.isChecked()

    def get_filters_list_index(self) -> int:
        return self.filters_list.currentIndex()

    def set_box_access(self, low_access: bool, high_access: bool, cut_off_access: bool) -> None:
        # True is inactive, and False is active
        self.low_cut_off.setDisabled(low_access)
        self.high_cut_off.setDisabled(high_access)
        self.cut_off_edit.setDisabled(cut_off_access)


class DCTWindowController(DFTWindowController):
    def __init__(self):
        super().__init__()
        loadUi('dct_window.ui', self)
