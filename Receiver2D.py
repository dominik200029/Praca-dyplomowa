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

        self.filtered_plot_dft = False
        self.filtered_plot_dct = False

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
        filename = controller.get_jpg_file()
        if filename:
            self.image = signals_handler.generate_from_file(filename) + 0.5  # add DC component

    def calculate_image(self, controller):
        """
        Calculates the image data based on provided parameters.

        Parameters:
            controller: The controller object.
        """
        spatial_frequency = controller.get_spatial_frequency()
        angle = controller.get_angle()

        signal = Sine2D(spatial_frequency, angle).get_wave(size=64)
        self.image = signal + 0.5  # add DC component

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
            image_plot = ImagePlot(self.image, 'Obraz oryginalny')
            canvas.clear()
            image_plot.create_on_canvas(canvas)

    def plot_2d_dft(self, canvas, controller):
        """Plots the two-dimensional Fourier transform."""
        log_button_state = controller.get_log_radio_button_state()
        log_constant = 1e-10  # constant to add in case of logarithmic 0
        if self.dft2 is not None:
            if log_button_state:
                dft_plot = ImagePlot(np.log(abs(self.dft2) + log_constant),  'Moduł 2D DFT')
            else:
                dft_plot = ImagePlot(abs(self.dft2), 'Moduł 2D DFT')
            canvas.clear()
            dft_plot.create_on_canvas(canvas)
            self.filtered_plot_dft = False

    def plot_2d_idft(self, canvas):
        """Plots the inverse two-dimensional Fourier transform."""
        if self.idft2 is not None:
            idft_plot = ImagePlot(self.idft2.real, 'IDFT')
            canvas.clear()
            idft_plot.create_on_canvas(canvas)

    def filter_2d_dft(self, controller):
        """Filters the two-dimensional Fourier transform."""
        filter_type = controller.filters_list.currentIndex()
        mask = np.zeros_like(self.dft2)

        if filter_type == 1:  # Gaussian Low-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                x, y = np.meshgrid(np.arange(mask.shape[0]), np.arange(mask.shape[1]))
                center_x, center_y = row_index, column_index
                sigma = controller.get_cut_off_spatial()
                x_cord = x - center_x
                y_cord = y - center_y
                mask = (np.exp(-(x_cord ** 2 + y_cord ** 2) / (2 * sigma ** 2))) / (2 * np.pi * sigma ** 2)

        elif filter_type == 2:  # Gaussian High-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                x, y = np.meshgrid(np.arange(mask.shape[0]), np.arange(mask.shape[1]))
                center_x, center_y = row_index, column_index
                sigma = controller.get_cut_off_spatial()
                x_cord = x - center_x
                y_cord = y - center_y
                mask = (1 - np.exp(-(x_cord ** 2 + y_cord ** 2) / (2 * sigma ** 2))) / (2 * np.pi * sigma ** 2)
        else:
            controller.print_error('Wybierz filtr')
            return

        self.filtered_dft2 = self.dft2 * mask

    def plot_filtered_2d_dft(self, canvas, controller):
        """Plots the filtered two-dimensional Fourier transform."""
        log_button_state = controller.get_log_radio_button_state()
        log_constant = 1e-10  # constant to add in case of logarithmic 0
        if self.filtered_dft2 is not None:
            if log_button_state:
                dft_plot = ImagePlot(np.log(abs(self.filtered_dft2) + log_constant), 'Moduł 2D DFT')
            else:
                dft_plot = ImagePlot(abs(self.filtered_dft2), 'Moduł 2D DFT')
            canvas.clear()
            dft_plot.create_on_canvas(canvas)
            self.filtered_plot_dft = True

    def filter_2d_idft(self):
        """Filters the inverse two-dimensional Fourier transform."""
        if self.filtered_dft2 is not None:
            self.filtered_idft2 = IFFT2DAnalyzer(self.filtered_dft2).calculate()

    def plot_filtered_2d_idft(self, canvas):
        """Plots the filtered inverse two-dimensional Fourier transform."""
        if self.filtered_idft2 is not None:
            idft_plot = ImagePlot(np.abs(self.filtered_idft2),  'IDFT')

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

    def plot_2d_dct(self, canvas, controller):
        """Plots the two-dimensional discrete cosine transform."""
        log_button_state = controller.get_log_radio_button_state()
        log_constant = 1e-10  # constant to add in case of logarithmic 0
        if self.dct2 is not None:
            if log_button_state:
                dct_plot = ImagePlot(np.log(abs(self.dct2) + log_constant), 'Moduł 2D DCT')
            else:
                dct_plot = ImagePlot(abs(self.dct2), 'Moduł 2D DCT')
            canvas.clear()
            dct_plot.create_on_canvas(canvas)
            self.filtered_plot_dct = False

    def plot_2d_idct(self, canvas):
        """Plots the inverse two-dimensional discrete cosine transform."""
        if self.idct2 is not None:
            idct_plot = ImagePlot(np.abs(self.idct2), 'IDCT')
            canvas.clear()
            idct_plot.create_on_canvas(canvas)

    def filter_2d_dct(self, controller):
        """Filters the two-dimensional discrete cosine transform."""
        filter_type = controller.filters_list.currentIndex()
        mask = np.zeros_like(self.dct2)

        if filter_type == 2:  # High-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                mask[row_index:, :] = 1
                mask[:, column_index:] = 1

        elif filter_type == 1:  # Low-pass filter
            row_index = controller.get_column()
            column_index = controller.get_row()
            if row_index is not None and column_index is not None:
                mask[:row_index, :] = 1
                mask[:, :column_index] = 1

        else:
            controller.print_error('Wybierz filtr')
            return

        self.filtered_dct2 = self.dct2 * mask

    def plot_filtered_2d_dct(self, canvas, controller):
        """Plots the filtered two-dimensional discrete cosine transform."""
        log_button_state = controller.get_log_radio_button_state()
        log_constant = 1e-10  # constant to add in case of logarithmic 0
        if self.filtered_dct2 is not None:
            if log_button_state:
                dct_plot = ImagePlot(np.log(abs(self.filtered_dct2) + log_constant), 'Moduł 2D DCT')
            else:
                dct_plot = ImagePlot(abs(self.filtered_dct2), 'Moduł 2D DCT')
            canvas.clear()
            dct_plot.create_on_canvas(canvas)
            self.filtered_plot_dct = True

    def filter_2d_idct(self):
        """Filters the inverse two-dimensional discrete cosine transform."""
        if self.filtered_dct2 is not None:
            self.filtered_idct2 = IDCT2DAnalyzer(self.filtered_dct2).calculate()

    def plot_filtered_2d_idct(self, canvas):
        """Plots the filtered inverse two-dimensional discrete cosine transform."""
        if self.filtered_idct2 is not None:
            idct_plot = ImagePlot(np.abs(self.filtered_idct2), 'IDCT')
            canvas.clear()
            idct_plot.create_on_canvas(canvas)
