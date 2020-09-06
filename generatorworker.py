from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from genserialport import GenSerialPort

class GeneratorWorker(QObject):
    max_power = 10.0
    min_power = -80.0
    max_phase = 360.0
    min_phase = 0.0
    freq_dict = {'k':'kHz','M':'MHz','G':'GHz'}
    event_occured = pyqtSignal(str)
    set_display = pyqtSignal(str)
    
    def send_settings_to_generator(self, port, active_channels, user_freq_set, user_power_set,  user_phase_set):
        generator_port = GenSerialPort(port)
        if not generator_port.isCreated:
            self.event_occured.emit("Wybrany port nie istnieje.")
            return
        if active_channels[0]:
            generator_port.setActiveChannel(1)
            self.set_generator(generator_port, user_power_set, user_freq_set, user_phase_set)
        if active_channels[1]:
            generator_port.setActiveChannel(2)
            self.set_generator(generator_port, user_power_set, user_freq_set, user_phase_set)

        del generator_port    
       
    def set_generator(self, generator_serial_port, user_power_set, user_freq_set, user_phase_set):
        if user_power_set:
            cP = self.checkPower(float(user_power_set))
            if cP[0]:
               generator_serial_port.setPower(user_power_set)
               self.set_display.emit("power")
            else:
               self.event_occured.emit(cP[1])
            if user_phase_set:
               cPh = self.checkPhase(float(user_phase_set))
               if cPh[0]:
                  generator_serial_port.setPhase(user_phase_set)
                  self.set_display.emit("phase")
               else:
                  self.event_occured.emit(cP[1])
            if user_freq_set:
               cF = self.checkFrequency(user_freq_set)
               if cF[0]:
                  generator_serial_port.setFrequency(user_freq_set[0:len(user_freq_set)-1], self.freq_dict[user_freq_set[len(user_freq_set)-1]])
                  self.set_display.emit("frequency")
               else:
                  self.event_occured.emit(cP[1])            

    def checkPower(self, power : float):
        if power < GeneratorWorker.min_power:
            return (False, "Moc zbyt niska")
        elif power > GeneratorWorker.max_power:
            return (False, "Moc zbyt wysoka")
        else:
            return (True, "OK")        
      
    def checkFrequency(self, frequency):
        f_dict_max = {'k':6700000.0,'M':6700.0,'G':6.7}
        f_dict_min = {'k':100.0,'M':0.1,'G':0.0001}
        f_digits = frequency[0:len(frequency)-1]
        decade = frequency[len(frequency)-1]
        if decade not in ['k','M','G']:
            return (False, u"Niepoprawna wartość")
        if float(f_digits) > f_dict_max[decade] :
            return (False, u"Częstotliwość zbyt wysoka")
        if float(f_digits) < f_dict_min[decade] :
            return (False, u"Częstotliwość zbyt niska")
        return (True, "OK")

    def checkPhase(self, phase : float):
        if phase < GeneratorWorker.min_phase or phase > GeneratorWorker.max_phase:
            return (False, "Przesunięcie fazy może być jedynie między {} a {} stopni".format(GeneratorWorker.min_phase, GeneratorWorker.max_phase))
        return (True, "OK")  
