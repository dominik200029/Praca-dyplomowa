from scipy.fft import fft, ifft, dct, idct, fft2, ifft2, dctn, idctn, fftshift, ifftshift
from abc import ABC, abstractmethod


class TransformAnalyzer(ABC):
    """
    Abstract base class for analyzing transforms.

    Attributes:
        function (array-like): The input data for the transformation.

    Methods:
        calculate(): Abstract method to perform the transformation and return the result.
    """

    def __init__(self, function):
        """
        Initializes a TransformAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the transformation.
        """
        self.function = function

    @abstractmethod
    def calculate(self):
        """
        Abstract method to perform the transformation and return the result.
        """
        pass


class FFTAnalyzer(TransformAnalyzer):
    """
    Performs Fast Fourier Transform (FFT) analysis.

    Attributes:
        function (array-like): The input data for the FFT.

    Methods:
        calculate(): Perform FFT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes an FFTAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the FFT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform FFT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the FFT.
        """
        return fft(self.function)


class DCTAnalyzer(TransformAnalyzer):
    """
    Performs Discrete Cosine Transform (DCT) analysis.

    Attributes:
        function (array-like): The input data for the DCT.

    Methods:
        calculate(): Perform DCT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes a DCTAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the DCT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform DCT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the DCT.
        """
        return dct(self.function, norm='ortho')


class IFFTAnalyzer(TransformAnalyzer):
    """
    Performs Inverse Fast Fourier Transform (IFFT) analysis.

    Attributes:
        function (array-like): The input data for the IFFT.

    Methods:
        calculate(): Perform IFFT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes an IFFTAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the IFFT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform IFFT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the IFFT.
        """
        return ifft(self.function)


class IDCTAnalyzer(TransformAnalyzer):
    """
    Performs Inverse Discrete Cosine Transform (IDCT) analysis.

    Attributes:
        function (array-like): The input data for the IDCT.

    Methods:
        calculate(): Perform IDCT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes an IDCTAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the IDCT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform IDCT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the IDCT.
        """
        return idct(self.function, norm='ortho')


class FFT2DAnalyzer(TransformAnalyzer):
    """
    Performs 2D Fast Fourier Transform (FFT) analysis.

    Attributes:
        function (array-like): The input data for the 2D FFT.

    Methods:
        calculate(): Perform 2D FFT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes a FFT2DAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the 2D FFT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform 2D FFT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the 2D FFT.
        """
        return fftshift(fft2(self.function))


class IFFT2DAnalyzer(TransformAnalyzer):
    """
    Performs 2D Inverse Fast Fourier Transform (IFFT) analysis.

    Attributes:
        function (array-like): The input data for the 2D IFFT.

    Methods:
        calculate(): Perform 2D IFFT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes an IFFT2DAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the 2D IFFT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform 2D IFFT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the 2D IFFT.
        """
        return ifft2(ifftshift(self.function))


class DCT2DAnalyzer(TransformAnalyzer):
    """
    Performs 2D Discrete Cosine Transform (DCT) analysis.

    Attributes:
        function (array-like): The input data for the 2D DCT.

    Methods:
        calculate(): Perform 2D DCT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes a DCT2DAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the 2D DCT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform 2D DCT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the 2D DCT.
        """
        return dctn(self.function, norm='ortho')


class IDCT2DAnalyzer(TransformAnalyzer):
    """
    Performs 2D Inverse Discrete Cosine Transform (IDCT) analysis.

    Attributes:
        function (array-like): The input data for the 2D IDCT.

    Methods:
        calculate(): Perform 2D IDCT on the input data and return the result.
    """

    def __init__(self, function):
        """
        Initializes an IDCT2DAnalyzer instance with the specified input data.

        Parameters:
            function (array-like): The input data for the 2D IDCT.
        """
        super().__init__(function)

    def calculate(self):
        """
        Perform 2D IDCT on the input data and return the result.

        Returns:
            numpy.ndarray: The result of the 2D IDCT.
        """
        return idctn(self.function, norm='ortho')
