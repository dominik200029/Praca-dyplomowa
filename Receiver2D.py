import numpy as np
from PyQt5.QtWidgets import QFileDialog

from Graph import ImagePlot
from Receiver import Receiver
from TransformAnalyzer import FFT2DAnalyzer, IFFT2DAnalyzer, DCT2DAnalyzer, IDCT2DAnalyzer
from Signal import Sine2D


class Receiver2D(Receiver):
    """
    Class for receiving and processing two-dimensional signals.

    Attributes:
        image (numpy.ndarray): The two-dimensional signal data.
        dft2 (numpy.ndarray): Result of the two-dimensional Fourier transform.
        idft2 (numpy.ndarray): Result of the inverse two-dimensional Fourier transform.
        dct2 (numpy.ndarray): Result of the two-dimensional discrete cosine transform.
        idct2 (numpy.ndarray): Result of the inverse two-dimensional discrete cosine transform.
        filtered_dft2 (numpy.ndarray): Filtered result of the two-dimensional Fourier transform.
        filtered_idft2 (numpy.ndarray): Filtered result of the inverse two-dimensional Fourier transform.
        filtered_dct2 (numpy.ndarray): Filtered result of the two-dimensional discrete cosine transform.
        filtered_idct2 (numpy.ndarray): Filtered result of the inverse two-dimensional discrete cosine transform.

    Methods:
        choose_jpg_file(controller): Opens a file dialog to choose a JPG file.
        set_image(controller, signals_handler): Sets the image data using a JPG file.
        calculate_image(controller): Calculates the image data based on provided parameters.
        perform_2d_dft(): Performs the two-dimensional Fourier transform.
        perform_2d_idft(): Performs the inverse two-dimensional Fourier transform.
        plot_image(canvas): Plots the original image.
        plot_2d_dft(canvas): Plots the two-dimensional Fourier transform.
        plot_2d_idft(canvas): Plots the inverse two-dimensional Fourier transform.
        filter_2d_dft(controller): Filters the two-dimensional Fourier transform.
        plot_filtered_2d_dft(canvas): Plots the filtered two-dimensional Fourier transform.
        filter_2d_idft(): Filters the inverse two-dimensional Fourier transform.
        plot_filtered_2d_idft(canvas): Plots the filtered inverse two-dimensional Fourier transform.
        perform_2d_dct(): Performs the two-dimensional discrete cosine transform.
        perform_2d_idct(): Performs the inverse two-dimensional discrete cosine transform.
        plot_2d_dct(canvas): Plots the two-dimensional discrete cosine transform.
        plot_2d_idct(canvas): Plots the inverse two-dimensional discrete cosine transform.
        filter_2d_dct(controller): Filters the two-dimensional discrete cosine transform.
        plot_filtered_2d_dct(canvas): Plots the filtered two-dimensional discrete cosine transform.
        filter_2d_idct(): Filters the inverse two-dimensional discrete cosine transform.
        plot_filtered_2d_idct(canvas): Plots the filtered inverse two-dimensional discrete cosine transform.
    """

    def __init__(self):
        """
        Initializes a Receiver2D instance.
        """
        super().__init__()
        self.image = None
        self.dft2 = None
        self.idft2 = None
        self.dct2 = None
        self.idct2 = None
        self.filtered_dft2 = None
        self.filtered_idft2 = None
        self.filtered_dct2 = None
        self.filtered_idct2 = None

    @staticmethod
    def choose_jpg_file(controller):
        """
        Opens a file dialog to choose a JPG file.

        Parameters:
            controller: The controller object.
        """
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, 'Choose Image File', filter='JPG files (*.jpg);')
        controller.image_file_name.setPlainText(str(file_path))

    def set_image(self, controller, signals_handler):
        """
        Sets the image data using a JPG file.

        Parameters:
            controller: The controller object.
            signals_handler: The signals handler object.
        """
        if controller.jpg_file_check_box_state():
            filename = controller.get_jpg_file()
            if filename:
                self.image = signals_handler.generate_from_file(filename)

    def calculate_image(self, controller):
        """
        Calculates the image data based on provided parameters.

        Parameters:
            controller: The controller object.
        """
        frequency_x = controller.get_frequency_x()
        frequency_y = controller.get_frequency_y()
        angle = controller.get_angle()

        signal = Sine2D(frequency_x, frequency_y, angle).get_wave(size=64)
        self.image = signal

    def perform_2d_dft(self):
        """Performs the two-dimensional Fourier transform."""
        if self.image is not None:
            self.dft2 = FFT2DAnalyzer(self.image).calculate()

    def perform_2d_idft(self):
        """Performs the inverse two-dimensional Fourier transform."""
        if self.dft2 is not None:
            self.idft2 = IFFT2DAnalyzer(self.dft2).calculate()

    def plot_image(self, canvas):
        """Plots the original image."""
        if self.image is not None:
            image_plot = ImagePlot(None, self.image, None, None, 'Original Image')

            canvas.clear()
            image_plot.create_on_canvas(canvas)

    def plot_2d_dft(self, canvas):
        """Plots the two-dimensional Fourier transform."""
        if self.dft2 is not None:
            dft_plot = ImagePlot(None, np.log(abs(self.dft2) + 1e-10), None, None, '2D DFT')

            canvas.clear()
            dft_plot.create_on_canvas(canvas)

    def plot_2d_idft(self, canvas):
        """Plots the inverse two-dimensional Fourier transform."""
        if self.idft2 is not None:
            idft_plot = ImagePlot(None, self.idft2.real, None, None, 'IDFT')

            canvas.clear()
            idft_plot.create_on_canvas(canvas)

    def filter_2d_dft(self, controller):
        """Filters the two-dimensional Fourier transform."""
        filter_type = controller.filters_list.currentIndex()
        mask = np.zeros_like(self.dft2)

        if filter_type == 1:  # Low-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                mask[row_index:, :] = 1
                mask[:, column_index:] = 1

        elif filter_type == 2:  # High-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                mask[:row_index, :] = 1
                mask[:, :column_index] = 1

        else:
            controller.print_error('Select a filter')
            return

        self.filtered_dft2 = self.dft2 * mask

    def plot_filtered_2d_dft(self, canvas):
        """Plots the filtered two-dimensional Fourier transform."""
        if self.filtered_dft2 is not None:
            dft_plot = ImagePlot(None, np.log(abs(self.filtered_dft2) + 1e-10), None, None, '2D DFT')

            canvas.clear()
            dft_plot.create_on_canvas(canvas)

    def filter_2d_idft(self):
        """Filters the inverse two-dimensional Fourier transform."""
        if self.filtered_dft2 is not None:
            self.filtered_idft2 = IFFT2DAnalyzer(self.filtered_dft2).calculate()

    def plot_filtered_2d_idft(self, canvas):
        """Plots the filtered inverse two-dimensional Fourier transform."""
        if self.filtered_idft2 is not None:
            idft_plot = ImagePlot(None, np.abs(self.filtered_idft2), None, None, 'IDFT')

            canvas.clear()
            idft_plot.create_on_canvas(canvas)

    def perform_2d_dct(self):
        """Performs the two-dimensional discrete cosine transform."""
        if self.image is not None:
            self.dct2 = DCT2DAnalyzer(self.image).calculate()

    def perform_2d_idct(self):
        """Performs the inverse two-dimensional discrete cosine transform."""
        if self.dct2 is not None:
            self.idct2 = IDCT2DAnalyzer(self.dct2).calculate()

    def plot_2d_dct(self, canvas):
        """Plots the two-dimensional discrete cosine transform."""
        if self.dct2 is not None:
            dct_plot = ImagePlot(None, np.log(abs(self.dct2) + 1e-10), None, None, '2D DCT')

            canvas.clear()
            dct_plot.create_on_canvas(canvas)

    def plot_2d_idct(self, canvas):
        """Plots the inverse two-dimensional discrete cosine transform."""
        if self.idct2 is not None:
            idct_plot = ImagePlot(None, np.abs(self.idct2), None, None, 'IDCT')

            canvas.clear()
            idct_plot.create_on_canvas(canvas)

    def filter_2d_dct(self, controller):
        """Filters the two-dimensional discrete cosine transform."""
        filter_type = controller.filters_list.currentIndex()
        mask = np.zeros_like(self.dct2)

        if filter_type == 1:  # Low-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                mask[row_index:, :] = 1
                mask[:, column_index:] = 1

        elif filter_type == 2:  # High-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                mask[:row_index, :] = 1
                mask[:, :column_index] = 1

        else:
            controller.print_error('Select a filter')
            return

        self.filtered_dct2 = self.dct2 * mask

    def plot_filtered_2d_dct(self, canvas):
        """Plots the filtered two-dimensional discrete cosine transform."""
        if self.filtered_dct2 is not None:
            dct_plot = ImagePlot(None, np.log(abs(self.filtered_dct2) + 1e-10), None, None, '2D DCT')

            canvas.clear()
            dct_plot.create_on_canvas(canvas)

    def filter_2d_idct(self):
        """Filters the inverse two-dimensional discrete cosine transform."""
        if self.filtered_dct2 is not None:
            self.filtered_idct2 = IDCT2DAnalyzer(self.filtered_dct2).calculate()

    def plot_filtered_2d_idct(self, canvas):
        """Plots the filtered inverse two-dimensional discrete cosine transform."""
        if self.filtered_idct2 is not None:
            idct_plot = ImagePlot(None, np.abs(self.filtered_idct2), None, None, 'IDCT')

            canvas.clear()
            idct_plot.create_on_canvas(canvas)
