#!/usr/bin/env python
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
import time
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from enum import Enum
import ipaddress
import bascontrolns
from bascontrolns import Device, Platform

LOGGER = polyinterface.LOGGER

class Controller(polyinterface.Controller):
    def __init__(self, polyglot):
        super(Controller, self).__init__(polyglot)
        self.name = 'BASpi Garage Doors'
        self.ipaddress = None
        self.ipaddress2 = None
        self.debug_enable = 'False'
        self.poly.onConfig(self.process_config)
        

    def start(self):
        serverdata = self.poly.get_server_data()
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']
        if self.check_params():
            self.ipaddress =  self.bc('sIpAddress')
                     
        LOGGER.info('Starting BASpi Garage Doors')
        # Remove all existing notices
        self.removeNoticesAll()
        self.check_params()
        
        
    def shortPoll(self):
        self.discover()
              

    def longPoll(self):
        self.discover()

    def query(self,command=None):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()
    class bc:
        def __init__(self):  #sIpAddress
            self.bc = Device()
                
    def get_request(self, url):
        try:
            r = requests.get(url, auth=HTTPBasicAuth('http://' + self.ipaddress, self.ipaddress2 + '/cgi-bin/xml-cgi')) #
            if r.status_code == requests.codes.ok:
                if self.debug_enable == 'True' or self.debug_enable == 'true':
                    print(r.content)

                return r.content
            else:
                LOGGER.error("BASpi Garage Door Network.get_request:  " + r.content)
                return None

        except requests.exceptions.RequestException as e:
            LOGGER.error("Error: " + str(e))        

    def discover(self, *args, **kwargs):
        ### Garage Doors 1-3 ###
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
            self.addNode(BaspiGarage_one(self, self.address, 'baspidoor1_id', 'Garage Doors 1-6', self.ipaddress, self.bc))
            self.setDriver('GV19', 1)    
     
        ### Garage Doors 4-6 ###
        if self.ipaddress2 is not None:
            self.bc2 = Device(self.ipaddress2)
            self.addNode(BaspiGarage_two(self, self.address, 'baspidoor2_id', 'Garage Doors 7-12', self.ipaddress2, self.bc2))
            self.setDriver('GV20', 1)
        

    def delete(self):
        LOGGER.info('Removing BASpi Garage Doors')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config));
        LOGGER.info("process_config: Exit");

    def check_params(self):
        st = True
        self.removeNoticesAll()
        default_door1_6_ip = None
        default_door7_12_ip = None
        st1 = None

        if 'door1_6_ip' and 'door7_12_ip' in self.polyConfig['customParams']:
            self.ipaddress = self.polyConfig['customParams']['door1_6_ip']
            self.ipaddress2 = self.polyConfig['customParams']['door7_12_ip']
        else:
            self.ipaddress = default_door1_6_ip
            self.ipaddress2 = default_door7_12_ip
            LOGGER.error(
                'check_params: BASpi Garage Doors IP not defined in customParams, please add it.  Using {}'.format(self.ipaddress))
            st = False        
                
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']

        # Make sure they are in the params 'password': self.password, 'user': self.user,
        self.addCustomParam({'door1_6_ip': self.ipaddress, 'debug_enable': self.debug_enable})
        self.addCustomParam({'door7_12_ip': self.ipaddress2, 'debug_enable': self.debug_enable})

        # Add a notice if they need to change the user/password from the defaultself.user == default_user or self.password == default_password or .
        if self.ipaddress == default_door1_6_ip:
            self.addNotice('Please set proper, BASpi6u6r_One IP as key = door1_6_ip also if desired key = door7_12_ip the BASpi IP Address for Value'
                           'in configuration page, and restart this nodeserver')
            st = False
        
        if self.ipaddress2 == default_door7_12_ip:
            self.addNotice('Please set proper, BASpi6u6r IP as key = door7_12_ip and the BASpi IP Address for Value'
                           'in configuration page, and restart this nodeserver')
            st1 = False               
            
        if st1 == True:
            return True
        else:
            return False

    
    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st
    
    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV19', 'value': 0, 'uom': 2},
        {'driver': 'GV20', 'value': 0, 'uom': 2},
    ]



class BaspiGarage_one(polyinterface.Node):
    def __init__(self, controller, primary, address, name, ipaddress, bc):
        super(BaspiGarage_one, self).__init__(controller, primary, address, name)
        self.ipaddress = (str(ipaddress).upper()) #Device(str(ipaddress).upper())
        self.bc = bc
        
    def start(self):
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
                        
            ### BASpi One ###
            if self.bc.ePlatform == Platform.BASC_NONE:
                LOGGER.info('Unable to connect to Garage Doo 1-6')
                LOGGER.info('ipaddress')
            if self.bc.ePlatform == Platform.BASC_PI:
                LOGGER.info('connected to Garage Door 1-6')
                self.setDriver('ST', 1)    

            LOGGER.info('\t' + str(self.bc.uiQty) + ' Universal inputs in this Doors 1-6')
            LOGGER.info('\t' + str(self.bc.boQty) + ' Binary outputs in this Doors 1-6')
            LOGGER.info('\t' + str(self.bc.biQty) + ' Binary inputs in This Doors 1-6')
            LOGGER.info('\t' + str(self.bc.aoQty) + ' Analog outputs In This Doors 1-6')
            
            ### Universal Inputs ###
            input_one = self.bc.universalInput(1)
            input_two = self.bc.universalInput(2)
            input_thr = self.bc.universalInput(3)
            input_for = self.bc.universalInput(4)
            input_fiv = self.bc.universalInput(5)
            input_six = self.bc.universalInput(6)

            # Binary/Digital Outputs
            output_one = (self.bc.binaryOutput(1))
            output_two = (self.bc.binaryOutput(2))
            output_tre = (self.bc.binaryOutput(3))
            output_for = (self.bc.binaryOutput(4))
            output_fiv = (self.bc.binaryOutput(5))
            output_six = (self.bc.binaryOutput(6))
                        
            self.setDriver('GV0', input_one, force=True)
            self.setDriver('GV1', input_two, force=True)
            self.setDriver('GV2', input_thr, force=True)
            self.setDriver('GV3', input_for, force=True)
            self.setDriver('GV4', input_fiv, force=True)
            self.setDriver('GV5', input_six, force=True)

            # Binary/Digital Outputs
            self.setDriver('GV6', output_one, force=True)
            self.setDriver('GV7', output_two, force=True)
            self.setDriver('GV8', output_tre, force=True)
            self.setDriver('GV9', output_for, force=True)
            self.setDriver('GV10', output_fiv, force=True)
            self.setDriver('GV11', output_six, force=True)
           
            LOGGER.info(self.bc.universalInput(1))
            LOGGER.info(self.bc.universalInput(2))
            LOGGER.info(self.bc.universalInput(3))
            LOGGER.info(self.bc.universalInput(4))
            LOGGER.info(self.bc.universalInput(5))
            LOGGER.info(self.bc.universalInput(6))
       
    # Output Door-1
    def setOn1(self, command=None):
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
    # Door-1 Status
    def doorStat1(self, command=None):
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV0", 0)
        if self.bc.universalInput(1) >= 155-161: 
            self.setDriver("GV0", 155)

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
    # Door-2 Status
    def doorStat2(self, command=None):
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV1", 0)
        if self.bc.universalInput(1) >= 155-161: 
            self.setDriver("GV1", 155)         

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
    # Door-3 Status
    def doorStat3(self, command=None):
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV2", 0)
        if self.bc.universalInput(1) >= 155-161: 
            self.setDriver("GV2", 155) 

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
    # Door-4 Status
    def doorStat4(self, command=None):
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV3", 0)
        if self.bc.universalInput(1) >= 155-161: 
            self.setDriver("GV3", 155)         

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
    # Door-5 Status
    def doorStat5(self, command=None):
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV4", 0)
        if self.bc.universalInput(1) >= 155-161: 
            self.setDriver("GV4", 155)         

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
    # Door-6 Status
    def doorStat6(self, command=None):
        if self.bc.universalInput(1) == 0:
            self.setDriver("GV5", 0)
        if self.bc.universalInput(1) >= 155-161: 
            self.setDriver("GV5", 155)     
     
    def query(self,command=None):
        self.reportDrivers()

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


class BaspiGarage_two(polyinterface.Node):
    def __init__(self, controller, primary, address2, name, ipaddress2, bc2):
        super(BaspiGarage_two, self).__init__(controller, primary, address2, name)
        self.ipaddress2 = (str(ipaddress2).upper()) #Device(str(ipaddress).upper())
        self.bc2 = bc2
        

    def start(self):
        if self.ipaddress2 is not None:
            self.bc2 = Device(self.ipaddress2)
                        
            ### BASpi One ###
            if self.bc2.ePlatform == Platform.BASC_NONE:
                LOGGER.info('Unable to connect to Garage Door 7-12')
                LOGGER.info('ipaddress2')
            if self.bc2.ePlatform == Platform.BASC_PI:
                LOGGER.info('connected to Garage Door 7-12')
                self.setDriver('ST', 1)    

            LOGGER.info('\t' + str(self.bc2.uiQty) + ' Universal inputs in this Doors 7-12')
            LOGGER.info('\t' + str(self.bc2.boQty) + ' Binary outputs in this Doors 7-12')
            LOGGER.info('\t' + str(self.bc2.biQty) + ' Binary inputs in This Doors 7-12')
            LOGGER.info('\t' + str(self.bc2.aoQty) + ' Analog outputs In This Doors 7-12')
            
            ### Universal Inputs ###
            input_one = self.bc2.universalInput(1)
            input_two = self.bc2.universalInput(2)
            input_thr = self.bc2.universalInput(3)
            input_for = self.bc2.universalInput(4)
            input_fiv = self.bc2.universalInput(5)
            input_six = self.bc2.universalInput(6)

            # Binary/Digital Outputs
            output_one = (self.bc2.binaryOutput(1))
            output_two = (self.bc2.binaryOutput(2))
            output_tre = (self.bc2.binaryOutput(3))
            output_for = (self.bc2.binaryOutput(4))
            output_fiv = (self.bc2.binaryOutput(5))
            output_six = (self.bc2.binaryOutput(6))
                        
            self.setDriver('GV0', input_one, force=True)
            self.setDriver('GV1', input_two, force=True)
            self.setDriver('GV2', input_thr, force=True)
            self.setDriver('GV3', input_for, force=True)
            self.setDriver('GV4', input_fiv, force=True)
            self.setDriver('GV5', input_six, force=True)

            # Binary/Digital Outputs
            self.setDriver('GV6', output_one, force=True)
            self.setDriver('GV7', output_two, force=True)
            self.setDriver('GV8', output_tre, force=True)
            self.setDriver('GV9', output_for, force=True)
            self.setDriver('GV10', output_fiv, force=True)
            self.setDriver('GV11', output_six, force=True)
           
            LOGGER.info(self.bc2.universalInput(1))
            LOGGER.info(self.bc2.universalInput(2))
            LOGGER.info(self.bc2.universalInput(3))
            LOGGER.info(self.bc2.universalInput(4))
            LOGGER.info(self.bc2.universalInput(5))
            LOGGER.info(self.bc2.universalInput(6))
    
    # Output Door-1
    def setOn1(self, command=None):
        if self.bc2.binaryOutput(1) != 1:
            self.bc2.binaryOutput(1, 1)
            self.setDriver("GV6", 1)
            self.setDriver("GV0", 255) 
            LOGGER.info('Output 1 On')   
            time.sleep(2)
        if self.bc2.binaryOutput(1) != 0:    
            self.bc2.binaryOutput(1, 0)
            self.setDriver("GV6", 0)
            LOGGER.info('Output 1 Off')
    # Door-1 Status
    def doorStat1(self, command=None):
        if self.bc2.universalInput(1) == 0:
            self.setDriver("GV1", 0)
        if self.bc2.universalInput(1) >= 155-161: 
            self.setDriver("GV1", 155)         
        
    # Output Door-2
    def setOn2(self, command):
        if self.bc2.binaryOutput(2) != 1:
            self.bc2.binaryOutput(2, 1)
            self.setDriver("GV7", 1) 
            self.setDriver("GV1", 255)
            LOGGER.info('Output 2 On')
            time.sleep(2)
        if self.bc2.binaryOutput(2) != 0:        
            self.bc2.binaryOutput(2, 0)
            self.setDriver("GV7", 0) 
            LOGGER.info('Output 2 Off')
    # Door-2 Status
    def doorStat2(self, command=None):
        if self.bc2.universalInput(1) == 0:
            self.setDriver("GV1", 0)
        if self.bc2.universalInput(1) >= 155-161: 
            self.setDriver("GV1", 155)         

    # Output Door-3
    def setOn3(self, command):
        if self.bc2.binaryOutput(3) != 1:
            self.bc2.binaryOutput(3, 1)
            self.setDriver("GV8", 1)
            self.setDriver("GV2", 255) 
            LOGGER.info('Output 3 On')
            time.sleep(2)
        if self.bc2.binaryOutput(3) != 0:     
            self.bc2.binaryOutput(3, 0)
            self.setDriver("GV8", 0) 
            LOGGER.info('Output 3 Off')
    # Door-3 Status
    def doorStat3(self, command=None):
        if self.bc2.universalInput(1) == 0:
            self.setDriver("GV2", 0)
        if self.bc2.universalInput(1) >= 155-161: 
            self.setDriver("GV2", 155) 

    # Output Door-4
    def setOn4(self, command):
        if self.bc2.binaryOutput(4) != 1:
            self.bc2.binaryOutput(4, 1)
            self.setDriver("GV9", 1)
            self.setDriver("GV3", 255) 
            LOGGER.info('Output 4 On')
            time.sleep(2)
        if self.bc2.binaryOutput(4) != 0:    
            self.bc2.binaryOutput(4, 0)
            self.setDriver("GV9", 0) 
            LOGGER.info('Output 4 Off')
    # Door-4 Status
    def doorStat4(self, command=None):
        if self.bc2.universalInput(1) == 0:
            self.setDriver("GV3", 0)
        if self.bc2.universalInput(1) >= 155-161: 
            self.setDriver("GV3", 155)         

    # Output Door-5
    def setOn5(self, command):
        if self.bc2.binaryOutput(5) != 1:
            self.bc2.binaryOutput(5,1)
            self.setDriver("GV10", 1)
            self.setDriver("GV4", 255) 
            LOGGER.info('Output 5 On')
            time.sleep(2)
        if self.bc2.binaryOutput(5) != 0:    
            self.bc2.binaryOutput(5,0)
            self.setDriver("GV10", 0) 
            LOGGER.info('Output 5 Off')
    # Door-5 Status
    def doorStat5(self, command=None):
        if self.bc2.universalInput(1) == 0:
            self.setDriver("GV4", 0)
        if self.bc2.universalInput(1) >= 155-161: 
            self.setDriver("GV4", 155)         

    # Output Door-6
    def setOn6(self, command):
        if self.bc2.binaryOutput(6) != 1:
            self.bc2.binaryOutput(6,1)
            self.setDriver("GV11", 1)
            self.setDriver("GV5", 255) 
            LOGGER.info('Output 6 On')
            time.sleep(2)
        if self.bc2.binaryOutput(6) != 0:    
            self.bc2.binaryOutput(6,0)
            self.setDriver("GV11", 0) 
            LOGGER.info('Output 6 Off')
    # Door-6 Status
    def doorStat6(self, command=None):
        if self.bc2.universalInput(1) == 0:
            self.setDriver("GV5", 0)
        if self.bc2.universalInput(1) >= 155-161: 
            self.setDriver("GV5", 155)
    
    def query(self,command=None):
        self.reportDrivers()

    "Hints See: https://github.com/UniversalDevicesInc/hints"
    hint = [1,2,3,4]
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
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
    
        
    id = "baspidoor2_id"
    
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

