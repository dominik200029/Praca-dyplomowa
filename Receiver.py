import numpy as np
from PyQt5.QtWidgets import QFileDialog
from Graph import Plot, StemPlot
from Signal import Sine
from Axis import TimeAxis, DiscreteTimeAxis, FrequencyAxis
from TransformAnalyzer import FFTAnalyzer, IFFTAnalyzer, DCTAnalyzer, IDCTAnalyzer


class Receiver:
    def __init__(self):
        self.fft_data = None
        self.ifft_data = None
        self.dct_data = None
        self.idct_data = None
        self.wave = None
        self.sampled_wave = None
        self.frequency_axis = None
        self.time_axis = None
        self.discrete_time_axis = None
        self.filtered_fft = None
        self.filtered_ifft = None
        self.filtered_dct = None
        self.filtered_idct = None
        self.is_signal_from_file = False

    @staticmethod
    def add_signal_to_list(signals_handler, controller):
        amplitude = controller.get_amplitude()
        frequency = controller.get_frequency()
        phase = controller.get_phase()

        if amplitude and frequency and phase:
            signal = Sine(amplitude, frequency, phase)
            signals_handler.append_signal(signal)

    def calculate_axis(self, controller):
        samples_number = controller.get_samples_number()
        sampling_frequency = controller.get_sampling_frequency()
        time_step = controller.get_time_step()

        if samples_number and sampling_frequency and time_step:
            self.time_axis = TimeAxis(samples_number, sampling_frequency, time_step).generate()
            self.discrete_time_axis = DiscreteTimeAxis(samples_number, sampling_frequency).generate()
            self.frequency_axis = FrequencyAxis(samples_number, sampling_frequency).generate()
        else:
            controller.print_error('Wybierz poprawne wartości')
            return

    def calculate_wave(self, signals_handler):
        self.wave = signals_handler.generate_wave(self.time_axis)
        self.sampled_wave = signals_handler.generate_wave(self.discrete_time_axis)

    def calculate_fft(self):
        self.fft_data = FFTAnalyzer(self.sampled_wave).calculate()
        self.ifft_data = IFFTAnalyzer(self.fft_data).calculate()

    def calculate_dct(self):
        self.dct_data = DCTAnalyzer(self.sampled_wave).calculate()
        self.idct_data = IDCTAnalyzer(self.dct_data).calculate()

    def update_signal_plot(self, canvas):
        signal_plot = Plot(self.time_axis, self.wave, 'Czas[s]', 'Amplituda', 'Sygnał oryginalny')
        sampled_signal_plot = StemPlot(self.discrete_time_axis, self.sampled_wave, 'Czas[s]', 'Amplituda',
                                       'Sygnał oryginalny')
        canvas.clear()
        signal_plot.create_on_canvas(canvas)
        sampled_signal_plot.create_on_canvas(canvas)

    def filtered_fft_plot(self, *canvases):
        if self.is_signal_from_file:
            fft_plot = Plot(self.frequency_axis, np.abs(self.filtered_fft), 'Częstotliwość[Hz]', 'Amplituda', 'abs(FFT)')
            ifft_plot = Plot(None, np.real(self.filtered_ifft), 'Czas[s]', 'Amplituda', 'IFFT')
        else:
            fft_plot = StemPlot(self.frequency_axis, np.abs(self.filtered_fft), 'Częstotliwość[Hz]', 'Amplituda',
                                'abs(FFT)')
            ifft_plot = StemPlot(self.discrete_time_axis, np.real(self.filtered_ifft), 'Czas[s]', 'Amplituda', 'IFFT')

        for canvas in canvases:
            canvas.clear()

        fft_plot.create_on_canvas(canvases[0])
        ifft_plot.create_on_canvas(canvases[1])

    def filtered_dct_plot(self, *canvases):
        if self.is_signal_from_file:
            dct_plot = Plot(self.frequency_axis, np.abs(self.filtered_dct), 'Częstotliwość[Hz]', 'Amplituda',
                            'abs(DCT)')
            idct_plot = Plot(None, np.real(self.filtered_idct), 'Czas[s]', 'Amplituda', 'IDCT')
        else:
            dct_plot = StemPlot(self.frequency_axis, np.abs(self.filtered_dct), 'Częstotliwość[Hz]', 'Amplituda',
                                'abs(DCT)')
            idct_plot = StemPlot(self.discrete_time_axis, np.real(self.filtered_idct), 'Czas[s]', 'Amplituda', 'IDCT')

        for canvas in canvases:
            canvas.clear()

        dct_plot.create_on_canvas(canvases[0])
        idct_plot.create_on_canvas(canvases[1])

    def update_fft_plot(self, canvas):
        if self.is_signal_from_file:
            fft_plot = Plot(self.frequency_axis, np.abs(self.fft_data), 'Częstotliwość[Hz]', 'Amplituda', 'abs(FFT)')
        else:
            fft_plot = StemPlot(self.frequency_axis, np.abs(self.fft_data), 'Częstotliwość[Hz]', 'Amplituda', 'abs(FFT)')

        canvas.clear()
        fft_plot.create_on_canvas(canvas)

    def update_ifft_plot(self, canvas):
        if self.is_signal_from_file:
            ifft_plot = Plot(None, np.real(self.ifft_data), 'Czas[s]', 'Amplituda', 'IFFT')
        else:
            ifft_plot = StemPlot(self.discrete_time_axis, np.real(self.ifft_data), 'Czas[s]', 'Amplituda', 'IFFT')

        canvas.clear()
        ifft_plot.create_on_canvas(canvas)

    def update_dct_plot(self, canvas):
        if self.is_signal_from_file:
            dct_plot = Plot(self.frequency_axis, np.abs(self.dct_data), 'Częstotliwość[Hz]', 'Amplituda', 'abs(DCT)')
        else:
            dct_plot = StemPlot(self.frequency_axis, np.abs(self.dct_data), 'Częstotliwość[Hz]', 'Amplituda', 'abs(DCT)')

        canvas.clear()
        dct_plot.create_on_canvas(canvas)

    def update_idct_plot(self, canvas):
        if self.is_signal_from_file:
            idct_plot = Plot(None, np.real(self.idct_data), 'Czas[s]', 'Amplituda', 'IDCT')
        else:
            idct_plot = StemPlot(self.discrete_time_axis, np.real(self.idct_data), 'Czas[s]', 'Amplituda', 'IDCT')

        canvas.clear()
        idct_plot.create_on_canvas(canvas)

    def update_plots_from_file(self, controller, signals_handler, *canvases):
        if controller.wav_file_check_box_state():
            filename = controller.get_wav_file()
            if filename:
                self.wave, sampling_frequency = signals_handler.generate_from_file(filename)
                samples_number = len(self.wave)
                self.fft_data = FFTAnalyzer(self.wave).calculate()[:samples_number//2]
                self.ifft_data = IFFTAnalyzer(self.fft_data).calculate()

                self.frequency_axis = FrequencyAxis(samples_number, sampling_frequency).generate()
                self.frequency_axis = self.frequency_axis[:samples_number//2]

                self.dct_data = DCTAnalyzer(self.wave).calculate()[:samples_number//2]
                self.idct_data = IDCTAnalyzer(self.dct_data).calculate()

                signal_plot = Plot(None, self.wave, 'Czas', 'Amplituda', 'Sygnał oryginalny')

                fft_plot = Plot(self.frequency_axis, np.abs(self.fft_data), 'Częstotliwość', 'Amplituda',
                                'abs(FFT)')
                idft_plot = Plot(None, np.real(self.ifft_data), 'Czas', 'Amplituda', 'IFFT')

                dct_plot = Plot(self.frequency_axis, np.abs(self.dct_data), 'Częstotliwość', 'Amplituda',
                                'abs(DCT)')
                idct_plot = Plot(None, np.real(self.idct_data), 'Czas', 'Amplituda', 'abs(IDCT)')

                for canvas in canvases:
                    canvas.clear()

                signal_plot.create_on_canvas(canvases[0])

                fft_plot.create_on_canvas(canvases[1])
                idft_plot.create_on_canvas(canvases[2])

                dct_plot.create_on_canvas(canvases[3])
                idct_plot.create_on_canvas(canvases[4])

    @staticmethod
    def delete_signal(signals_handler, controller):
        signal_number = controller.get_signal_number()
        if signal_number:
            index = signal_number - 1
            signal_amount = signals_handler.signal_amount

            list_of_signals = signals_handler.signals
            list_of_signals_labels = signals_handler.signals_labels

            if list_of_signals and list_of_signals_labels and 0 <= index < signal_amount:
                list_of_signals.pop(index)
                list_of_signals_labels.pop(index)
                signals_handler.signal_amount -= 1
        else:
            controller.print_error('Aby usunać daną składową, musisz zaznaczyć pole.')

    @staticmethod
    def update_signal(signals_handler, controller):
        signal_number = controller.get_signal_number()
        if signal_number:
            index = signal_number - 1
            if index < signals_handler.signal_amount:
                signal = signals_handler.signals[index]
            else:
                controller.print_error('Numer składowej nie może być większy niż ich ilość. Wpisz poprawny numer lub '
                                       'odznacz pole.')
                return

            amplitude = controller.get_amplitude()
            frequency = controller.get_frequency()
            phase = controller.get_phase()

            if amplitude and frequency and phase:
                signal.amplitude = amplitude
                signal.frequency = frequency
                signal.phase = phase

            signals_handler.signals_labels[index] = signal.signal_to_text()

    @staticmethod
    def handle_list_of_filters(controller):
        filter_type = controller.get_filters_list_index()
        if filter_type == 0:
            controller.set_box_access(True, True, True)
        elif filter_type == 1:
            controller.set_box_access(True, True, False)
        elif filter_type == 2:
            controller.set_box_access(True, True, False)
        elif filter_type == 3:
            controller.set_box_access(False, False, True)
        elif filter_type == 4:
            controller.set_box_access(False, False, True)

    def filter_fft(self, controller):
        filter_type = controller.filters_list.currentIndex()
        self.filtered_fft = np.copy(self.fft_data)
        indices_to_zero = []
        if filter_type == 1:
            cut_off_frequency = controller.get_cut_off_frequency()
            if controller.apply_check_box_state() and cut_off_frequency is not None:
                indices_to_zero = np.where(self.frequency_axis > cut_off_frequency)
        elif filter_type == 2:
            cut_off_frequency = controller.get_cut_off_frequency()
            if controller.apply_check_box_state() and cut_off_frequency is not None:
                indices_to_zero = np.where(self.frequency_axis < cut_off_frequency)
        elif filter_type == 3:
            low_cut_off_frequency = controller.get_low_cut_off_frequency()
            high_cut_off_frequency = controller.get_high_cut_off_frequency()
            if low_cut_off_frequency >= high_cut_off_frequency:
                controller.print_error('Dolna częstotliwość nie może być większa niż górna.')
                controller.low_cut_off.setValue(low_cut_off_frequency - 1)
                return
            if (controller.apply_check_box_state() and low_cut_off_frequency is not None
                    and high_cut_off_frequency is not None):
                indices_to_zero = (
                        (self.frequency_axis < low_cut_off_frequency)
                        | (self.frequency_axis > high_cut_off_frequency)
                )
        elif filter_type == 4:
            low_cut_off_frequency = controller.get_low_cut_off_frequency()
            high_cut_off_frequency = controller.get_high_cut_off_frequency()
            if low_cut_off_frequency >= high_cut_off_frequency:
                controller.print_error('Dolna częstotliwość nie może być większa niż górna.')
                controller.low_cut_off.setValue(low_cut_off_frequency - 1)
                return
            if (controller.apply_check_box_state() and low_cut_off_frequency is not None
                    and high_cut_off_frequency is not None):
                indices_to_zero = (
                        (low_cut_off_frequency < self.frequency_axis)
                        & (self.frequency_axis < high_cut_off_frequency)
                )
        else:
            controller.print_error('Wybierz filtr')
            return

        self.filtered_fft[indices_to_zero] = 0
        self.filtered_ifft = IFFTAnalyzer(self.filtered_fft).calculate()

    def filter_dct(self, controller):
        filter_type = controller.filters_list.currentIndex()
        self.filtered_dct = np.copy(self.dct_data)
        indices_to_zero = []
        if filter_type == 1:
            cut_off_frequency = controller.get_cut_off_frequency()
            if controller.apply_check_box_state() and cut_off_frequency is not None:
                indices_to_zero = np.where(self.frequency_axis > cut_off_frequency)
        elif filter_type == 2:
            cut_off_frequency = controller.get_cut_off_frequency()
            if controller.apply_check_box_state() and cut_off_frequency is not None:
                indices_to_zero = np.where(self.frequency_axis < cut_off_frequency)
        elif filter_type == 3:
            low_cut_off_frequency = controller.get_low_cut_off_frequency()
            high_cut_off_frequency = controller.get_high_cut_off_frequency()
            if low_cut_off_frequency >= high_cut_off_frequency:
                controller.print_error('Dolna częstotliwość nie może być większa niż górna.')
                controller.low_cut_off.setValue(low_cut_off_frequency - 1)
                return
            if (controller.apply_check_box_state() and low_cut_off_frequency is not None
                    and high_cut_off_frequency is not None):
                indices_to_zero = (
                        (self.frequency_axis < low_cut_off_frequency)
                        | (self.frequency_axis > high_cut_off_frequency)
                )
        elif filter_type == 4:
            low_cut_off_frequency = controller.get_low_cut_off_frequency()
            high_cut_off_frequency = controller.get_high_cut_off_frequency()
            if low_cut_off_frequency >= high_cut_off_frequency:
                controller.print_error('Dolna częstotliwość nie może być większa niż górna.')
                controller.low_cut_off.setValue(low_cut_off_frequency - 1)
                return
            if (controller.apply_check_box_state() and low_cut_off_frequency is not None
                    and high_cut_off_frequency is not None):
                indices_to_zero = (
                        (low_cut_off_frequency < self.frequency_axis)
                        & (self.frequency_axis < high_cut_off_frequency)
                )
        else:
            controller.print_error('Wybierz filtr')
            return

        self.filtered_dct[indices_to_zero] = 0
        self.filtered_idct = IDCTAnalyzer(self.filtered_dct).calculate()

    @staticmethod
    def choose_wav_file(controller):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, 'Choose Audio File', filter='WAV files (*.wav);')
        controller.file_name.setPlainText(str(file_path))

    @staticmethod
    def show_window(controller):
        controller.show()

    def set_main_window_inactive(self, condition, controller):
        if condition:
            self.is_signal_from_file = True
            controller.amplitude_edit.setDisabled(True)
            controller.frequency_edit.setDisabled(True)
            controller.phase_edit.setDisabled(True)
            controller.sampling_frequency_edit.setDisabled(True)
            controller.samples_number_edit.setDisabled(True)
            controller.time_step_edit.setDisabled(True)
            controller.signal_number_edit.setDisabled(True)
        else:
            self.is_signal_from_file = False
            controller.amplitude_edit.setDisabled(False)
            controller.frequency_edit.setDisabled(False)
            controller.phase_edit.setDisabled(False)
            controller.sampling_frequency_edit.setDisabled(False)
            controller.samples_number_edit.setDisabled(False)
            controller.time_step_edit.setDisabled(False)
            controller.signal_number_edit.setDisabled(False)
