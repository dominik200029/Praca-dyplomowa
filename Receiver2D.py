from PyQt5.QtWidgets import QFileDialog

from Graph import ImagePlot


class Receiver2D:
    def __init__(self):
        self.image = None

    def update_plots_from_jpg_file(self, controller, signals_handler, *canvases):
        if controller.jpg_file_check_box_state():
            filename = controller.get_jpg_file()
            if filename:
                self.image = signals_handler.generate_from_file(filename)

                image_plot = ImagePlot(None, self.image, None, None, 'Obraz oryginalny')

                for canvas in canvases:
                    canvas.clear()

                image_plot.create_on_canvas(canvases[0])

    @staticmethod
    def choose_jpg_file(controller):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, 'Choose Image File', filter='JPG files (*.jpg);')
        controller.image_file_name.setPlainText(str(file_path))
