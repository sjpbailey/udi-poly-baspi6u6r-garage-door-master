
"""
Get the polyinterface objects we need.  Currently Polyglot Cloud uses
a different Python module which doesn't have the new LOG_HANDLER functionality
"""
try:
    from polyinterface import Controller,LOG_HANDLER,LOGGER
except ImportError:
    from pgc_interface import Controller,LOGGER
import logging
import time
import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from enum import Enum
import ipaddress
import bascontrolns
from bascontrolns import Device, Platform
from nodes import GarageDoorsNodes


# IF you want a different log format than the current default
LOG_HANDLER.set_log_format('%(asctime)s %(threadName)-10s %(name)-18s %(levelname)-8s %(module)s:%(funcName)s: %(message)s')

class GarageDoorsController(Controller):
    
    def __init__(self, polyglot):
        super(GarageDoorsController, self).__init__(polyglot)
        self.name = 'BASpi Garage Doors'
        self.hb = 0
        self.Device = Device
        # This can be used to call your function everytime the config changes
        # But currently it is called many times, so not using.
        #self.poly.onConfig(self.process_config)

    def start(self):
        serverdata = self.poly.get_server_data(check_profile=True)
        #serverdata['version'] = "testing"
        LOGGER.info('Started BASpi Garage Doors 1-6 NodeServer {}'.format(serverdata['version']))
        # Show values on startup if desired.
        LOGGER.debug('ST=%s',self.getDriver('ST'))
        self.setDriver('ST', 1)
        self.heartbeat(0)
        self.check_params()
        self.set_debug_level(self.getDriver('GV1'))
        self.discover()
        self.poly.add_custom_config_docs("<b>This is some custom config docs data</b>")

    def shortPoll(self):
        LOGGER.debug('shortPoll')
        for node in self.nodes:
            if node != self.address:
                self.nodes[node].shortPoll()

    def longPoll(self):
        LOGGER.debug('longPoll')
        self.heartbeat()

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
        ### Garage Doors 1-6 ###
        if self.ipaddress is not None:
            self.bc = Device(self.ipaddress)
        self.addNode(GarageDoorsNodes(self, self.address, 'baspidoor1_id', 'Garage Doors 1-6', self.ipaddress, self.bc))
                                    
    def delete(self):
        LOGGER.info('Removing Baspi Garage Doors NodeServer')

    def stop(self):
        LOGGER.debug('NodeServer stopped.')

    def process_config(self, config):
        # this seems to get called twice for every change, why?
        # What does config represent?
        LOGGER.info("process_config: Enter config={}".format(config))
        LOGGER.info("process_config: Exit")

    def heartbeat(self,init=False):
        LOGGER.debug('heartbeat: init={}'.format(init))
        if init is not False:
            self.hb = init
        LOGGER.debug('heartbeat: hb={}'.format(self.hb))
        if self.hb == 0:
            self.reportCmd("DON",2)
            self.hb = 1
        else:
            self.reportCmd("DOF",2)
            self.hb = 0

    def set_module_logs(self,level):
        logging.getLogger('urllib3').setLevel(level)

    def set_debug_level(self,level):
        LOGGER.debug('set_debug_level: {}'.format(level))
        if level is None:
            level = 0
        level = int(level)
        if level == 0:
            level = 30
        LOGGER.info('set_debug_level: Set GV1 to {}'.format(level))
        self.setDriver('GV1', level)
        # 0=All 10=Debug are the same because 0 (NOTSET) doesn't show everything.
        if level <= 10:
            LOGGER.setLevel(logging.DEBUG)
        elif level == 20:
            LOGGER.setLevel(logging.INFO)
        elif level == 30:
            LOGGER.setLevel(logging.WARNING)
        elif level == 40:
            LOGGER.setLevel(logging.ERROR)
        elif level == 50:
            LOGGER.setLevel(logging.CRITICAL)
        else:
            LOGGER.debug("set_debug_level: Unknown level {}".format(level))
        # this is the best way to control logging for modules, so you can
        # still see warnings and errors
        #if level < 10:
        #    self.set_module_logs(logging.DEBUG)
        #else:
        #    # Just warnigns for the modules unless in module debug mode
        #    self.set_module_logs(logging.WARNING)
        # Or you can do this and you will never see mention of module logging
        if level < 10:
            LOG_HANDLER.set_basic_config(True,logging.DEBUG)
        else:
            # This is the polyinterface default
            LOG_HANDLER.set_basic_config(True,logging.WARNING)

    def check_params(self):
        self.removeNoticesAll()
        default_door1_6_ip = None
        st = None

        if 'door1_6_ip' in self.polyConfig['customParams']:
            self.ipaddress = self.polyConfig['customParams']['door1_6_ip']
        else:
            self.ipaddress = default_door1_6_ip
            LOGGER.error(
                'check_params: BASpi Garage Doors IP not defined in customParams, please add it.  Using {}'.format(self.ipaddress))
            st = False        
                
        if 'debug_enable' in self.polyConfig['customParams']:
            self.debug_enable = self.polyConfig['customParams']['debug_enable']

        # Always overwrite this, it's just an example...
        self.addCustomParam({'door1_6_ip': self.ipaddress})

        # Add a notice if they need to change the user/password from the default.
        if self.ipaddress == default_door1_6_ip:
            # This doesn't pass a key to test the old way.
            self.addNotice('Please set proper, BASpi6u6r_One IP as key = door1_6_ip the BASpi IP Address for Value'
                           'in configuration page, and restart this nodeserver')
            st = False
        if st == True:
            return True    
        else:
            return False

    def remove_notice_test(self,command):
        LOGGER.info('remove_notice_test: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNotice('test')

    def remove_notices_all(self,command):
        LOGGER.info('remove_notices_all: notices={}'.format(self.poly.config['notices']))
        # Remove all existing notices
        self.removeNoticesAll()

    def update_profile(self,command):
        LOGGER.info('update_profile:')
        st = self.poly.installprofile()
        return st

    def cmd_set_debug_mode(self,command):
        val = int(command.get('value'))
        LOGGER.debug("cmd_set_debug_mode: {}".format(val))
        self.set_debug_level(val)

    """
    Optional.
    Since the controller is the parent node in ISY, it will actual show up as a node.
    So it needs to know the drivers and what id it will use. The drivers are
    the defaults in the parent Class, so you don't need them unless you want to add to
    them. The ST and GV1 variables are for reporting status through Polyglot to ISY,
    DO NOT remove them. UOM 2 is boolean.
    The id must match the nodeDef id="controller"
    In the nodedefs.xml
    """
    id = 'controller'
    commands = {
        'QUERY': query,
        'DISCOVER': discover,
        'UPDATE_PROFILE': update_profile,
        'REMOVE_NOTICES_ALL': remove_notices_all,
        'REMOVE_NOTICE_TEST': remove_notice_test,
        'SET_DM': cmd_set_debug_mode,
    }
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 10, 'uom': 25}, # Debug (Log) Mode, default=30=Warning
    ]

#sjb/gtb 1/4/2021