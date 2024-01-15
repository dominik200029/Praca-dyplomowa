import os

from PyQt5.QtWidgets import QFileDialog

from SignalsHandler import SignalsHandler
from Signal import Signal
from AxisHandler import AxisHandler
from TransformAnalyzer import TransformAnalyzer
from WavFileHandler import WavFileHandler

import numpy as np

""" Class responsible for """


class Receiver:
    @staticmethod
    def add_signal_to_list(signals_handler: SignalsHandler, signal: Signal):
        signals_handler.append_signal(signal)

    @staticmethod
    def update_plots(gui, data, signals_handler: SignalsHandler):
        gui.clear_all()

        axis_handler = AxisHandler(data)
        time_axis = axis_handler.generate_time_axis()
        discrete_time_axis = axis_handler.generate_discrete_time_axis()
        frequency_axis = axis_handler.generate_frequency_axis()
        wave, sampled_wave = signals_handler.generate_wave(time_axis, discrete_time_axis)
        fft_data = TransformAnalyzer(sampled_wave).calculate_fft()
        ifft_data = TransformAnalyzer(fft_data).calculate_ifft()
        dct_data = TransformAnalyzer(sampled_wave).calculate_dct()
        idct_data = TransformAnalyzer(dct_data).calculate_idct()

        gui.update_canvas('signal', time_axis, wave, 'Original signal', 'plot', 'Time',
                          'Amplitude')
        gui.update_canvas('signal', discrete_time_axis, sampled_wave, 'Original signal', 'stem', 'Time',
                          'Amplitude')
        gui.update_canvas('fft', frequency_axis, abs(fft_data), 'abs(FFT)', 'stem', 'Frequency',
                          'Amplitude')
        gui.update_canvas('ifft', discrete_time_axis, np.real(ifft_data), 'Inverse FFT', 'stem', 'Time',
                          'Amplitude')
        gui.update_canvas('dct', frequency_axis, dct_data, 'DCT', 'stem', 'Frequency', 'Amplitude')
        gui.update_canvas('idct', discrete_time_axis, np.real(idct_data), 'IDCT', 'stem', 'Time', 'Amplitude')

    @staticmethod
    def update_plots_from_file(filename, signals_handler: SignalsHandler, data, gui):
        axis_handler = AxisHandler(data)
        wave, time_axis, file_sampling_frequency = signals_handler.generate_wave_from_file(filename)
        axis_handler.sampling_frequency = file_sampling_frequency
        axis_handler.samples_number = len(wave)
        frequency_axis = axis_handler.generate_frequency_axis()
        fft_data = TransformAnalyzer(wave).calculate_fft()
        ifft_data = TransformAnalyzer(fft_data).calculate_ifft()
        dct_data = TransformAnalyzer(wave).calculate_dct()
        idct_data = TransformAnalyzer(dct_data).calculate_idct()
        gui.update_canvas('signal', time_axis, wave, 'Original signal from file', 'plot', 'Time',
                          'Amplitude')
        gui.update_canvas('fft', frequency_axis, abs(fft_data), 'abs(FFT)', 'stem', 'Frequency',
                          'Amplitude')
        gui.update_canvas('ifft', time_axis, np.real(ifft_data), 'Inverse FFT', 'stem', 'Time',
                          'Amplitude')
        gui.update_canvas('dct', frequency_axis, dct_data, 'DCT', 'stem', 'Frequency', 'Amplitude')
        gui.update_canvas('idct', time_axis, np.real(idct_data), 'IDCT', 'stem', 'Time', 'Amplitude')

    @staticmethod
    def delete_signal(signals_handler: SignalsHandler, number):
        signals_handler.signals.pop(number)
        signals_handler.signals_labels.pop(number)

    @staticmethod
    def update_signal(signals_handler: SignalsHandler, data, number):
        signal = signals_handler.signals[number]
        signal.amplitude = data['amplitude']
        signal.frequency = data['frequency']
        signal.phase = data['phase']
        signals_handler.signals_labels[number] = signal.signal_to_text()

    @staticmethod
    def choose_file(gui, controller):
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
                controller.filename = filename_with_extension
                gui.file_name.setPlainText(filename_with_extension)
