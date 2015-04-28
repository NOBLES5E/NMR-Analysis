# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import nmr_analysis
import PlotWindowGUI
import pickle

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        ######## Set Up Reader ##############
        self.reader = nmr_analysis.Reader()
        self.plot_window = PlotWindowGUI.PlotWindow(parent=self)
        self.plot_window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 700)
        MainWindow.setMinimumSize(QtCore.QSize(300, 700))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.data_row_selection_label = QtWidgets.QLabel(self.centralWidget)
        self.data_row_selection_label.setObjectName("data_row_selection_label")
        self.verticalLayout_2.addWidget(self.data_row_selection_label)
        self.data_row_selection_table = QtWidgets.QTableWidget(self.centralWidget)
        self.data_row_selection_table.setObjectName("data_row_selection_table")
        self.data_row_selection_table.setColumnCount(0)
        self.data_row_selection_table.setRowCount(0)
        self.verticalLayout_2.addWidget(self.data_row_selection_table)
        self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.basic_process_tab = QtWidgets.QWidget()
        self.basic_process_tab.setObjectName("basic_process_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.basic_process_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.basic_process_para_table = QtWidgets.QTableWidget(self.basic_process_tab)
        self.basic_process_para_table.setObjectName("basic_process_para_table")
        self.basic_process_para_table.setColumnCount(0)
        self.basic_process_para_table.setRowCount(0)
        self.verticalLayout_3.addWidget(self.basic_process_para_table)
        self.tabWidget.addTab(self.basic_process_tab, "")
        self.advanced_process_tab = QtWidgets.QWidget()
        self.advanced_process_tab.setObjectName("advanced_process_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.advanced_process_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.advanced_process_para_table = QtWidgets.QTableWidget(self.advanced_process_tab)
        self.advanced_process_para_table.setObjectName("advanced_process_para_table")
        self.advanced_process_para_table.setColumnCount(0)
        self.advanced_process_para_table.setRowCount(0)
        self.verticalLayout_4.addWidget(self.advanced_process_para_table)
        self.tabWidget.addTab(self.advanced_process_tab, "")
        self.plot_tab = QtWidgets.QWidget()
        self.plot_tab.setObjectName("plot_tab")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.plot_tab)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.plot_selection_label = QtWidgets.QLabel(self.plot_tab)
        self.plot_selection_label.setObjectName("plot_selection_label")
        self.verticalLayout_5.addWidget(self.plot_selection_label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.time_checkbox = QtWidgets.QCheckBox(self.plot_tab)
        self.time_checkbox.setObjectName("time_checkbox")
        self.horizontalLayout.addWidget(self.time_checkbox)
        self.freq_checkbox = QtWidgets.QCheckBox(self.plot_tab)
        self.freq_checkbox.setObjectName("freq_checkbox")
        self.horizontalLayout.addWidget(self.freq_checkbox)
        self.glue_checkbox = QtWidgets.QCheckBox(self.plot_tab)
        self.glue_checkbox.setObjectName("glue_checkbox")
        self.horizontalLayout.addWidget(self.glue_checkbox)
        self.int_checkbox = QtWidgets.QCheckBox(self.plot_tab)
        self.int_checkbox.setObjectName("int_checkbox")
        self.horizontalLayout.addWidget(self.int_checkbox)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.glue_int_para_label = QtWidgets.QLabel(self.plot_tab)
        self.glue_int_para_label.setObjectName("glue_int_para_label")
        self.verticalLayout_5.addWidget(self.glue_int_para_label)
        self.glue_int_para_table = QtWidgets.QTableWidget(self.plot_tab)
        self.glue_int_para_table.setObjectName("glue_int_para_table")
        self.glue_int_para_table.setColumnCount(0)
        self.glue_int_para_table.setRowCount(0)
        self.verticalLayout_5.addWidget(self.glue_int_para_table)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.tabWidget.addTab(self.plot_tab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.apply_to_all_checkbox = QtWidgets.QCheckBox(self.centralWidget)
        self.apply_to_all_checkbox.setObjectName("apply_to_all_checkbox")
        self.verticalLayout_2.addWidget(self.apply_to_all_checkbox)
        self.note_label = QtWidgets.QLabel(self.centralWidget)
        self.note_label.setObjectName("note_label")
        self.verticalLayout_2.addWidget(self.note_label)
        self.note_textedit = QtWidgets.QTextEdit(self.centralWidget)
        self.note_textedit.setObjectName("note_textedit")
        self.verticalLayout_2.addWidget(self.note_textedit)
        self.save_note_btn = QtWidgets.QPushButton(self.centralWidget)
        self.save_note_btn.setObjectName("save_note_btn")
        self.verticalLayout_2.addWidget(self.save_note_btn)
        self.refresh_all_plot_btn = QtWidgets.QPushButton(self.centralWidget)
        self.refresh_all_plot_btn.setObjectName("refresh_all_plot_btn")
        self.verticalLayout_2.addWidget(self.refresh_all_plot_btn)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 400, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuNMR_Analysis_v1_00_by_iceorange = QtWidgets.QMenu(self.menuBar)
        self.menuNMR_Analysis_v1_00_by_iceorange.setObjectName("menuNMR_Analysis_v1_00_by_iceorange")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.menuWindow = QtWidgets.QMenu(self.menuBar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        MainWindow.insertToolBarBreak(self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionAdd_Data = QtWidgets.QAction(MainWindow)
        self.actionAdd_Data.setObjectName("actionAdd_Data")
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionFit = QtWidgets.QAction(MainWindow)
        self.actionFit.setObjectName("actionFit")
        self.actionOperation_Queue_Observer = QtWidgets.QAction(MainWindow)
        self.actionOperation_Queue_Observer.setObjectName("actionOperation_Queue_Observer")
        self.actionIndex = QtWidgets.QAction(MainWindow)
        self.actionIndex.setObjectName("actionIndex")
        self.actionReport_Bug = QtWidgets.QAction(MainWindow)
        self.actionReport_Bug.setObjectName("actionReport_Bug")
        self.actionOpen_Lab_s_Website = QtWidgets.QAction(MainWindow)
        self.actionOpen_Lab_s_Website.setObjectName("actionOpen_Lab_s_Website")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuNMR_Analysis_v1_00_by_iceorange.addSeparator()
        self.menuNMR_Analysis_v1_00_by_iceorange.addAction(self.actionOpen)
        self.menuNMR_Analysis_v1_00_by_iceorange.addAction(self.actionAdd_Data)
        self.menuNMR_Analysis_v1_00_by_iceorange.addSeparator()
        self.menuNMR_Analysis_v1_00_by_iceorange.addAction(self.actionSave_As)
        self.menuNMR_Analysis_v1_00_by_iceorange.addSeparator()
        self.menuNMR_Analysis_v1_00_by_iceorange.addAction(self.actionExit)
        self.menuTools.addAction(self.actionFit)
        self.menuWindow.addAction(self.actionOperation_Queue_Observer)
        self.menuHelp.addAction(self.actionIndex)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionReport_Bug)
        self.menuHelp.addAction(self.actionOpen_Lab_s_Website)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuNMR_Analysis_v1_00_by_iceorange.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuWindow.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NMR Analysis v1.00 by iceorange"))
        self.data_row_selection_label.setText(_translate("MainWindow", "Data Row Selection"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.basic_process_tab), _translate("MainWindow", "Basic Process"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.advanced_process_tab), _translate("MainWindow", "Advanced Process"))
        self.plot_selection_label.setText(_translate("MainWindow", "Plot Selection"))
        self.time_checkbox.setText(_translate("MainWindow", "Time"))
        self.freq_checkbox.setText(_translate("MainWindow", "Freq"))
        self.glue_checkbox.setText(_translate("MainWindow", "Glue"))
        self.int_checkbox.setText(_translate("MainWindow", "Int"))
        self.glue_int_para_label.setText(_translate("MainWindow", "Glue & Int Parameters"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plot_tab), _translate("MainWindow", "Plot"))
        self.apply_to_all_checkbox.setText(_translate("MainWindow", "Apply to All"))
        self.note_label.setText(_translate("MainWindow", "Note"))
        self.save_note_btn.setText(_translate("MainWindow", "Save Note"))
        self.refresh_all_plot_btn.setText(_translate("MainWindow", "Refresh All Plots"))
        self.menuNMR_Analysis_v1_00_by_iceorange.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionAdd_Data.setText(_translate("MainWindow", "Add Data"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionFit.setText(_translate("MainWindow", "Fit"))
        self.actionOperation_Queue_Observer.setText(_translate("MainWindow", "Operation Queue Observer"))
        self.actionIndex.setText(_translate("MainWindow", "Index"))
        self.actionReport_Bug.setText(_translate("MainWindow", "Report Bug"))
        self.actionOpen_Lab_s_Website.setText(_translate("MainWindow", "Open Lab\'s Website"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.time_checkbox.setChecked(True)
        self.freq_checkbox.setChecked(True)

        #################################### Menu #######################################
        # File
        self.actionOpen.triggered.connect(self.open_file_dialog)
        self.actionAdd_Data.triggered.connect(self.add_data_dialog)
        self.actionSave_As.triggered.connect(self.save_data_dialog)
        self.actionExit.triggered.connect(QtWidgets.qApp.quit)
        # Tools
        self.actionFit.triggered.connect(self.show_fit_dialog)
        # Window
        self.actionOperation_Queue_Observer.triggered.connect(self.show_operation_queue_dialog)
        # Help
        self.actionIndex.triggered.connect(self.show_help_index_widget)
        self.actionReport_Bug.triggered.connect(self.show_report_bug_dialog)
        self.actionOpen_Lab_s_Website.triggered.connect(self.open_website)
        self.actionAbout.triggered.connect(self.show_about_message)

        ############################### Data Row Selection #############################

        self.data_row_selection_table.currentCellChanged.connect(self.data_row_selection_selection_change)

        ############################## Basic Process ###################################



        ############################### Advanced Process ###############################



        ############################## Plot ##########################################



        ############################### Note #########################################
        self.save_note_btn.clicked.connect(self.save_note)

        ############################### OTHERS ##################################
        self.set_data_change_handler()
        self.refresh_all_plot_btn.clicked.connect(self.refresh_all_plot)
    # Additional Functions

    ############################### Menu ###########################################
    # File Menu
    def open_file_dialog(self):
        self.ban_data_change_hander()
        fname, ftype = QtWidgets.QFileDialog.getOpenFileName(self, 'Open .ice file')
        if fname:
            try:
                if (fname.endswith('.ice')):
                    with open(fname, 'rb') as file:
                        self.reader = pickle.load(file)
                else:
                    raise nmr_analysis.FileTypeError('File must be .ice file!')
                self.refresh_tables()
            except nmr_analysis.FileTypeError as e:
                self.show_message_box(str(e))
        self.set_data_change_handler()

    def add_data_dialog(self):
        self.ban_data_change_hander()
        fname, ftype = QtWidgets.QFileDialog.getOpenFileNames(self, 'Add (Multiple) Data')
        if fname:
            try:
                self.reader.add_files(fname)
                self.refresh_tables()
            except Exception as e:
                self.show_message_box(str(e))
        self.set_data_change_handler()

    def save_data_dialog(self):
        fname, ftype = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as .ice file')
        if fname:
            self.reader.save(fname)

    # Tools Menu
    # TODO Fit
    def show_fit_dialog(self):
        self.show_message_box('Function Under Development!', 'Fit')

    # Window Menu
    # TODO Operation Queue
    def show_operation_queue_dialog(self):
        self.show_message_box('<b>TimeProcess:</b> <br>'
                              'BaseLine -> Cut -> Phase -> Treat <br>'
                              '<b>FreqProcess:</b> <br>'
                              'HalfEchoMove -> FFT -> FullEchoMux -> Treat', 'Operation Queue')

    # Help Menu
    def show_help_index_widget(self):
        self.show_message_box('Function Under Development!', 'Help Index')



    # TODO report bug
    def show_report_bug_dialog(self):
        bug_text = QtWidgets.QInputDialog.getText(self, 'Report Bug', 'Input your description here or send it directly to lianxiangru@gmail.com')
        if bug_text:
            pass

    # TODO open web site
    def open_website(self):
        pass

    def show_about_message(self):
        self.show_message_box('NMR Data Analysis System\n'
        'Version:\t1.00\n'
        'Author:\tXiangru Lian\n'
        'E-mail:\tlianxiangru@gmail.com', 'About')

    ################################### Note #######################################
    def save_note(self):
        self.reader.note = self.note_textedit.toPlainText()
        self.show_message_box('Note Saved!')

    ################################# OTHERS #######################################

    # Message

    def show_message_box(self, message, title = 'Attention!'):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setText(message)
        message_box.setWindowTitle(title)
        message_box.show()

    # Refresh

    def refresh_tables(self):
        self.refresh_data_selection_table()
        self.refresh_basic_process_table(0)
        self.refresh_advanced_process_table(0)
        self.refresh_glue_int_table()
        self.show_message_box('All tables refreshed!')

    def refresh_basic_advanced_process_table(self, index):
        self.refresh_basic_process_table(index)
        self.refresh_advanced_process_table(index)

    def refresh_data_selection_table(self):
        self.data_row_selection_table.clear()
        self.data_row_selection_table.setColumnCount(len(nmr_analysis.QT_DATA_COLUMN_ENTRIES))
        self.data_row_selection_table.setRowCount(len(self.reader.dics))
        self.data_row_selection_table.setHorizontalHeaderLabels(nmr_analysis.QT_DATA_COLUMN_ENTRIES)
        for row, dics in enumerate(self.reader.dics):
            for key in dics[0]:
                if key in nmr_analysis.QT_DATA_COLUMN_ENTRIES:
                    cell = QtWidgets.QTableWidgetItem()
                    cell.setData(QtCore.Qt.EditRole, dics[0][key])
                    self.data_row_selection_table.setItem(row, nmr_analysis.QT_DATA_COLUMN_ENTRIES.index(key), cell)


    def refresh_basic_process_table(self, index):
        self.basic_process_para_table.clear()
        self.basic_process_para_table.setColumnCount(1)
        self.basic_process_para_table.setRowCount(len(nmr_analysis.QT_BASIC_PROCESS_DIC))
        key_list = [key for key in nmr_analysis.QT_BASIC_PROCESS_DIC]
        dic = self.reader.dics[index][1]
        self.basic_process_para_table.setVerticalHeaderLabels(key_list)
        self.basic_process_para_table.setHorizontalHeaderLabels(['Value'])
        for key in dic:
            if key in nmr_analysis.QT_BASIC_PROCESS_DIC:
                cell = QtWidgets.QTableWidgetItem()
                cell.setData(QtCore.Qt.EditRole, dic[key])
                self.basic_process_para_table.setItem(key_list.index(key), 0, cell)

    def refresh_advanced_process_table(self, index):
        self.advanced_process_para_table.clear()
        self.advanced_process_para_table.setColumnCount(1)
        self.advanced_process_para_table.setRowCount(len(nmr_analysis.QT_ADVANCED_PROCESS_DIC))
        key_list = [key for key in nmr_analysis.QT_ADVANCED_PROCESS_DIC]
        dic = self.reader.dics[index][2]
        self.advanced_process_para_table.setVerticalHeaderLabels(key_list)
        self.advanced_process_para_table.setHorizontalHeaderLabels(['Value'])
        for key in dic:
            if key in nmr_analysis.QT_ADVANCED_PROCESS_DIC:
                cell = QtWidgets.QTableWidgetItem()
                cell.setData(QtCore.Qt.EditRole, dic[key])
                self.advanced_process_para_table.setItem(key_list.index(key), 0, cell)

    def refresh_glue_int_table(self):
        self.glue_int_para_table.clear()
        self.glue_int_para_table.setColumnCount(1)
        self.glue_int_para_table.setRowCount(len(nmr_analysis.QT_GLUE_INT_OPERATION_DIC))
        key_list = [key for key in nmr_analysis.QT_GLUE_INT_OPERATION_DIC]
        dic = self.reader.root_dic
        self.glue_int_para_table.setVerticalHeaderLabels(key_list)
        self.glue_int_para_table.setHorizontalHeaderLabels(['Value'])
        for key in dic:
            if key in nmr_analysis.QT_GLUE_INT_OPERATION_DIC:
                cell = QtWidgets.QTableWidgetItem()
                cell.setData(QtCore.Qt.EditRole, dic[key])
                self.glue_int_para_table.setItem(key_list.index(key), 0, cell)


    # Data Change

    def set_data_change_handler(self):
        self.data_row_selection_table.itemChanged.connect(self.data_row_selection_data_change)
        self.basic_process_para_table.itemChanged.connect(self.basic_process_data_change)
        self.advanced_process_para_table.itemChanged.connect(self.advanced_process_data_change)
        self.glue_int_para_table.itemChanged.connect(self.glue_int_para_data_change)

        self.glue_checkbox.stateChanged.connect(self.glue_checkbox_change)

    def ban_data_change_hander(self):
        self.data_row_selection_table.itemChanged.disconnect()
        self.basic_process_para_table.itemChanged.disconnect()
        self.advanced_process_para_table.itemChanged.disconnect()
        self.glue_int_para_table.itemChanged.disconnect()

        self.glue_checkbox.stateChanged.disconnect()

    def data_row_selection_data_change(self, cell_item):
        self.reader.dics[cell_item.row()][0][nmr_analysis.QT_DATA_COLUMN_ENTRIES[cell_item.column()]] = cell_item.data(QtCore.Qt.EditRole)

    def basic_process_data_change(self, cell_item):
        if not self.apply_to_all_checkbox.isChecked():
            self.reader.dics[self.data_row_selection_table.currentRow()][1][self.basic_process_para_table.verticalHeaderItem(cell_item.row()).text()] = cell_item.data(QtCore.Qt.EditRole)
        else:
            for dic in self.reader.dics:
                dic[1][self.basic_process_para_table.verticalHeaderItem(cell_item.row()).text()] = cell_item.data(QtCore.Qt.EditRole)
        self.refresh_plot_window(index = self.data_row_selection_table.currentRow())

    def advanced_process_data_change(self, cell_item):
        if not self.apply_to_all_checkbox.isChecked():
            self.reader.dics[self.data_row_selection_table.currentRow()][2][self.advanced_process_para_table.verticalHeaderItem(cell_item.row()).text()] = cell_item.data(QtCore.Qt.EditRole)
        else:
            for dic in self.reader.dics:
                dic[2][self.advanced_process_para_table.verticalHeaderItem(cell_item.row()).text()] = cell_item.data(QtCore.Qt.EditRole)
        self.refresh_plot_window(index = self.data_row_selection_table.currentRow())

    def glue_int_para_data_change(self, cell_item):
        self.reader.root_dic[self.glue_int_para_table.verticalHeaderItem(cell_item.row()).text()] = cell_item.data(QtCore.Qt.EditRole)
        self.refresh_plot_window(time=False, freq=False)

    def glue_checkbox_change(self):
        self.refresh_plot_window(time=False, freq=False, inte=False)

    # Plot
    def data_row_selection_selection_change(self, cr, cc, pr, pc):
        self.ban_data_change_hander()
        print(cr)
        self.refresh_plot_window(glue= False, inte = False, index=cr)
        self.refresh_basic_advanced_process_table(cr)
        self.set_data_change_handler()

    def refresh_plot_window(self, time = True, freq = True, glue = True, inte = True, index = None):
        print('refresh plot window executed')
        if time and self.time_checkbox.isChecked() and index!=None:
            self.plot_window.plot_time(*self.reader.get_time_plot_dic_data(index))
        if freq and self.freq_checkbox.isChecked() and index!=None:
            self.plot_window.plot_freq(*self.reader.get_freq_plot_dic_data(index))
        if inte and self.int_checkbox.isChecked():
            self.plot_window.plot_int(self.reader.get_int_plot_dic(), x_label=self.reader.root_dic['Int_x'])
        if glue and self.glue_checkbox.isChecked():
            self.plot_window.plot_glue(*self.reader.get_glue_plot_dic_data(), title='Glue', x_label='Frequency')

    def refresh_all_plot(self):
        self.refresh_plot_window()

if __name__ =='__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())
