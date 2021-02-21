#!/usr/bin/env python
"""
Original NodeServer template for Polyglot v2 written in Python2/3
by Einstein.42 (James Milne) milne.james@gmail.com
BasGarageDoors by Steve Bailey sjpbailey1961@gmail.com
"""
try:
    import polyinterface
except ImportError:
    import pgc_interface as polyinterface
import sys
from nodes import GarageDoorsController
from nodes import GarageDoorsNodes

LOGGER = polyinterface.LOGGER

if __name__ == "__main__":
    try:
        polyglot = polyinterface.Interface('Garage_Doors')
        polyglot.start()
        control = GarageDoorsController(polyglot)
        control.runForever()
    except (KeyboardInterrupt, SystemExit):
        LOGGER.warning("Received interrupt or exit...")
        """
                Catch SIGTERM or Control-C and exit cleanly.
        """
        polyglot.stop()
    except Exception as err:
        LOGGER.error('Excption: {0}'.format(err), exc_info=True)
    sys.exit(0)
