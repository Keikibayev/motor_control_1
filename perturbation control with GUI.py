import odrive
import time
import sys
import odrive.shell
import kbhit
import random
import csv

AXIS_STATE_FULL_CALIBRATION_SEQUENCE = 3
AXIS_STATE_CLOSED_LOOP_CONTROL = 8
AXIS_STATE_IDLE = 1
CONTROL_MODE_TORQUE_CONTROL = 1
CONTROL_MODE_POSITION_CONTROL = 3

run_gait_flag = False
interval = 1
current_time = 0
sequence = [i for i in range(3,6)]
motor_num = [i for i in range(1,5)]
random_number = random.choice(sequence)
random_motor = random.choice(motor_num)
negative = -1
delay = 0.2
counter = 0
torque = 0.09
int_counter = 0
pat_name = ""
torque_value = 0.01

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(511, 810)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout.addWidget(self.line_6)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMaximumSize(QtCore.QSize(300, 16777215))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 65))
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.widget_4)
        self.label_6.setMinimumSize(QtCore.QSize(150, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.pat_name_txt = QtWidgets.QLineEdit(self.widget_4)
        self.pat_name_txt.setMinimumSize(QtCore.QSize(140, 0))
        self.pat_name_txt.setObjectName("pat_name_txt")
        self.horizontalLayout_4.addWidget(self.pat_name_txt)
        self.verticalLayout.addWidget(self.widget_4)
        self.line_4 = QtWidgets.QFrame(self.widget)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout.addWidget(self.line_4)
        self.widget_23 = QtWidgets.QWidget(self.widget)
        self.widget_23.setMinimumSize(QtCore.QSize(0, 300))
        self.widget_23.setObjectName("widget_23")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.widget_23)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.widget_24 = QtWidgets.QWidget(self.widget_23)
        self.widget_24.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_24.setObjectName("widget_24")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.widget_24)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_9 = QtWidgets.QLabel(self.widget_24)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_15.addWidget(self.label_9)
        self.verticalLayout_14.addWidget(self.widget_24)
        self.widget_19 = QtWidgets.QWidget(self.widget_23)
        self.widget_19.setObjectName("widget_19")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_19)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.connect_btn = QtWidgets.QPushButton(self.widget_19)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.connect_btn.setFont(font)
        self.connect_btn.setObjectName("connect_btn")
        self.verticalLayout_4.addWidget(self.connect_btn)
        self.run_btn = QtWidgets.QPushButton(self.widget_19)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.run_btn.setFont(font)
        self.run_btn.setObjectName("run_btn")
        self.verticalLayout_4.addWidget(self.run_btn)
        self.idle_btn = QtWidgets.QPushButton(self.widget_19)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.idle_btn.setFont(font)
        self.idle_btn.setObjectName("idle_btn")
        self.verticalLayout_4.addWidget(self.idle_btn)
        self.calibr_btn = QtWidgets.QPushButton(self.widget_19)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.calibr_btn.setFont(font)
        self.calibr_btn.setObjectName("calibr_btn")
        self.verticalLayout_4.addWidget(self.calibr_btn)
        self.exit_btn = QtWidgets.QPushButton(self.widget_19)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.exit_btn.setFont(font)
        self.exit_btn.setObjectName("exit_btn")
        self.verticalLayout_4.addWidget(self.exit_btn)
        self.verticalLayout_14.addWidget(self.widget_19)
        self.verticalLayout.addWidget(self.widget_23)
        self.line_3 = QtWidgets.QFrame(self.widget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.widget_13 = QtWidgets.QWidget(self.widget_3)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.widget_22 = QtWidgets.QWidget(self.widget_13)
        self.widget_22.setObjectName("widget_22")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.widget_22)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_2 = QtWidgets.QLabel(self.widget_22)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_13.addWidget(self.label_2)
        self.verticalLayout_12.addWidget(self.widget_22)
        self.widget_20 = QtWidgets.QWidget(self.widget_13)
        self.widget_20.setObjectName("widget_20")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_20)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(self.widget_20)
        self.label_7.setMinimumSize(QtCore.QSize(100, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.min_time_txt = QtWidgets.QLineEdit(self.widget_20)
        self.min_time_txt.setMinimumSize(QtCore.QSize(100, 0))
        self.min_time_txt.setObjectName("min_time_txt")
        self.horizontalLayout_9.addWidget(self.min_time_txt)
        self.verticalLayout_12.addWidget(self.widget_20)
        self.widget_21 = QtWidgets.QWidget(self.widget_13)
        self.widget_21.setObjectName("widget_21")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.widget_21)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.widget_21)
        self.label_8.setMinimumSize(QtCore.QSize(100, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.max_time_txt = QtWidgets.QLineEdit(self.widget_21)
        self.max_time_txt.setMinimumSize(QtCore.QSize(100, 0))
        self.max_time_txt.setObjectName("max_time_txt")
        self.horizontalLayout_8.addWidget(self.max_time_txt)
        self.verticalLayout_12.addWidget(self.widget_21)
        self.apply_btn = QtWidgets.QPushButton(self.widget_13)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(True)
        font.setUnderline(False)
        font.setWeight(50)
        self.apply_btn.setFont(font)
        self.apply_btn.setObjectName("apply_btn")
        self.verticalLayout_12.addWidget(self.apply_btn)
        self.verticalLayout_5.addWidget(self.widget_13)
        self.verticalLayout.addWidget(self.widget_3)
        self.line_2 = QtWidgets.QFrame(self.widget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout.addWidget(self.line_2)
        self.widget_12 = QtWidgets.QWidget(self.widget)
        self.widget_12.setMaximumSize(QtCore.QSize(16777215, 200))
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.widget_12)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.status_label = QtWidgets.QLabel(self.widget_12)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.status_label.setFont(font)
        self.status_label.setText("")
        self.status_label.setObjectName("status_label")
        self.verticalLayout_16.addWidget(self.status_label)
        self.verticalLayout.addWidget(self.widget_12)
        self.horizontalLayout.addWidget(self.widget)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setLineWidth(4)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_5 = QtWidgets.QWidget(self.widget_2)
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_11 = QtWidgets.QWidget(self.widget_5)
        self.widget_11.setMinimumSize(QtCore.QSize(150, 80))
        self.widget_11.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_11.setObjectName("widget_11")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.widget_11)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_7.addWidget(self.label_3)
        self.bk_lt_spin = QtWidgets.QSpinBox(self.widget_11)
        self.bk_lt_spin.setMinimumSize(QtCore.QSize(0, 30))
        self.bk_lt_spin.setMaximumSize(QtCore.QSize(40, 16777215))
        self.bk_lt_spin.setMaximum(10)
        self.bk_lt_spin.setProperty("value", 3)
        self.bk_lt_spin.setObjectName("bk_lt_spin")
        self.verticalLayout_7.addWidget(self.bk_lt_spin, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.widget_11)
        self.widget_15 = QtWidgets.QWidget(self.widget_5)
        self.widget_15.setMinimumSize(QtCore.QSize(150, 80))
        self.widget_15.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_15.setObjectName("widget_15")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.widget_15)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_4 = QtWidgets.QLabel(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_9.addWidget(self.label_4)
        self.bk_rt_spin = QtWidgets.QSpinBox(self.widget_15)
        self.bk_rt_spin.setMinimumSize(QtCore.QSize(0, 30))
        self.bk_rt_spin.setMaximumSize(QtCore.QSize(40, 16777215))
        self.bk_rt_spin.setMaximum(10)
        self.bk_rt_spin.setProperty("value", 3)
        self.bk_rt_spin.setObjectName("bk_rt_spin")
        self.verticalLayout_9.addWidget(self.bk_rt_spin, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.widget_15)
        self.widget_10 = QtWidgets.QWidget(self.widget_5)
        self.widget_10.setMinimumSize(QtCore.QSize(150, 80))
        self.widget_10.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.fr_lt_spin = QtWidgets.QSpinBox(self.widget_10)
        self.fr_lt_spin.setMinimumSize(QtCore.QSize(0, 30))
        self.fr_lt_spin.setMaximumSize(QtCore.QSize(40, 16777215))
        self.fr_lt_spin.setAlignment(QtCore.Qt.AlignCenter)
        self.fr_lt_spin.setMaximum(10)
        self.fr_lt_spin.setProperty("value", 3)
        self.fr_lt_spin.setObjectName("fr_lt_spin")
        self.verticalLayout_3.addWidget(self.fr_lt_spin, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.widget_10)
        self.widget_17 = QtWidgets.QWidget(self.widget_5)
        self.widget_17.setMinimumSize(QtCore.QSize(150, 80))
        self.widget_17.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget_17.setObjectName("widget_17")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.widget_17)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_5 = QtWidgets.QLabel(self.widget_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_11.addWidget(self.label_5)
        self.fr_rt_spin = QtWidgets.QSpinBox(self.widget_17)
        self.fr_rt_spin.setMinimumSize(QtCore.QSize(0, 30))
        self.fr_rt_spin.setMaximumSize(QtCore.QSize(40, 16777215))
        self.fr_rt_spin.setMaximum(10)
        self.fr_rt_spin.setProperty("value", 3)
        self.fr_rt_spin.setObjectName("fr_rt_spin")
        self.verticalLayout_11.addWidget(self.fr_rt_spin, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.widget_17)
        self.horizontalLayout_2.addWidget(self.widget_5)
        self.horizontalLayout.addWidget(self.widget_2)
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout.addWidget(self.line_5)
        MainWindow.setCentralWidget(self.centralwidget)

        ########################################
        self.connect_btn.clicked.connect(odrive_config)
        self.run_btn.clicked.connect(GaitLoop)
        self.idle_btn.clicked.connect(Idle)
        self.calibr_btn.clicked.connect(Calibrate)
        self.apply_btn.clicked.connect(Random_time)
        self.exit_btn.clicked.connect(Exit)
        ########################################

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "Patient name"))
        self.label_9.setText(_translate("MainWindow", "Control buttons"))
        self.connect_btn.setText(_translate("MainWindow", "CONNECT"))
        self.run_btn.setText(_translate("MainWindow", "RUN"))
        self.idle_btn.setText(_translate("MainWindow", "IDLE"))
        self.calibr_btn.setText(_translate("MainWindow", "CALIBRATE"))
        self.exit_btn.setText(_translate("MainWindow", "EXIT"))
        self.label_2.setText(_translate("MainWindow", "Randomizer time"))
        self.label_7.setText(_translate("MainWindow", "Min time (s)"))
        self.label_8.setText(_translate("MainWindow", "Max time (s)"))
        self.apply_btn.setText(_translate("MainWindow", "APPLY"))
        self.label_3.setText(_translate("MainWindow", "Back Left"))
        self.label_4.setText(_translate("MainWindow", "Back Right"))
        self.label.setText(_translate("MainWindow", "Front Left"))
        self.label_5.setText(_translate("MainWindow", "Front Right"))

def odrive_config():
    global Fr_Lt
    global Fr_Rt
    global Bk_Lt
    global Bk_Rt
    global FrMt
    global BkMt
    global run_gait_flag
    global odrive_connected

    run_gait_flag = False
    print("Searching for ODrive...")

    Front_Motor = odrive.find_any(serial_number="2066398E5453")
    Back_Motor = odrive.find_any(serial_number="2084398D5453")

    if len(odrive.connected_devices) != 2:
        ui.status_label.setText("Connection Error!")

    if Front_Motor:
        print("Front Odrive detected!")
        FrMt = Front_Motor
        Fr_Lt = getattr(FrMt, "axis0")
        Fr_Rt = getattr(FrMt, "axis1")
    
    if Back_Motor:
        print("Back Odrive detected!")
        BkMt = Back_Motor
        Bk_Lt = getattr(BkMt, "axis0")
        Bk_Rt = getattr(BkMt, "axis1")
    
    odrive_connected = True
    
    Fr_Lt.requested_state = AXIS_STATE_IDLE
    Fr_Rt.requested_state = AXIS_STATE_IDLE
    Bk_Lt.requested_state = AXIS_STATE_IDLE
    Bk_Rt.requested_state = AXIS_STATE_IDLE
    
    Fr_Lt.controller.input_torque = 0
    Fr_Rt.controller.input_torque = 0
    Bk_Lt.controller.input_torque = 0
    Bk_Rt.controller.input_torque = 0

    #******************configure Front Left motor**************************#
    Fr_Lt.requested_state = AXIS_STATE_IDLE
    Fr_Lt.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
    Fr_Lt.trap_traj.config.vel_limit = 60
    Fr_Lt.controller.config.vel_limit = 150

    #******************configure Front Right motor*************************#
    Fr_Rt.requested_state = AXIS_STATE_IDLE
    Fr_Rt.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
    Fr_Rt.trap_traj.config.vel_limit = 60
    Fr_Rt.controller.config.vel_limit = 150

    #******************configure Back Left motor***************************#
    Bk_Lt.requested_state = AXIS_STATE_IDLE
    Bk_Lt.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
    Bk_Lt.trap_traj.config.vel_limit = 60
    Bk_Lt.controller.config.vel_limit = 150

    #******************configure Back Left motor***************************#
    Bk_Rt.requested_state = AXIS_STATE_IDLE
    Bk_Rt.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL
    Bk_Rt.trap_traj.config.vel_limit = 60
    Bk_Rt.controller.config.vel_limit = 150

def recovery():
    global run_gait_flag
    global FrMt
    global BkMt
    global Fr_Lt
    global Fr_Rt
    global Bk_Lt
    global Bk_Rt
    global initial_position_Bk_Lt
    global initial_position_Bk_Rt
    global initial_position_Fr_Lt
    global initial_position_Fr_Rt

    current_position_Fr_Lt = Fr_Lt.encoder.pos_estimate
    current_position_Fr_Rt = Fr_Rt.encoder.pos_estimate
    current_position_Bk_Lt = Bk_Lt.encoder.pos_estimate
    current_position_Bk_Rt = Bk_Rt.encoder.pos_estimate

    if not (initial_position_Fr_Lt-20 < current_position_Fr_Lt < initial_position_Fr_Lt+20):
        Idle()
        time.sleep(1)
        print("Front Left spinning!")
        ui.status_label.setText("Front Left spinning!")
        
    if not (initial_position_Fr_Rt-20 < current_position_Fr_Rt < initial_position_Fr_Rt+20):
        Idle()
        time.sleep(1)
        print("Front Right spinning!")
        ui.status_label.setText("Front Right spinning!")

    if not (initial_position_Bk_Lt-20 < current_position_Bk_Lt < initial_position_Bk_Lt+20):
        Idle()
        time.sleep(1)
        print("Back Left spinning!")
        ui.status_label.setText("Back Left spinning!")

    if not (initial_position_Bk_Rt-20 < current_position_Bk_Rt < initial_position_Bk_Rt+20):
        Idle()
        time.sleep(1)
        print("Back Right spinning!")
        ui.status_label.setText("Back Right spinning!")
    
def Calibrate():
    global run_gait_flag
    global FrMt
    global BkMt
    global Fr_Lt
    global Fr_Rt
    global Bk_Lt
    global Bk_Rt
    global odrive_connected
    run_gait_flag = False

    if odrive_connected:
        ui.status_label.setText("Calibrating...")
        print("Calibrating...")
        FrMt.clear_errors()
        BkMt.clear_errors()
        time.sleep(1)
        Fr_Lt.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        Fr_Rt.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        Bk_Lt.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        Bk_Rt.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        time.sleep(15)
        ui.status_label.setText("")
    else: 
        ui.status_label.setText("First connect odrives!")
        print("First connect odrives!")

def Idle():
    global Fr_Lt
    global Fr_Rt
    global Bk_Lt
    global Bk_Rt
    global run_gait_flag
    global odrive_connected

    run_gait_flag = False
    if odrive_connected:
        ui.status_label.setText("Idle mode!")
        Fr_Lt.controller.input_torque = 0
        Fr_Rt.controller.input_torque = 0
        Bk_Lt.controller.input_torque = 0
        Bk_Rt.controller.input_torque = 0
        Fr_Lt.requested_state = AXIS_STATE_IDLE
        Fr_Rt.requested_state = AXIS_STATE_IDLE
        Bk_Lt.requested_state = AXIS_STATE_IDLE
        Bk_Rt.requested_state = AXIS_STATE_IDLE
    else: 
        ui.status_label.setText("First connect odrives!")
        print("First connect odrives!")

def Exit():
    global odrive_connected
    odrive_connected = True
    Idle()
    time.sleep(1)
    ui.status_label.setText("Exiting!")
    sys.exit(1)

def Random_time():
    global run_gait_flag
    global sequence
    global counter
    run_gait_flag = False
    min_sec = int(ui.min_time_txt.text())
    max_sec = int(ui.max_time_txt.text())
    if isinstance(min_sec, int) or isinstance(max_sec, int) or min_sec>max_sec:
        sequence = [i for i in range(min_sec, max_sec+1)]
        counter = 0
    else:
        ui.status_label.setText("Incorrect format!")

def GaitLoop():
    global first_time_to_run_exo
    global run_gait_flag
    global interval
    global current_time
    global FrMt
    global BkMt
    global Fr_Lt
    global Fr_Rt
    global Bk_Lt
    global Bk_Rt
    global sequence
    global random_number
    global motor_num
    global random_motor
    global delay
    global torque_bk_lt
    global torque_bk_rt
    global torque_fr_lt
    global torque_fr_rt
    global torque_value
    global initial_position_Bk_Lt
    global initial_position_Bk_Rt
    global initial_position_Fr_Lt
    global initial_position_Fr_Rt
    global odrive_connected

    if not odrive_connected:
        ui.status_label.setText("First connect odrives!")
        print("First connect odrives!")
        return

    if len(ui.pat_name_txt.text()) <= 2:
        ui.status_label.setText("Improper patient name!")
        return
    else:
        pat_name = ui.pat_name_txt.text()
    
    run_gait_flag = True
    first_time_to_run_exo = time.time()
    recovery_time = time.time()
    int_counter = 0
    interval = 1
    counter = 0

    ui.status_label.setText("Running!")

    initial_position_Fr_Lt = Fr_Lt.encoder.pos_estimate
    initial_position_Fr_Rt = Fr_Rt.encoder.pos_estimate
    initial_position_Bk_Lt = Bk_Lt.encoder.pos_estimate
    initial_position_Bk_Rt = Bk_Rt.encoder.pos_estimate

    with open('Perturb_data1.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Patient","Motor", "Time", "Torque"])
    
    Fr_Lt.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    Fr_Rt.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    Bk_Lt.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    Bk_Rt.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

    while True:
        try:
            current_time1 = time.time()
            if run_gait_flag and (current_time1-recovery_time) >= 0.1:
                recovery()
                recovery_time = current_time1

            current_time = time.time()
            if run_gait_flag and (current_time-first_time_to_run_exo) >= interval:
                torque_bk_lt = ui.bk_lt_spin.value()*torque_value
                torque_bk_rt = ui.bk_rt_spin.value()*torque_value
                torque_fr_lt = ui.fr_lt_spin.value()*torque_value
                torque_fr_rt = ui.fr_rt_spin.value()*torque_value
                Fr_Lt.controller.input_torque = torque_fr_lt
                Fr_Rt.controller.input_torque = torque_fr_rt*negative
                Bk_Lt.controller.input_torque = torque_bk_lt*negative
                Bk_Rt.controller.input_torque = torque_bk_rt
                        
                print("Counter: {}".format(counter))
                print("Int_counter: {}".format(int_counter))
                if int_counter == random_number:
                    if random_motor == 1:
                        Fr_Lt.controller.input_torque = torque_fr_lt*5
                        Fr_Rt.controller.input_torque = 0
                        Bk_Lt.controller.input_torque = 0
                        Bk_Rt.controller.input_torque = 0
                        print("Perturbation Front_Left motor in %2d seconds." % (counter))
                        time.sleep(delay)
                        Fr_Lt.controller.input_torque = torque_fr_lt
                        Fr_Rt.controller.input_torque = torque_fr_rt*negative
                        Bk_Lt.controller.input_torque = torque_bk_lt*negative
                        Bk_Rt.controller.input_torque = torque_bk_rt
                        
                        with open('Perturb_data1.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([pat_name, "Front_Left", counter, torque_fr_lt*5])
                                            
                    if random_motor == 2:
                        Fr_Rt.controller.input_torque = torque_fr_rt*5*negative
                        Fr_Lt.controller.input_torque = 0
                        Bk_Lt.controller.input_torque = 0
                        Bk_Rt.controller.input_torque = 0
                        print("Perturbation Front_Right motor in %2d seconds." % (counter))
                        time.sleep(delay)
                        Fr_Lt.controller.input_torque = torque_fr_lt
                        Fr_Rt.controller.input_torque = torque_fr_rt*negative
                        Bk_Lt.controller.input_torque = torque_bk_lt*negative
                        Bk_Rt.controller.input_torque = torque_bk_rt

                        with open('Perturb_data1.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([pat_name, "Front_Right", counter, torque_fr_rt*5])

                    if random_motor == 3:
                        Bk_Lt.controller.input_torque = torque_bk_lt*5*negative
                        Fr_Lt.controller.input_torque = 0
                        Fr_Rt.controller.input_torque = 0
                        Bk_Rt.controller.input_torque = 0
                        print("Perturbation Back_Left motor in %2d seconds." % (counter))
                        time.sleep(delay)
                        Fr_Lt.controller.input_torque = torque_fr_lt
                        Fr_Rt.controller.input_torque = torque_fr_rt*negative
                        Bk_Lt.controller.input_torque = torque_bk_lt*negative
                        Bk_Rt.controller.input_torque = torque_bk_rt

                        with open('Perturb_data1.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([pat_name, "Back_Left", counter, torque_bk_lt*5])

                    if random_motor == 4:
                        Bk_Rt.controller.input_torque = torque_bk_rt*5
                        Fr_Lt.controller.input_torque = 0
                        Fr_Rt.controller.input_torque = 0
                        Bk_Lt.controller.input_torque = 0
                        print("Perturbation Back_Right motor in %2d seconds." % (counter))
                        time.sleep(delay)
                        Fr_Lt.controller.input_torque = torque_fr_lt
                        Fr_Rt.controller.input_torque = torque_fr_rt*negative
                        Bk_Lt.controller.input_torque = torque_bk_lt*negative
                        Bk_Rt.controller.input_torque = torque_bk_rt

                        with open('Perturb_data1.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([pat_name, "Back_Right", counter, torque_bk_rt*5])

                    int_counter = 0
                    random_number = random.choice(sequence)
                    random_motor = random.choice(motor_num)
                    print("Next number: {}".format(random_number))

                else:
                    int_counter += 1
                
                counter += 1
                first_time_to_run_exo = current_time

        except Exception as err:
            Idle()
            time.sleep(1)
            print(f"Unexpected {err=}, {type(err)=}")
            raise

        except KeyboardInterrupt:
            print ('Interrupted from keyboard')
            Exit()

        QtCore.QCoreApplication.processEvents()

if __name__ == "__main__":
    odrive_connected = False
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec_()
        Exit()
        