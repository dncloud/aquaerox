aquaerox
=========
A library and web service for accessing Aquaero fan controllers by Aqua Computer GmbH & Co. KG, written in Python.

Install
-------
Depends on the [pyusb](https://walac.github.io/pyusb/) module.

Compatibility
-------------
Only known to support the Aquaero 6. May support other devices. Use at your own risk.

Usage
-----
```
python aquaero.py
```

Open your browser with the url http://localhost:8000

Output
------
JSON
```
{"status": "success", "message": {"fans": {"fan11": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}, "fan10": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}, "fan12": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}, "fan1": {"power": 10000, "torque": 0, "current": 0, "voltage": 1199, "performance": 0, "rpm": 1155}, "fan3": {"power": 10000, "torque": 0, "current": 0, "voltage": 1202, "performance": 0, "rpm": 1167}, "fan2": {"power": 10000, "torque": 0, "current": 0, "voltage": 1205, "performance": 0, "rpm": 1183}, "fan5": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}, "fan4": {"power": 10000, "torque": 69, "current": 72, "voltage": 1202, "performance": 86, "rpm": 1187}, "fan7": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}, "fan6": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}, "fan9": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}, "fan8": {"power": 10000, "torque": 0, "current": 0, "voltage": 0, "performance": 0, "rpm": -1}}, "reportId": 1, "aquabus": {"rtc": true, "poweradjust7": false, "mps4": false, "farbwerk2": false, "farbwerk1": false, "mps1": false, "poweradjust4": false, "poweradjust6": false, "aquastream2": false, "aquastream1": false, "poweradjust5": false, "poweradjust2": false, "poweradjust3": false, "poweradjust1": false, "mps2": false, "aquaero5slave": false, "poweradjust8": false, "mps3": false}, "temperatures": {"virtualsensor3": null, "virtualsensor2": null, "virtualsensor1": null, "virtualsensor4": null, "temperaturesensor8": null, "temperaturesensor6": 1964, "temperaturesensor7": null, "temperaturesensor4": 1944, "temperaturesensor5": 1865, "temperaturesensor2": 1951, "temperaturesensor3": 1954, "temperaturesensor1": 1967, "fanamplifier1": 2431, "fanamplifier3": 2356, "fanamplifier2": 2431, "fanamplifier4": 2356, "softwaresensor4": 5000, "softwaresensor5": 5000, "softwaresensor6": 5000, "softwaresensor7": 5000, "softwaresensor1": 5000, "softwaresensor2": 5000, "softwaresensor3": 5000, "softwaresensor8": 5000}, "timestamp": 1503266488, "deviceInfo": {"hardware": 6000, "uptimeTotal": 98340, "uptime": 15864, "bootloader": 200, "status": 3, "serial": "xxxxx-xxxxx", "firmware": 2009, "type": "Aquaero XT", "capabilities": {"keys": true, "touch": true, "remote": true, "display": true}, "lockControl": 0}, "structureVersion": 1200, "alarmlevel": 0}}
```
