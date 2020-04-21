import serial
import sys
import platform
import glob

class GenSerialPort() :
    def __init__(self, port_name) :
       self.isCreated=False
       try :
          self.active_port=serial.Serial(port_name,115200,serial.EIGHTBITS)
          if not self.active_port.is_open :
             self.active_port.open()
          self.isCreated = True
       except(serial.SerialException):
          self.isCreated=False
           
    def isCreate(self) :
        return self.isCreated
    
    def setFrequency(self, frequency,decade):
       if decade == 'kHz' :
           zeros=6
       elif decade == 'MHz' :
           zeros=9
       elif decade == 'GHz' :
           zeros=12
       else:
           raise AttributeError    
           
       if '.' in str(frequency) :
          freq=str(frequency)
          freq=freq+(zeros+1-len(freq[freq.find("."):len(freq)]))*"0";
          freq=freq.replace(".","")
          freq=(13-len(freq))*"0"+freq
       else :
          freq=str(frequency)+zeros*"0"
          freq=(13-len(freq))*"0"+freq

       freq_msg="FREQ:"+freq
       self.active_port.write(bytes(freq_msg,'ascii'))
       
    def setPower(self, power):
       power_to_send=str(int(float(power)*100))
       power_to_send=power_to_send.replace(".","")
       if float(power) > 0.0 :
          if len(power_to_send) < 4 :
              power_to_send='+'+(4-len(power_to_send))*"0"+power_to_send
          else :
             power_to_send='+'+power_to_send
       elif float(power) < 0.0 :
           if len(power_to_send) < 5:
               power_to_send=power_to_send[1:len(power_to_send)]
               power_to_send='-'+(4-len(power_to_send))*"0"+power_to_send
       else :
          power_to_send="+0000"
           
       pwr_msg="PWR:"+power_to_send
       self.active_port.write(bytes(pwr_msg,"ascii"))
     
           
    def setPhase(self, phase):
        phase_to_send=str(phase)
        if '.' in phase :
            phase_to_send=phase.replace('.',"")
            phase_to_send=(4-len(phase_to_send))*"0"+phase_to_send
        else :
            phase_to_send=(3-len(phase_to_send))*"0"+phase_to_send+"0"

        phase_msg="PHS:"+phase_to_send 
        self.active_port.write(bytes(phase_msg,'ascii'))    
        #print(phase_msg)

    def setActiveChannel(self, channel):
        ch_msg="CH:"+str(channel)
        #print(ch_msg)
        self.active_port.write(bytes(ch_msg,'ascii'))

    def testPort(self):
        print("TEST")

    def __del__(self) :
        if self.isCreated == True :
           self.active_port.close()

def list_ports():
   operating_system=platform.system()
   if(operating_system=='Windows'):
      ports=['COM%s' % (i+1) for i in range(256)]
   else:
       ports=glob.glob('/dev/tty[A-Za-z]*')
   available_ports=[]
   for port in ports :
      try :
         s=serial.Serial(port)
         s.close()
         available_ports.append(port)
      except (OSError, serial.SerialException) :
         pass
   return available_ports        
