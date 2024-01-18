class Controller:
    """
    Controller class for handling input from the GUI.

    Attributes:
        gui: The GUI instance.

    Methods:
        get_from_line_edit(line_edit, error_message): Get a  value from a QLineEdit.
        get_amplitude(): Get the amplitude from the GUI.
        get_frequency(): Get the frequency from the GUI.
        get_phase(): Get the phase from the GUI.
        get_time_step(): Get the time step from the GUI.
        get_sampling_frequency(): Get the sampling frequency from the GUI.
        get_samples_number(): Get the number of samples from the GUI.
        get_signal_number(): Get the signal number from the GUI.
        get_filename(): Get the filename from the GUI.
    """

    def __init__(self, gui):
        """
        Initialize the Controller instance.

        Parameters:
            gui: The GUI instance.
        """
        self.gui = gui
        self.figure = None

    def get_from_line_edit(self, line_edit, error_message, value):
        """
        Get a float value from a QLineEdit.

        Parameters:
            line_edit: The QLineEdit widget.
            error_message: The error message to be displayed if the input is not valid.
            value: 'float' or 'int' depends on the variable to return

        Returns:
            float or int or None: The float value if value == float, int if value == int, or None if there was an error.
        """
        text = line_edit.text()
        if text:
            try:
                if value == 'float':
                    return float(text)
                elif value == 'int':
                    return int(text)
                else:
                    raise ValueError
            except ValueError:
                self.gui.print_error('Invalid input. Please enter a valid number.')
        else:
            self.gui.print_error(error_message)

    def get_amplitude(self):
        """
        Get the amplitude from the GUI.

        Returns:
            float or None: The amplitude if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.gui.amplitude_edit, 'Enter amplitude', 'float')

    def get_frequency(self):
        """
        Get the frequency from the GUI.

        Returns:
            float or None: The frequency if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.gui.frequency_edit, 'Enter frequency', 'float')

    def get_phase(self):
        """
        Get the phase from the GUI.

        Returns:
            float or None: The phase if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.gui.phase_edit, 'Enter phase', 'float')

    def get_time_step(self):
        """
        Get the time step from the GUI.

        Returns:
            float or None: The time step if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.gui.time_step_edit, 'Enter time step', 'float')

    def get_sampling_frequency(self):
        """
        Get the sampling frequency from the GUI.

        Returns:
            float or None: The sampling frequency if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.gui.sampling_frequency_edit, 'Enter sampling frequency', 'float')

    def get_samples_number(self):
        """
        Get the number of samples from the GUI.

        Returns:
            float or None: The number of samples if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.gui.samples_number_edit, 'Enter samples number', 'int')

    def get_signal_number(self):
        """
        Get the signal number from the GUI.

        Returns:
            float or None: The signal number if successful, or None if there was an error.
        """
        return self.get_from_line_edit(self.gui.signal_number_edit, 'Enter signal number', 'int')

    def get_filename(self):
        """
        Get the filename from the GUI.

        Returns:
            str or None: The filename if successful, or None if there was an error.
        """
        filename = self.gui.file_name.toPlainText()
        if filename:
            return filename
        else:
            self.gui.print_error('Choose valid filename')
            return None
