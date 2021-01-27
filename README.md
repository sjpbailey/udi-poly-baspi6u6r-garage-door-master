# Universal Devices BASpi Garage Doors Controller

## Based on the Contemporary Controls BASpi6U6R Device

![BASpi 6U6R Network Poly](https://github.com/sjpbailey/udi-poly-baspi6u6r-garage-door-master/blob/71d20be7496f19246ab4da70eaf8fd1e00d26c0c/Images%2FController_garage_doors.png)

* For up to Six Garage Doors on One BASpi6U6R Bacnet Programmable Device.

* Doors 1-6

![BASpi 6U6R One](https://github.com/sjpbailey/udi-poly-baspi6u6r-garage-door-master/blob/71d20be7496f19246ab4da70eaf8fd1e00d26c0c/Images%2FClass_nodes_garage_door.png)

## BASpi-SYS6U6R DIY BacNet Control Device by Contemporary Controls

* Main
* It utilizing the Contemporary Controls BASpi SYS6U6R control Module.
Please Visit these links for information & configuration of this Device.

[Contemporary Controls BASpi DIY](https://www.ccontrols.com/basautomation/baspi.php)

* BASpi 6U6R Controller
[Contemporary Controls BASpi 6U6R](https://www.ccontrols.com/pdf/ds/BASPI-datasheet.pdf)
* BASpi 6U6R Installation
[Contemporary Controls BASpi 6U6R Install](https://www.ccontrols.com/pdf/BASpi-hardware-install-guide.pdf)
* BASpi 6U4R2A Controller
[Contemporary Controls BASpi 6U4R2A](https://www.ccontrols.com/pdf/ds/BASPI-AO2-datasheet.pdf)
* BASpi 6U4R2A Installation
[Contemporary Controls BASpi 6U4R2A Install](https://www.ccontrols.com/pdf/TD180600.pdf)
* BASpi Controller Configuration
[Contemporary Controls BASpi Configuration Quick Start](https://www.ccontrols.com/pdf/is/BASPI-QSGuide.pdf)

### Garage Doors and Future Builds

* The purpose of this Polyglot Node Server is to open close and stop Garage Doors for up to 6 Doors. This is custom control for general Home automation for control operations.

* This Network series will include in the near future custom home control for Irrigation, Pool Control, Well Pump Control, General HVAC control, VVT, Boiler, Chiller along with any custom control you create utilizing the released bascontrolns module.

[bascontrolns](https://pypi.org/project/bascontrolns/)

#### Need to add

* Need to some how add a multiple pulldown menu for the Universal Inputs. The universal inputs have a large list of configurable UOM's 'unit of measure' of their own.
Please see configuration quick start link above. On page two, 2 it shows the GUI for the device there you can pick on each universal input to configure its type, a separate UOM.
* This controller sits on a Raspberry Pi. You can easily add it to your ISY after you configure its ipaddress.

* Please see the YouTube video below, you have to configure the BASpi6U6R devices Inputs for Resistance, Type & COV (change of value increment, this keeps the transmitted resistor values from bouncing).
* A 220 ohm resistor is added to the open switch and a 560 ohm resistor to the close switch, both on one leg of the switch to the wire so when the switch is closed it sees the resistance.

[Universal Input Configuration for the Garage Door Node Server](https://youtu.be/I3tSfYk8ti8)

[Resistor Installation](https://youtu.be/5409LGvDWNY)

![Future Adds](https://github.com/sjpbailey/udi-poly-baspi6u6r-garage-door-master/blob/master/Images%2Fshot_3.png)

* Requirments
* Python 3.7.7
* bascontrolns==0.0.3
* polyinterface==2.1.0
* requests==2.25.0

* Supported Nodes
  * Six 6 Universal Inputs
  * Six 6 Binary Outputs
  
##### Configuration

###### Defaults

* Default Short Poll:  Every 60 seconds
* Default Long Poll: Every 4 minutes (heartbeat)

###### User Provided

* Enter your IP address for your BASpi-SYS6U6R controller,
* key = door1_6_ip Value = Enter Your BASpi IP Address.

* Save and restart the NodeServer
* sjb & gtb Dec 2020
