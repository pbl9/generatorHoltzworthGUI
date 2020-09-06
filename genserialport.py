import serial
import sys
import platform
import glob

class GenSerialPort() :
    def __init__(self, port_name) :
       self.isCreated = False
       try :
          self.active_port = serial.Serial(port_name, 115200, serial.EIGHTBITS)
          if not self.active_port.is_open :
             self.active_port.open()
          self.isCreated = True
       except:
          self.isCreated = False
    
    def setFrequency(self, frequency, decade):
        """To set frequency user need to send message in format 
        FREQ:XXXXXXXXXXXXX, frequency is taking with mHz accuracy"""
        zeros_dict = {"kHz" : 6, "MHz" : 9, "GHz" : 12}
        number_of_zeros = zeros_dict[decade]
        freq = str(frequency)
    
        if '.' in freq:
           freq += (number_of_zeros - len(freq.split(".")[1])) * "0"
           freq = freq.replace(".", "")
           freq = (13-len(freq)) * "0" + freq
        else:
           freq += number_of_zeros * "0"
           freq += (13-len(freq)) * "0"

        self.active_port.write(bytes("FREQ:" + freq, "ascii"))
       
    def setPower(self, power):
        """To set power user need to send ascii string in format PWR:XXXX
        power can be in range -80 dBm to 10 dBm, string need to be send without
        dot sign"""
        power_to_send = str(power).replace(".", "")
        if float(power) > 0.0:
           if len(power_to_send) < 4 :
               power_to_send = '+' + (4-len(power_to_send)) * "0" + power_to_send
           else :
              power_to_send = '+' + power_to_send
        elif float(power) < 0.0:
            if len(power_to_send) < 5:
                power_to_send = power_to_send[1:]
                power_to_send = '-' + (4-len(power_to_send))*"0" + power_to_send
        else :
           power_to_send = "+0000"
           
        self.active_port.write(bytes("PWR:" + power_to_send, "ascii"))
     
           
    def setPhase(self, phase):
        phase_to_send = str(phase)
        if '.' in phase:
            phase_to_send = phase.replace('.', "")
            phase_to_send = (4-len(phase_to_send)) * "0" + phase_to_send
        else:
            phase_to_send = (3-len(phase_to_send)) * "0" + phase_to_send + "0"

        self.active_port.write(bytes("PHS:" + phase_to_send, "ascii"))    

    def setActiveChannel(self, channel):
        self.active_port.write(bytes("CH:" + str(channel), "ascii"))

    def __del__(self) :
        if self.isCreated == True :
           self.active_port.close()

def list_ports():
   operating_system = platform.system()
   if(operating_system == "Windows"):
      ports = ["COM" + str(i+1) for i in range(256)]
   else:
       ports = glob.glob("/dev/tty[A-Za-z]*")
   available_ports = []
   for port in ports :
      try:
         s = serial.Serial(port)
         s.close()
         available_ports.append(port)
      except (OSError, serial.SerialException):
         pass
   return available_ports        
