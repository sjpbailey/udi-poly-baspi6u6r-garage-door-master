
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import threading 
from threading import Event
import urllib3
from bascontrolns import Device, Platform

LOGGER = polyinterface.LOGGER

class GarageDoorsNodes(polyinterface.Node):
    def __init__(self, controller, primary, address, name, ipaddress, bc):
        super(GarageDoorsNodes, self).__init__(controller, primary, address, name)
        self.ipaddress = (str(ipaddress).upper()) #Device(str(ipaddress).upper())
        self.bc = bc
        sumss_count1=None

    def start(self):
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
                        
        ### BASpi One ###
        if self.bc.ePlatform == Platform.BASC_NONE:
            LOGGER.info('Unable to connect to Garage Doo 1-6')
            LOGGER.info('ipaddress')
        if self.bc.ePlatform == Platform.BASC_PI:
            LOGGER.info('connected to Garage Door 1-6')
        if self.bc.ePlatform == Platform.BASC_ED:
            LOGGER.info('connected to BASpi-Edge Module ONE')
            self.setDriver('ST', 1)    

        LOGGER.info('\t' + str(self.bc.uiQty) + ' Universal inputs in this Doors 1-6')
        LOGGER.info('\t' + str(self.bc.boQty) + ' Binary outputs in this Doors 1-6')
        LOGGER.info('\t' + str(self.bc.biQty) + ' Binary inputs in This Doors 1-6')
        LOGGER.info('\t' + str(self.bc.aoQty) + ' Analog outputs In This Doors 1-6')
        
        LOGGER.info(self.bc.universalInput(1))
        LOGGER.info(self.bc.universalInput(2))
        LOGGER.info(self.bc.universalInput(3))
        LOGGER.info(self.bc.universalInput(4))
        LOGGER.info(self.bc.universalInput(5))
        LOGGER.info(self.bc.universalInput(6))
            
        # Binary/Digital Outputs
        output_one = (self.bc.binaryOutput(1))
        output_two = (self.bc.binaryOutput(2))
        output_tre = (self.bc.binaryOutput(3))
        output_for = (self.bc.binaryOutput(4))
        output_fiv = (self.bc.binaryOutput(5))
        output_six = (self.bc.binaryOutput(6))

        # Binary/Digital Outputs
        self.setDriver('GV6', output_one, force=True)
        self.setDriver('GV7', output_two, force=True)
        self.setDriver('GV8', output_tre, force=True)
        self.setDriver('GV9', output_for, force=True)
        self.setDriver('GV10', output_fiv, force=True)
        self.setDriver('GV11', output_six, force=True)



        
        ### Universal Inputs Also Conversion ###
        input_one = self.bc.universalInput(1)
        sumss_count1 = 0
        if input_one is not None:
            sumss_count1 = int(float(input_one))//1000
            self.setDriver('GV0', sumss_count1, force=True)
            return sumss_count1
        
        
        input_two = self.bc.universalInput(2)
        sumss_count2 = 0    
        if input_two is not None:
            sumss_count2 = int(float(input_two))//1000
            self.setDriver('GV1', sumss_count2, force=True)
            return sumss_count2
        
     
        input_thr = self.bc.universalInput(3)
        sumss_count3 = 0
        if input_thr is not None:
            sumss_count3 = int(float(input_thr))//1000
            self.setDriver('GV2', sumss_count3, force=True)
            return sumss_count3
       
            
        input_for = self.bc.universalInput(4)
        sumss_count4 = 0    
        if input_for is not None:
            sumss_count4 = int(float(input_for))//1000
            self.setDriver('GV3', sumss_count4, force=True)
            return sumss_count4
        

        input_fiv = self.bc.universalInput(5)
        sumss_count5 = 0
        if input_fiv is not None:
            sumss_count5 = int(float(input_fiv))//1000
            self.setDriver('GV4', sumss_count5, force=True)
            return sumss_count5
      

        input_six = self.bc.universalInput(6)
        sumss_count6 = 0
        if input_six is not None:
            sumss_count6 = int(float(input_six))//1000
            self.setDriver('GV5', sumss_count6, force=True)
            return sumss_count6           
       

    # Input Output Control       
    # Output Door-1
    def setOn1(self, command):
        if self.bc.binaryOutput(1) != 1:
            self.bc.binaryOutput(1, 1)
            self.setDriver("GV6", 1)
            self.setDriver("GV0", 255) 
            LOGGER.info('Output 1 On')   
            time.sleep(2)
        if self.bc.binaryOutput(1) != 0:    
            self.bc.binaryOutput(1, 0)
            self.setDriver("GV6", 0)
            LOGGER.info('Output 1 Off')
            self.delay1(self)
    
    def delay1(self, command):
        time.sleep(15)
        self.doorStat1(self)
        
    # Door-1 Status
    def doorStat1(self, command):
        if 'sumss_count1' == 12:
            self.setDriver("GV0", '12', report=True, force=True)
        if 'sumss_count1' == 5:
            self.setDriver("GV0", '5', report=True, force=True)
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV0", '0', report=True, force=True)
        LOGGER.info('Door 1 Operation Complete')
    
    # Output Door-2
    def setOn2(self, command):
        if self.bc.binaryOutput(2) != 1:
            self.bc.binaryOutput(2, 1)
            self.setDriver("GV7", 1) 
            self.setDriver("GV1", 255)
            LOGGER.info('Output 2 On')
            time.sleep(2)
        if self.bc.binaryOutput(2) != 0:        
            self.bc.binaryOutput(2, 0)
            self.setDriver("GV7", 0) 
            LOGGER.info('Output 2 Off')
            self.delay2(self)
    
    def delay2(self, command):
        time.sleep(15)
        self.doorStat2(self)
       
    # Door-2 Status
    def doorStat2(self, command):
        if 'sumss_count2' == 12:
            self.setDriver("GV1", '12', report=True, force=True)
        if 'sumss_count2' == 5:
            self.setDriver("GV1", '5', report=True, force=True)
        if self.bc.universalInput(2) == 0:
            self.setDriver("GV1", '0', report=True, force=True)
        LOGGER.info('Door 2 Operation Complete')
    
    # Output Door-3
    def setOn3(self, command):
        if self.bc.binaryOutput(3) != 1:
            self.bc.binaryOutput(3, 1)
            self.setDriver("GV8", 1)
            self.setDriver("GV2", 255) 
            LOGGER.info('Output 3 On')
            time.sleep(2)
        if self.bc.binaryOutput(3) != 0:     
            self.bc.binaryOutput(3, 0)
            self.setDriver("GV8", 0) 
            LOGGER.info('Output 3 Off')
            self.delay3(self)
    
    def delay3(self, command):
        time.sleep(15)
        self.doorStat3(self)
        #if self.bc.universalInput(3) == 0:
        #    self.reportDrivers()
    
    # Door-3 Status
    def doorStat3(self, command):
        if 'sumss_count3' == 12:
            self.setDriver("GV2", '12', report=True, force=True)
        if 'sumss_count3' == 5:
            self.setDriver("GV2", '5', report=True, force=True)
        if self.bc.universalInput(3) == 0:
            self.setDriver("GV2", '0', report=True, force=True)
        LOGGER.info('Door 3 Operation Complete')

    # Output Door-4
    def setOn4(self, command):
        if self.bc.binaryOutput(4) != 1:
            self.bc.binaryOutput(4, 1)
            self.setDriver("GV9", 1)
            self.setDriver("GV3", 255) 
            LOGGER.info('Output 4 On')
            time.sleep(2)
        if self.bc.binaryOutput(4) != 0:    
            self.bc.binaryOutput(4, 0)
            self.setDriver("GV9", 0)
            LOGGER.info('Output 4 Off')
            self.delay4(self)
    
    def delay4(self, command):
        time.sleep(15)
        self.doorStat4(self)
        
    # Door-4 Status
    def doorStat4(self, command):
        if 'sumss_count4' == 12:
            self.setDriver("GV3", '12', report=True, force=True)
        if 'sumss_count4' == 5:
            self.setDriver("GV3", '5', report=True, force=True)
        if self.bc.universalInput(4) == 0:
            self.setDriver("GV3", '0', report=True, force=True)
        LOGGER.info('Door 4 Operation Complete') 

    # Output Door-5
    def setOn5(self, command):
        if self.bc.binaryOutput(5) != 1:
            self.bc.binaryOutput(5,1)
            self.setDriver("GV10", 1)
            self.setDriver("GV4", 255) 
            LOGGER.info('Output 5 On')
            time.sleep(2)
        if self.bc.binaryOutput(5) != 0:    
            self.bc.binaryOutput(5,0)
            self.setDriver("GV10", 0) 
            LOGGER.info('Output 5 Off')
            self.delay5(self)
    
    def delay5(self, command):
        time.sleep(15)
        self.doorStat5(self)
        
    # Door-5 Status
    def doorStat5(self, command):
        if 'sumss_count5' == 12:
            self.setDriver("GV4", '12', report=True, force=True)
        if 'sumss_count5' == 5:
            self.setDriver("GV4", '5', report=True, force=True)
        if self.bc.universalInput(5) == 0:
            self.setDriver("GV4", '0', report=True, force=True)
        LOGGER.info('Door 5 Operation Complete')
            
    # Output Door-6
    def setOn6(self, command):
        if self.bc.binaryOutput(6) != 1:
            self.bc.binaryOutput(6,1)
            self.setDriver("GV11", 1)
            self.setDriver("GV5", 255) 
            LOGGER.info('Output 6 On')
            time.sleep(2)
        if self.bc.binaryOutput(6) != 0:    
            self.bc.binaryOutput(6,0)
            self.setDriver("GV11", 0)
            LOGGER.info('Output 6 Off')
            self.delay6(self)
    
    def delay6(self, command):
        time.sleep(15)
        self.doorStat6(self)
        
    # Door-6 Status
    def doorStat6(self, command):
        if 'sumss_count6' == 12:
            self.setDriver("GV5", '12', report=True, force=True)
        if 'sumss_count6' == 5:
            self.setDriver("GV5", '5', report=True, force=True)
        if self.bc.universalInput(6) == 0:
            self.setDriver("GV5", '0', report=True, force=True)
        LOGGER.info('Door 6 Operation Complete')

    def shortPoll(self):
        LOGGER.debug('shortPoll')
        
    def longPoll(self):
        LOGGER.debug('longPoll')    
     
    def query(self,command=None):
        self.reportDrivers()
        #self.check_params()
        #for node in self.nodes:
        #self.nodes[node].reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2},
        {'driver': 'GV0', 'value': 1, 'uom': 25},
        {'driver': 'GV1', 'value': 1, 'uom': 25},
        {'driver': 'GV2', 'value': 1, 'uom': 25},
        {'driver': 'GV3', 'value': 1, 'uom': 25},
        {'driver': 'GV4', 'value': 1, 'uom': 25},
        {'driver': 'GV5', 'value': 1, 'uom': 25},
        {'driver': 'GV6', 'value': 1, 'uom': 80},
        {'driver': 'GV7', 'value': 1, 'uom': 80},
        {'driver': 'GV8', 'value': 1, 'uom': 80},
        {'driver': 'GV9', 'value': 1, 'uom': 80},
        {'driver': 'GV10', 'value': 1, 'uom': 80},
        {'driver': 'GV11', 'value': 1, 'uom': 80},
        
        ]
    id = 'baspidoor1_id'
   
    commands = {
                    'BON1': setOn1,
                    'BON2': setOn2,
                    'BON3': setOn3,
                    'BON4': setOn4,
                    'BON5': setOn5,
                    'BON6': setOn6,
                    'QUERY': query,
                }



if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('BASPI_GARAGE')
        polyglot.start()
        control = Controller(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)

#copyright GTB & SJB Bailey 2020 Union Made