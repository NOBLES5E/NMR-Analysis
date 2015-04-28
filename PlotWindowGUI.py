import sys

from PyQt5 import QtWidgets
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib import style
style.use('ggplot')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
import matplotlib.pyplot as plt
import nmrglue as ng
from io import StringIO


class PlotWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, figure=None):
        super().__init__(parent)
        # a figure instance to plot on
        self.setWindowTitle('Plot Window')
        if not figure:
            self.figure = plt.figure()
        else:
            self.figure = figure
        self.time_subplot = self.figure.add_subplot(221)
        self.freq_subplot = self.figure.add_subplot(222)
        self.glue_subplot = self.figure.add_subplot(223)
        self.int_subplot = self.figure.add_subplot(224)

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Get data button
        self.get_time_button = QtWidgets.QPushButton('Get Time Data', self)
        self.get_freq_button = QtWidgets.QPushButton('Get Freq Data', self)
        self.get_glue_button = QtWidgets.QPushButton('Get Glue Data', self)
        self.get_int_button = QtWidgets.QPushButton('Get Int Data', self)

        self.get_time_button.clicked.connect(self.show_time_data)
        self.get_freq_button.clicked.connect(self.show_freq_data)
        self.get_glue_button.clicked.connect(self.show_glue_data)
        self.get_int_button.clicked.connect(self.show_int_data)

        # set the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        hlayout = QtWidgets.QHBoxLayout(self)
        hlayout.addWidget(self.get_time_button)
        hlayout.addWidget(self.get_freq_button)
        hlayout.addWidget(self.get_glue_button)
        hlayout.addWidget(self.get_int_button)
        layout.addLayout(hlayout)
        self.setLayout(layout)

        # data
        self.time_data = None
        self.freq_data = None
        self.glue_data = None
        self.int_data = None



    def plot_time(self, dic, data, title='Time', x_label='Time'):
        # discards the old graph
        self.time_subplot.hold(False)

        uc = ng.pipe.make_uc(dic, data)
        [re, im, ab] = self.time_subplot.plot(uc.us_scale(), data.real, 'r-', uc.us_scale(), data.imag, 'g-',
                                              uc.us_scale(), np.absolute(data), 'm--')
        re.set_label('Real Part')
        im.set_label('Imag Part')
        ab.set_label('Absolute')
        self.time_subplot.legend()

        self.time_subplot.set_title(title)
        self.time_subplot.set_xlabel(x_label + ' / ' + 'us')

        # refresh canvas
        self.canvas.draw()

        # refresh data
        self.time_data = [uc.us_scale(), data.real, data.imag, np.absolute(data)]

    def show_time_data(self):
        self.show_data_dialog('time')
    def show_freq_data(self):
        self.show_data_dialog('freq')
    def show_glue_data(self):
        self.show_data_dialog('glue')
    def show_int_data(self):
        self.show_data_dialog('int')


    def show_data_dialog(self, data_type):
        message_widget = QtWidgets.QDialog(self)
        if data_type == 'time':
            message = self.format_data(header = 'Time/us\tRealPart\tImagPart\tAbs', data_list=self.time_data)
        if data_type == 'freq':
            message = self.format_data(header = 'Freq/hz\tRealPart\tImagPart\tAbs', data_list=self.freq_data)
        if data_type == 'glue':
            message = self.format_data(header = 'Freq/hz\tRealPart\tImagPart\tAbs', data_list=self.glue_data)
        if data_type == 'int':
            message = self.format_data(header = 'X0\tRealPart\tImagPart\tAbs\tX1\tRealPart\tImagPart\tAbs\tX2\tRealPart\tImagPart\tAbs\tX3\tRealPart\tImagPart\tAbs\t', data_list=self.int_data)

        message_box = QtWidgets.QTextEdit(message_widget)
        message_box.setText(message)
        layout = QtWidgets.QVBoxLayout(message_widget)
        layout.addWidget(message_box)
        message_widget.setLayout(layout)
        message_widget.setWindowTitle('Data')
        message_widget.show()

    def format_data(self, header, data_list):
        zipped_list = list(zip(*[data for data in data_list if any(data)]))
        out_text = StringIO()
        out_text.write(header+'\n')
        for item in zipped_list:
            out_text.write('\t'.join((str(item_item) for item_item in item))+'\n')
        return out_text.getvalue()

    def plot_freq(self, dic, data, title='Spectrum', x_label='Frequency Deviation'):
        # discards the old graph
        self.freq_subplot.hold(False)

        uc = ng.pipe.make_uc(dic, data)
        (re, im, ab) = self.freq_subplot.plot(uc.hz_scale(), data.real, 'r-', uc.hz_scale(), data.imag, 'g-',
                                              uc.hz_scale(), np.core.umath.absolute(data), 'm--')
        re.set_label('Real Part')
        im.set_label('Imag Part')
        ab.set_label('Absolute')
        self.freq_subplot.legend()

        self.freq_subplot.set_title(title)
        self.freq_subplot.set_xlabel(x_label + ' / ' + 'hz')

        # refresh canvas
        self.canvas.draw()

        # refresh data
        self.freq_data = [uc.hz_scale(), data.real, data.imag, np.absolute(data)]



    def plot_glue(self, x, y, y_list, title='Glue', x_label='Frequency', show = 'sum'):
        # discards the old graph
        self.glue_subplot.hold(False)

        if show == 'sum':
            (re, im, ab) = self.glue_subplot.plot(x, y.real, 'r-', x, y.imag, 'g-', x, np.core.umath.absolute(y), 'm--')
            re.set_label('Real Part')
            im.set_label('Imag Part')
            ab.set_label('Absolute')
            # refresh data
            self.glue_data = [x, y.real, y.imag, np.absolute(y)]
        else:
            self.glue_subplot.plot(x, y_list)

        self.glue_subplot.legend()
        self.glue_subplot.set_xlabel(x_label + ' / ' + 'hz')
        self.glue_subplot.set_title(title)
        # refresh canvas
        self.canvas.draw()



    def plot_int(self, int_plot_dic, title='Integral', x_label='No X Label'):
        # discards the old graph
        self.int_subplot.hold(False)

        (int_0_re, int_0_im, int_0_ab,
        int_1_re, int_1_im, int_1_ab,
        int_2_re, int_2_im, int_2_ab,
        int_3_re, int_3_im, int_3_ab,) = self.int_subplot.plot(int_plot_dic[0][0], np.asarray(int_plot_dic[0][1]).real, 'r--',
                                                               int_plot_dic[0][0], np.asarray(int_plot_dic[0][1]).imag, 'r-.',
                                                               int_plot_dic[0][0], np.core.umath.absolute(int_plot_dic[0][1]), 'r-',

                                                               int_plot_dic[1][0], np.asarray(int_plot_dic[1][1]).real, 'k--',
                                                               int_plot_dic[1][0], np.asarray(int_plot_dic[1][1]).imag, 'k-.',
                                                               int_plot_dic[1][0], np.core.umath.absolute(int_plot_dic[1][1]), 'k-',

                                                               int_plot_dic[2][0], np.asarray(int_plot_dic[2][1]).real, 'g--',
                                                               int_plot_dic[2][0], np.asarray(int_plot_dic[2][1]).imag, 'g-.',
                                                               int_plot_dic[2][0], np.core.umath.absolute(int_plot_dic[2][1]), 'g-',

                                                               int_plot_dic[3][0], np.asarray(int_plot_dic[3][1]).real, 'm--',
                                                               int_plot_dic[3][0], np.asarray(int_plot_dic[3][1]).imag, 'm-.',
                                                               int_plot_dic[3][0], np.core.umath.absolute(int_plot_dic[3][1]), 'm-')
        int_0_re.set_label('Integral 0 Re')
        int_0_im.set_label('Integral 0 Im')
        int_0_ab.set_label('Integral 0 ABS')

        int_1_re.set_label('Integral 1 Re')
        int_1_im.set_label('Integral 1 Im')
        int_1_ab.set_label('Integral 1 ABS')

        int_2_re.set_label('Integral 2 Re')
        int_2_im.set_label('Integral 2 Im')
        int_2_ab.set_label('Integral 2 ABS')

        int_3_re.set_label('Integral 3 Re')
        int_3_im.set_label('Integral 3 Im')
        int_3_ab.set_label('Integral 3 ABS')

        self.int_subplot.legend()

        self.int_subplot.set_title(title)
        self.int_subplot.set_xlabel(x_label)

        # refresh canvas
        self.canvas.draw()

        # refresh data
        self.int_data = [int_plot_dic[0][0], np.asarray(int_plot_dic[0][1]).real, np.asarray(int_plot_dic[0][1]).imag, np.core.umath.absolute(int_plot_dic[0][1]),

                                                               int_plot_dic[1][0], np.asarray(int_plot_dic[1][1]).real,  np.asarray(int_plot_dic[1][1]).imag, np.core.umath.absolute(int_plot_dic[1][1]),

                                                               int_plot_dic[2][0], np.asarray(int_plot_dic[2][1]).real,  np.asarray(int_plot_dic[2][1]).imag, np.core.umath.absolute(int_plot_dic[2][1]),

                                                               int_plot_dic[3][0], np.asarray(int_plot_dic[3][1]).real,  np.asarray(int_plot_dic[3][1]).imag, np.core.umath.absolute(int_plot_dic[3][1])]

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main = PlotWindow()
    main.show()

    sys.exit(app.exec_())