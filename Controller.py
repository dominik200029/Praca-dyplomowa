from Gui import Gui

""" Class responsible for collecting data from user """


class Controller:
    def __init__(self, view, signal_handler):
        # Initialize the model, view, and lists to store signal parameters
        self.view = view
        self.signal_handler = signal_handler
        self.filename = ''

    def collect_signal_data(self):
        # Collect amplitude, frequency, and phase data from the user input
        amplitude_text = self.view.amplitude_edit.text()
        frequency_text = self.view.frequency_edit.text()
        phase_text = self.view.phase_edit.text()

        if not (amplitude_text and frequency_text and phase_text):
            Gui.print_error("Enter all the data required")
            return None

        amplitude = float(amplitude_text)
        frequency = float(frequency_text)
        phase = float(phase_text)

        data = {
            'amplitude': amplitude,
            'frequency': frequency,
            'phase': phase
        }
        return data

    def collect_axis_data(self):
        # Collect time step, sampling frequency, and samples number data from the user input
        time_step_text = self.view.time_step_edit.text()
        sampling_frequency_text = self.view.sampling_frequency_edit.text()
        samples_number_text = self.view.samples_number_edit.text()

        try:
            time_step = float(time_step_text)
            sampling_frequency = float(sampling_frequency_text)
            samples_number = int(samples_number_text)

            # Check if all data is greater than zero
            if time_step > 0 and sampling_frequency > 0 and samples_number > 0:
                data = {
                    'time_step': time_step,
                    'sampling_frequency': sampling_frequency,
                    'samples_number': samples_number
                }
                return data
            else:
                Gui.print_error("Every variable has to be greater than zero")
                return None

        except ValueError:
            Gui.print_error("Wrong data format. Please enter numbers only")

    def collect_signal_number(self):
        signal_number_text = self.view.signal_number_edit.text()
        signals_amount = self.signal_handler.signal_amount
        try:
            signal_number = int(signal_number_text)
            if 0 > signal_number > signals_amount:
                Gui.print_error("Signal number has to be greater than zero and less than amount of signals")
                return None
            else:
                return signal_number
        except ValueError:
            Gui.print_error("Wrong data format. Please enter numbers only")
