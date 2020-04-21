# -*- coding: utf-8 -*-

import sys
import serial_port
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QCheckBox,QPushButton, QAction, QLineEdit, QMessageBox, QComboBox, QLabel, QLCDNumber, QMessageBox
from PyQt5.QtGui import QIcon, QPainter, QColor, QFont, QRegExpValidator
from PyQt5.QtCore import pyqtSlot, QRegExp
 
class App(QMainWindow):
 
   def __init__(self):
      super().__init__()
      self.title = 'Generator Holzworth'
      self.left = 30
      self.top = 30
      self.width = 720
      self.height = 500
      self.initUI()
 
   def initUI(self):
      self.setWindowTitle(self.title)
      self.setGeometry(self.left, self.top, self.width, self.height)
# get available ports on start
      self.available_ports=serial_port.list_ports()
# combo for choose appropriate port
      self.port_select=QComboBox(self)
      self.port_select.addItems(self.available_ports)
      self.port_select.move(500,400)
# LCDs and labels for frequency, power and phase settings      
      self.lcd_f1=QLCDNumber(self)
      self.lcd_f1.move(20,30)
      self.lcd_f1.resize(260,50)
      self.lcd_f1.display(100.0)
      self.lcd_f1.setDigitCount(11)

      self.f1_label=QLabel("MHz",self)
      self.f1_label.move(285,40)
      self.f1_label.setFont(QFont('Times',20))

      self.lcd_p1=QLCDNumber(self)
      self.lcd_p1.move(350,30)
      self.lcd_p1.resize(100,50)
      self.lcd_p1.display(0.0)

      p1_label=QLabel("dBm",self)
      p1_label.move(455,40)
      p1_label.setFont(QFont('Times',20))
     
      self.lcd_ph1=QLCDNumber(self)
      self.lcd_ph1.move(525,30)
      self.lcd_ph1.resize(100,50)
      self.lcd_ph1.display(0.0)

      ph1_label=QLabel(u"°",self)
      ph1_label.move(630,30)
      ph1_label.setFont(QFont('Times',20))
# checkbox to choose channel
      self.label_ch1 = QLabel(u"Kanał 1",self)
      self.label_ch1.move(20,5)

      self.label_ch2 = QLabel(u"Kanał 2",self)
      self.label_ch2.move(20,95)

      self.cb_ch1 = QCheckBox(u"Kanał 1",self)
      self.cb_ch1.move(20,300)
      
      self.cb_ch2 = QCheckBox(u"Kanał 2",self)
      self.cb_ch2.move(20,330)
#LCDs and labels for second channel
      self.lcd_f2=QLCDNumber(self)
      self.lcd_f2.move(20,120)
      self.lcd_f2.resize(260,50)
      self.lcd_f2.display(100.0)
      self.lcd_f2.setDigitCount(11)

      self.f2_label=QLabel("MHz",self)
      self.f2_label.move(285,130)
      self.f2_label.setFont(QFont('Times',20))
      
      self.lcd_p2=QLCDNumber(self)
      self.lcd_p2.move(350,120)
      self.lcd_p2.resize(100,50)
      self.lcd_p2.display(0.0)

      p2_label=QLabel("dBm",self)
      p2_label.move(455,130)
      p2_label.setFont(QFont('Times',20))

      self.lcd_ph2=QLCDNumber(self)
      self.lcd_ph2.move(525,120)
      self.lcd_ph2.resize(100,50)
      self.lcd_ph2.display(0.0)

      ph2_label=QLabel(u"°",self)
      ph2_label.move(630,120)
      ph2_label.setFont(QFont('Times',20))
# textbox to edit to set generator parameters
      self.textbox_fset = QLineEdit(self)
      self.textbox_fset.move(20,220)
      self.textbox_fset.resize(200,40)

      self.textbox_pset = QLineEdit(self)
      self.textbox_pset.move(350,220)
      self.textbox_pset.resize(100,40)
      label_f=QLabel(u"Częstotliwość",self)
      label_f.move(20,195)
      
      label_p=QLabel("Moc",self)
      label_p.move(350,195)

      label_dbm=QLabel("dBm",self)
      label_dbm.move(455,220)

      label_ph=QLabel(u"Przesunięcie fazy",self)
      label_ph.move(525,195)
      
      self.textbox_phset = QLineEdit(self)
      self.textbox_phset.move(525,220)
      self.textbox_phset.resize(100,40)
      
      label_Hz=QLabel("Hz",self)
      label_Hz.move(230,220)
# regular expression for settings
      reg_exp_freq=QRegExp("[0-9]{0,4}[.]{0,1}[0-9]{0,6}[kMG]")# 4 digits before dot, 6 after, must end with k,M or G
      gen_validator=QRegExpValidator(reg_exp_freq, self.textbox_fset)
      self.textbox_fset.setValidator(gen_validator)
# regex for power settings      
      reg_exp_power=QRegExp("[-]*[0-9]+[.]*[0-9]{2}")
      gen_validator=QRegExpValidator(reg_exp_power, self.textbox_pset)
      self.textbox_pset.setValidator(gen_validator)
# regex for phase settings
      phase_validator=QRegExpValidator(QRegExp("[0-9]+[.]*[0-9]"),self.textbox_phset)
      self.textbox_phset.setValidator(phase_validator)
# button for refresh available serial ports 
      self.ports_button=QPushButton(u"Odśwież porty",self)
      self.ports_button.move(400,400)
      self.ports_button.clicked.connect(self.refresh_ports)
# button to set generator       
      self.activate_button = QPushButton('Ustaw', self)
      self.activate_button.move(300,400)
      self.activate_button.clicked.connect(self.on_click)
      
      self.show()

   def on_click(self) :
       generator_port=serial_port.GenSerialPort(str(self.port_select.currentText()))
       # __init__ of GenSerialPort check if port exist and is ready to use
       if generator_port.isCreate() == False :
          QMessageBox.about(self,"Komunikat","Wybrany port nie istnieje")
          del generator_port
          return  
       user_freq=self.textbox_fset.text()
       user_pwr=self.textbox_pset.text()
       user_ph=self.textbox_phset.text()
       freq_dict={'k':'kHz','M':'MHz','G':'GHz'}
       if self.cb_ch1.isChecked() :
          generator_port.setActiveChannel(1)
          if user_pwr :
             cP=checkPower(user_pwr)
             if cP[0] :
                self.lcd_p1.display(user_pwr)
                generator_port.setPower(user_pwr)
             else :
                QMessageBox.about(self,"Komunikat",cP[1])
          if user_ph :
             cPh=checkPhase(user_ph)  
             if cPh[0] :
                self.lcd_ph1.display(user_ph)
                generator_port.setPhase(user_ph)
             else :
                QMessageBox.about(self,"Komunikat",cPh[1])
          if user_freq :
             cF=checkFrequency(user_freq)
             if cF[0] :
                self.lcd_f1.display(user_freq[0:len(user_freq)-1])
                generator_port.setFrequency(user_freq[0:len(user_freq)-1],freq_dict[user_freq[len(user_freq)-1]])
                self.f1_label.setText(freq_dict[user_freq[len(user_freq)-1]])
             else :
                QMessageBox.about(self,"Komunikat",cF[1])

       if self.cb_ch2.isChecked() :
          generator_port.setActiveChannel(2)
          if user_pwr :
             cP=checkPower(user_pwr)
             if cP[0] :
                self.lcd_p2.display(user_pwr)
                generator_port.setPower(user_pwr)
             else :
                QMessageBox.about(self, "Komunikat",cP[1])
          if user_ph :
             cPh=checkPhase(user_ph)
             if cPh[0] :
                self.lcd_ph2.display(user_ph)
                generator_port.setPhase(user_ph)
             else :
                QMessageBox.about(self,"Komunikat",cPh[1])
          if user_freq :
             cF=checkFrequency(user_freq)
             if cF[0] :
                self.lcd_f2.display(user_freq[0:len(user_freq)-1])
                generator_port.setFrequency(user_freq[0:len(user_freq)-1],freq_dict[user_freq[len(user_freq)-1]])
                self.f2_label.setText(freq_dict[user_freq[len(user_freq)-1]])
             else :
                QMessageBox.about(self,"Komunikat",cF[1])
       del generator_port

   def refresh_ports(self) :
      self.port_select.clear()
      self.port_select.addItems(serial_port.list_ports())
       
def checkPower(power) :
   if float(power)< -80.0 :
      return [False,"Moc zbyt niska"]
   if float(power) > 10.0 :
      return [False,"Moc zbyt wysoka"]
   return [True,"OK"]
      
def checkFrequency(frequency) :
   f_dict_max={'k':6700000.0,'M':6700.0,'G':6.7}
   f_dict_min={'k':100.0,'M':0.1,'G':0.0001}#dolna granica 100 kHz, mozna latwo zmienic jakby co
   f_digits=frequency[0:len(frequency)-1]
   dec=frequency[len(frequency)-1]
   if dec not in ['k','M','G'] :
      return [False, u"Niepoprawna wartość"]
   if float(f_digits) > f_dict_max[dec] :
      return [False,u"Częstotliwość zbyt wysoka"]
   if float(f_digits) < f_dict_min[dec] :
      return [False,u"Częstotliwość zbyt niska"]
   return [True,"OK"]

def checkPhase(phase) :
   if float(phase) < 0.0 or float(phase) > 360.0 :
      return [False,u"Przesunięcie fazy może być jedynie między 0 a 360 stopni"]
   return [True,"OK"]           

if __name__ == '__main__' :
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

