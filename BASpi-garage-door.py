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
        self.name = 'BAS Garage Doors'
        self.ipaddress = None
        self.debug_enable = 'False'
        self.poly.onConfig(self.process_config)
        

    def start(self):
        serverdata = self.poly.get_server_data()
        LOGGER.info('Starting BASpi Garage Doors')
        self.check_params()
        self.discover()
        self.poly.add_custom_config_docs("<b>And this is some custom config data</b>")
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']
            
    def shortPoll(self):
        self.discover()
    
    def longPoll(self):
        self.discover()

    def query(self,command=None):
        self.check_params()
        for node in self.nodes:
            self.nodes[node].reportDrivers()
    class bc:
        def __init__(self, sIpAddress):  #sIpAddress
            self.bc = Device()
                
    def get_request(self, url):
        try:
            r = requests.get(url, auth=HTTPBasicAuth('http://' + self.ipaddress + '/cgi-bin/xml-cgi'))
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
        self.removeNoticesAll()
        default_door_ip = None
        st = None

        if 'door_ip' in self.polyConfig['customParams']:
            self.ipaddress = self.polyConfig['customParams']['door_ip']
        else:
            self.ipaddress = default_door_ip
            LOGGER.error(
                'check_params: BASpi Garage Doors IP not defined in customParams, please add it.  Using {}'.format(self.ipaddress))
            st = False        
                
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']

        # Make sure they are in the params 'password': self.password, 'user': self.user,
        self.addCustomParam({'door_ip': self.ipaddress, 'debug_enable': self.debug_enable})
        

        # Add a notice if they need to change the user/password from the defaultself.user == default_user or self.password == default_password or .
        if self.ipaddress == default_door_ip:
            self.addNotice('Please set proper, BASpi6u6r_One IP as key = door_ip the BASpi IP Address for Value'
                           'in configuration page, and restart this nodeserver')
            st = False
                           
        if st == True:
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
        ]



class BaspiGarage_one(polyinterface.Node):
    def __init__(self, controller, primary, address, name, ipaddress, bc):
        super(BaspiGarage_one, self).__init__(controller, primary, address, name)
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

            # Input Conversion
            if input_one is not None:
                sumss_count1 = int(input_one)//1000
            if input_two is not None:
                sumss_count2 = int(input_two)//100
            if input_thr is not None:
                sumss_count3 = int(input_thr)//100
            if input_for is not None:
                sumss_count4 = int(input_for)//100
            if input_fiv is not None:
                sumss_count5 = int(input_six)//100
            if input_six is not None:
                sumss_count6 = int(input_fiv)//100

            LOGGER.info(sumss_count1)
            LOGGER.info(sumss_count2)
            LOGGER.info(sumss_count3)
            LOGGER.info(sumss_count4)
            LOGGER.info(sumss_count5)
            LOGGER.info(sumss_count6)
           
            # Binary/Digital Outputs
            output_one = (self.bc.binaryOutput(1))
            output_two = (self.bc.binaryOutput(2))
            output_tre = (self.bc.binaryOutput(3))
            output_for = (self.bc.binaryOutput(4))
            output_fiv = (self.bc.binaryOutput(5))
            output_six = (self.bc.binaryOutput(6))
                        
            self.setDriver('GV0', sumss_count1, force=True)
            self.setDriver('GV1', sumss_count2, force=True)
            self.setDriver('GV2', sumss_count3, force=True)
            self.setDriver('GV3', sumss_count4, force=True)
            self.setDriver('GV4', sumss_count5, force=True)
            self.setDriver('GV5', sumss_count6, force=True)

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
            LOGGER.info('Output 1 Off')
            self.setDriver("GV6", 0)
            self.delay1(self)
    
    def delay1(self, command):
        time.sleep(15)
        self.doorStat1(self)
        #if self.bc.universalInput(1) == 0:
        #    self.reportDrivers()
   
    # Door-1 Status
    def doorStat1(self, command):
        if 'sumss_count1' == 12:
            self.setDriver("GV0", '12', report=True, force=True)
        elif 'sumss_count1' == 5:
              self.setDriver("GV0", '5', report=True, force=True)
        else:
            if self.bc.universalInput(1) == 0:
                self.setDriver("GV0", '0', report=True, force=True)
        
    
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
        #if self.bc.universalInput(2) == 0:
        #    self.doorStat2(self)
    
    # Door-2 Status
    def doorStat2(self, command):
        if 'sumss_count2' == 12:
            self.setDriver("GV1", '12', report=True, force=True)
        elif 'sumss_count2' == 5:
              self.setDriver("GV1", '5', report=True, force=True)
        else:
            if self.bc.universalInput(2) == 0:
                self.setDriver("GV1", '0', report=True, force=True)
      
    
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
        elif 'sumss_count3' == 5:
              self.setDriver("GV2", '5', report=True, force=True)
        else:
            if self.bc.universalInput(3) == 0:
                self.setDriver("GV2", '0', report=True, force=True)
       

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
        #if self.bc.universalInput(4) == 0:
        #    self.doorStat4(self)
    
    # Door-4 Status
    def doorStat4(self, command):
        if 'sumss_count4' == 12:
            self.setDriver("GV3", '12', report=True, force=True)
        elif 'sumss_count4' == 5:
              self.setDriver("GV3", '5', report=True, force=True)
        else:
            if self.bc.universalInput(4) == 0:
                self.setDriver("GV3", '0', report=True, force=True)
        

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
            self.doorStat3(self)
            LOGGER.info('Output 5 Off')
            self.delay5(self)
    
    def delay5(self, command):
        time.sleep(15)
        self.doorStat5(self)
        #if self.bc.universalInput(5) == 0:
        #    self.doorStat5(self)
    
    # Door-5 Status
    def doorStat5(self, command):
        if 'sumss_count5' == 12:
            self.setDriver("GV4", '12', report=True, force=True)
        elif 'sumss_count5' == 5:
             self.setDriver("GV4", '5', report=True, force=True)
        else:
            if self.bc.universalInput(5) == 0:
                self.setDriver("GV4", '0', report=True, force=True)
       
            
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
        #if self.bc.universalInput(6) == 0:
        #    self.doorStat6(self)
    
    # Door-6 Status
    def doorStat6(self, command):
        if 'sumss_count6' == 12:
            self.setDriver("GV5", '12', report=True, force=True)
        elif 'sumss_count6' == 5:
              self.setDriver("GV5", '5', report=True, force=True)
        else:
            if self.bc.universalInput(6) == 0:
                self.setDriver("GV5", '0', report=True, force=True)
        
     
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