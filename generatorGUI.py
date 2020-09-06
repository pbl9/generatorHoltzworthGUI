# -*- coding: utf-8 -*-

import sys
import genserialport
from generatorworker import GeneratorWorker
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QCheckBox, QPushButton, QLineEdit, 
                              QMessageBox, QComboBox, QLabel, QLCDNumber, QHBoxLayout)
from PyQt5.QtGui import QPainter, QColor, QFont, QRegExpValidator
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QRegExp, QThread
 
class App(QMainWindow):
   send_to_generator = pyqtSignal(str, tuple, str, str, str)
   def __init__(self):
      super().__init__()
      self.title = "Generator Holzworth"
      self.left = 30
      self.top = 30
      self.width = 720
      self.height = 500
      self.initUI()
 
   def initUI(self):
      self.setWindowTitle(self.title)
      self.setGeometry(self.left, self.top, self.width, self.height)
      # get available ports on start
      self.available_ports = genserialport.list_ports()
      # combo for choose appropriate port
      self.port_select = QComboBox(self)
      self.port_select.addItems(self.available_ports)
      self.port_select.move(550, 400)
      self.port_select.adjustSize()
      # LCDs and labels for frequency, power and phase settings      
      self.lcd_frequency_channel1 = QLCDNumber(self)
      self.lcd_frequency_channel1.move(20, 30)
      self.lcd_frequency_channel1.resize(260, 50)
      self.lcd_frequency_channel1.display(100.0)
      self.lcd_frequency_channel1.setDigitCount(11)

      self.channel1_mhz_label = QLabel("MHz", self)
      self.channel1_mhz_label.move(285, 40)
      self.channel1_mhz_label.setFont(QFont("Times", 20))

      self.lcd_power_channel1 = QLCDNumber(self)
      self.lcd_power_channel1.move(350, 30)
      self.lcd_power_channel1.resize(100, 50)
      self.lcd_power_channel1.display(0.0)

      ch1_dbm_label = QLabel("dBm",self)
      ch1_dbm_label.move(455, 40)
      ch1_dbm_label.setFont(QFont("Times", 20))
     
      self.lcd_phase_channel1 = QLCDNumber(self)
      self.lcd_phase_channel1.move(525, 30)
      self.lcd_phase_channel1.resize(100, 50)
      self.lcd_phase_channel1.display(0.0)

      ch1_degree_label = QLabel(u"°", self)
      ch1_degree_label.move(630, 30)
      ch1_degree_label.setFont(QFont("Times", 20))
      # checkbox to choose channel
      self.label_channel1 = QLabel(u"Kanał 1", self)
      self.label_channel1.move(20, 5)

      self.label_channel2 = QLabel(u"Kanał 2", self)
      self.label_channel2.move(20, 95)

      self.checkbox_channel1 = QCheckBox(u"Kanał 1", self)
      self.checkbox_channel1.move(20, 300)
      
      self.checkbox_channel2 = QCheckBox(u"Kanał 2", self)
      self.checkbox_channel2.move(20, 330)
      #LCDs and labels for second channel
      self.lcd_frequency_channel2 = QLCDNumber(self)
      self.lcd_frequency_channel2.move(20, 120)
      self.lcd_frequency_channel2.resize(260, 50)
      self.lcd_frequency_channel2.display(100.0)
      self.lcd_frequency_channel2.setDigitCount(11)

      self.f2_label = QLabel("MHz", self)
      self.f2_label.move(285, 130)
      self.f2_label.setFont(QFont("Times", 20))
      
      self.lcd_power_channel2 = QLCDNumber(self)
      self.lcd_power_channel2.move(350, 120)
      self.lcd_power_channel2.resize(100, 50)
      self.lcd_power_channel2.display(0.0)

      ch2_dbm_label = QLabel("dBm",self)
      ch2_dbm_label.move(455, 130)
      ch2_dbm_label.setFont(QFont("Times", 20))

      self.lcd_phase_channel2 = QLCDNumber(self)
      self.lcd_phase_channel2.move(525, 120)
      self.lcd_phase_channel2.resize(100, 50)
      self.lcd_phase_channel2.display(0.0)

      ch2_degree_label = QLabel(u"°", self)
      ch2_degree_label.move(630, 120)
      ch2_degree_label.setFont(QFont("Times", 20))
      # textbox to edit to set generator parameters
      self.textbox_frequency_set = QLineEdit(self)
      self.textbox_frequency_set.move(20, 220)
      self.textbox_frequency_set.resize(200, 40)

      self.textbox_power_set = QLineEdit(self)
      self.textbox_power_set.move(350, 220)
      self.textbox_power_set.resize(100, 40)
      
      label_frequency = QLabel(u"Częstotliwość", self)
      label_frequency.move(20, 195)
      label_frequency.adjustSize()

      label_power = QLabel("Moc", self)
      label_power.move(350, 195)

      label_dbm = QLabel("dBm", self)
      label_dbm.move(455, 220)

      label_phase = QLabel(u"Przesunięcie fazy", self)
      label_phase.move(525, 195)
      label_phase.adjustSize()
      
      self.textbox_phase_set = QLineEdit(self)
      self.textbox_phase_set.move(525, 220)
      self.textbox_phase_set.resize(100, 40)
      
      label_Hz = QLabel("Hz", self)
      label_Hz.move(230, 220)
      # regular expression for settings
      reg_exp_freq = QRegExp("[0-9]{0,4}[.]{0,1}[0-9]{0,6}[kMG]")# 4 digits before dot, 6 after, must end with k,M or G
      gen_validator = QRegExpValidator(reg_exp_freq, self.textbox_frequency_set)
      self.textbox_frequency_set.setValidator(gen_validator)
      # regex for power settings      
      reg_exp_power = QRegExp("[-]*[0-9]+[.]*[0-9]{2}")
      gen_validator = QRegExpValidator(reg_exp_power, self.textbox_power_set)
      self.textbox_power_set.setValidator(gen_validator)
      # regex for phase settings
      phase_validator = QRegExpValidator(QRegExp("[0-9]+[.]*[0-9]"), self.textbox_phase_set)
      self.textbox_phase_set.setValidator(phase_validator)
      # button for refresh available serial ports 
      self.ports_button = QPushButton(u"Odśwież porty", self)
      self.ports_button.move(400, 400)
      self.ports_button.clicked.connect(self.refresh_ports)
      self.ports_button.adjustSize()
      # button to set generator       
      self.activate_button = QPushButton("Ustaw", self)
      self.activate_button.move(300, 400)
      # thread creation and signals and slots connection
      self.generator_thread = QThread()
      self.generator_worker = GeneratorWorker()
      self.generator_worker.moveToThread(self.generator_thread)
      self.activate_button.clicked.connect(self.get_user_input_and_send_to_generator)
      self.send_to_generator.connect(self.generator_worker.send_settings_to_generator)
      self.generator_worker.set_display.connect(self.show_on_display)
      self.generator_worker.event_occured.connect(self.show_event)
      self.generator_thread.start()

      self.show()

   def show_on_display(self, setting : str):
      if setting == "frequency":
         user_freq_set = self.textbox_frequency_set.text()
         self.lcd_frequency_channel2.display(user_freq_set[0:len(user_freq_set)-1])
         self.f2_label.setText(GeneratorWorker.freq_dict[user_freq_set[len(user_freq_set)-1]])
      elif setting == "power":
         self.lcd_power_channel2.display(self.textbox_power_set.text())
      elif setting == "phase":
         self.lcd_phase_channel2.display(self.textbox_phase_set.text())

   def show_event(self, message):
       QMessageBox.about(self, "Komunikat", message)


   def get_user_input_and_send_to_generator(self):
      user_freq = self.textbox_frequency_set.text()
      user_pwr = self.textbox_power_set.text()
      user_ph = self.textbox_phase_set.text()
      current_port = str(self.port_select.currentText())
      active_channels = (self.checkbox_channel1.isChecked(), self.checkbox_channel2.isChecked())
      self.send_to_generator.emit(current_port, active_channels, user_freq, user_pwr, user_ph)

   def refresh_ports(self) :
      self.port_select.clear()
      self.port_select.addItems(genserialport.list_ports())       

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

