import os

import numpy as np
from PyQt5.QtWidgets import QFileDialog
from Figure import Figure
from Graph import Plot, StemPlot
from Signal import Sine
from SignalsHandler import SignalsHandler
from Axis import TimeAxis, DiscreteTimeAxis, FrequencyAxis
from TransformAnalyzer import FFTAnalyzer, IFFTAnalyzer, DCTAnalyzer, IDCTAnalyzer
from Gui import Gui


class Receiver:
    @staticmethod
    def add_signal_to_list(signals_handler: SignalsHandler, controller):
        amplitude = controller.get_amplitude()
        frequency = controller.get_frequency()
        phase = controller.get_phase()
        if amplitude and frequency and phase:
            signal = Sine(amplitude, frequency, phase)
            signals_handler.append_signal(signal)

    @staticmethod
    def update_plots(controller, signals_handler: SignalsHandler, canvas):
        canvas.clear_canvas()

        dft_figure = Figure.get_figure_by_name('DFT')
        dct_figure = Figure.get_figure_by_name('DCT')
        idft_figure = Figure.get_figure_by_name('IDFT')
        idct_figure = Figure.get_figure_by_name('IDCT')

        samples_number = controller.get_samples_number()
        sampling_frequency = controller.get_sampling_frequency()
        time_step = controller.get_time_step()

        time_axis = TimeAxis(samples_number, sampling_frequency, time_step).generate()
        discrete_time_axis = DiscreteTimeAxis(samples_number, sampling_frequency).generate()
        frequency_axis = FrequencyAxis(samples_number, sampling_frequency).generate()

        wave, sampled_wave = signals_handler.generate_wave(time_axis, discrete_time_axis)

        fft_data = FFTAnalyzer(sampled_wave).calculate()
        ifft_data = IFFTAnalyzer(fft_data).calculate()
        dct_data = DCTAnalyzer(sampled_wave).calculate()
        idct_data = IDCTAnalyzer(dct_data).calculate()

        signal_plot = Plot(time_axis, wave, 'Czas', 'Amplituda', 'Sygnał oryginalny')
        sampled_signal_plot = StemPlot(discrete_time_axis, sampled_wave, 'Czas', 'Amplituda', 'Sygnał oryginalny')

        fft_plot = StemPlot(frequency_axis, np.abs(fft_data), 'Częstotliwość', 'Amplituda', 'abs(FFT)')
        idft_plot = StemPlot(discrete_time_axis, np.real(ifft_data), 'Czas', 'Amplituda', 'IFFT')

        dct_plot = StemPlot(frequency_axis, np.abs(dct_data), 'Częstotliwość', 'Amplituda', 'abs(DCT)')
        idct_plot = StemPlot(discrete_time_axis, np.real(idct_data), 'Czas', 'Amplituda', 'IDCT')

        signal_plot.create_on_canvas(canvas)
        sampled_signal_plot.create_on_canvas(canvas)

        if dft_figure:
            dft_figure.clf()
            fft_plot.create(dft_figure)
        if dct_figure:
            dct_figure.clf()
            dct_plot.create(dct_figure)
        if idft_figure:
            idft_figure.clf()
            idft_plot.create(idft_figure)
        if idct_figure:
            idct_figure.clf()
            idct_plot.create(idct_figure)

    @staticmethod
    def update_plots_from_file(controller, signals_handler: SignalsHandler, canvas):
        canvas.clear_canvas()

        dft_figure = Figure.get_figure_by_name('DFT')
        dct_figure = Figure.get_figure_by_name('DCT')
        idft_figure = Figure.get_figure_by_name('IDFT')
        idct_figure = Figure.get_figure_by_name('IDCT')

        filename = controller.get_filename()

        wave, time_axis, sampling_frequency = signals_handler.generate_wave_from_file(filename)
        samples_number = len(wave)

        frequency_axis = FrequencyAxis(samples_number, sampling_frequency).generate()

        fft_data = FFTAnalyzer(wave).calculate()
        ifft_data = IFFTAnalyzer(fft_data).calculate()

        dct_data = DCTAnalyzer(wave).calculate()
        idct_data = IDCTAnalyzer(dct_data).calculate()

        signal_plot = Plot(time_axis, wave, 'Czas', 'Amplituda', 'Sygnał oryginalny')

        fft_plot = StemPlot(frequency_axis, np.abs(fft_data), 'Częstotliwość', 'Amplituda', 'abs(FFT)')
        idft_plot = StemPlot(time_axis, np.real(ifft_data), 'Czas', 'Amplituda', 'IFFT')

        dct_plot = StemPlot(frequency_axis, np.abs(dct_data), 'Częstotliwość', 'Amplituda', 'abs(DCT)')
        idct_plot = StemPlot(time_axis, np.real(idct_data), 'Czas', 'Amplituda', 'abs(IDCT)')

        signal_plot.create_on_canvas(canvas)

        if dft_figure:
            dft_figure.clf()
            fft_plot.create(dft_figure)
        if dct_figure:
            dct_figure.clf()
            dct_plot.create(dct_figure)
        if idft_figure:
            idft_figure.clf()
            idft_plot.create(idft_figure)
        if idct_figure:
            idct_figure.clf()
            idct_plot.create(idct_figure)

    @staticmethod
    def delete_signal(signals_handler: SignalsHandler, controller):
        index = controller.get_signal_number() - 1
        signal_amount = signals_handler.signal_amount

        list_of_signals = signals_handler.signals
        list_of_signals_labels = signals_handler.signals_labels

        if list_of_signals and list_of_signals_labels and 0 <= index < signal_amount:
            list_of_signals.pop(index)
            list_of_signals_labels.pop(index)
            signals_handler.signal_amount -= 1

    @staticmethod
    def update_signal(signals_handler: SignalsHandler, controller):
        signal_number = controller.get_signal_number()
        if signal_number > 0:
            index = signal_number - 1
        else:
            Gui.print_error('Numer składowej nie może być równy 0')
            return
        if index < signals_handler.signal_amount:
            signal = signals_handler.signals[index]
        else:
            Gui.print_error('Numer składowej nie może być większy niż ich ilość.')
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
    def choose_file(gui):
        options = QFileDialog.Options()

        file_dialog = QFileDialog()
        file_dialog.setOptions(options)

        # Set file dialog properties, if needed
        file_dialog.setNameFilter("Wav files (*.wav);;All files (*)")
        file_dialog.setViewMode(QFileDialog.Detail)

        # Show the dialog and get the selected file(s)
        result = file_dialog.exec_()

        if result == QFileDialog.Accepted:
            selected_files = file_dialog.selectedFiles()

            # Process the selected file (only the first one)
            if selected_files:
                selected_file = selected_files[0]
                filename_with_extension = os.path.basename(selected_file)
                gui.file_name.setPlainText(filename_with_extension)

    @staticmethod
    def create_figure(title):
        figure = Figure(title)
        figure.create()
        figure.show()
