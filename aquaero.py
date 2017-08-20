# -*- coding: utf-8 -*-
#
# aquaerox - Aquacomputer Aquaero 5/6 support for Linux.
#
#
# The MIT License
#
# Copyright © 2017 Oliver Cermann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import usb.core
import usb.util
import structs
import enums
import time
import datetime
import simplejson as json

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class Aquaero(object):
    def __init__(self):
        super(Aquaero, self).__init__()
        
        self.connected = False
        self.vendor_id = 0x0c70
        self.product_id = 0xf001
        self.interfaces = 0x0003
        self.interface = 0x0002
        self.bytelength = 0x0367

        # Aquacomputer offset. Epoch starts at 01/01/2009 12:00am (UTC)
        # The Year 2038 problem
        self.offset_date = 0x495c0780

        self.dev = None

    def connect(self):
        if self.connected == False:
            dev = usb.core.find(idVendor=self.vendor_id, idProduct=self.product_id)

            if dev != None:
                self.dev = dev
                self.connected = True

    def clear(self):
        if self.connected:
            try:
                for interface in range(0, self.interfaces):
                    if self.dev.is_kernel_driver_active(interface) is True:
                        self.dev.detach_kernel_driver(interface)
                        usb.util.claim_interface(self.dev, interface)
            except:
                self.connected = False
                self.connect()
                self.clear()

    def read(self):
        self.clear()

        if self.connected:
            endpoint = self.dev[0x0000][(self.interface, 0x0000)][0x0000]
            data = self.dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize * 0x0040)

            if len(data) >= self.bytelength:
                report = structs.createReport(data)

                output = {
                    'reportId': report.reportId,
                    'timestamp': report.timestamp + self.offset_date,
                    'structureVersion': report.structureVersion,
                    'deviceInfo': {
                        'serial': str(report.deviceInfo.serial[0]) + '-' + str(report.deviceInfo.serial[1]),
                        'firmware': report.deviceInfo.firmware,
                        'bootloader': report.deviceInfo.bootloader,
                        'hardware': report.deviceInfo.hardware,
                        'uptime': report.deviceInfo.uptime,
                        'uptimeTotal': report.deviceInfo.uptimeTotal,
                        'status': report.deviceInfo.status,
                        'lockControl': report.deviceInfo.lockControl,
                        'type': enums.deviceTypes[report.deviceInfo.type],
                        'capabilities': {
                            'display': (True if str(report.deviceInfo.capabilities).find('display') != -1 else False),
                            'keys': (True if str(report.deviceInfo.capabilities).find('keys') != -1 else False),
                            'touch': (True if str(report.deviceInfo.capabilities).find('touch') != -1 else False),
                            'remote': (True if str(report.deviceInfo.capabilities).find('remote') != -1 else False)
                        }
                    },

                    # 'lastSettingsUpdateTime': report.lastSettingsUpdateTime,
                    # 'lcdstate': '|'.join([str(x) for x in report.lcdstate]),
                    'alarmlevel': report.alarmlevel,
                    # 'actualProfile': report.actualProfile,
                    'aquabus': {
                        'aquastream1': (True if str(report.aquabus).find('aquastream1') != -1 else False),
                        'aquastream2': (True if str(report.aquabus).find('aquastream2') != -1 else False),
                        'poweradjust1': (True if str(report.aquabus).find('poweradjust1') != -1 else False),
                        'poweradjust2': (True if str(report.aquabus).find('poweradjust2') != -1 else False),
                        'poweradjust3': (True if str(report.aquabus).find('poweradjust3') != -1 else False),
                        'poweradjust4': (True if str(report.aquabus).find('poweradjust4') != -1 else False),
                        'poweradjust5': (True if str(report.aquabus).find('poweradjust5') != -1 else False),
                        'poweradjust6': (True if str(report.aquabus).find('poweradjust6') != -1 else False),
                        'poweradjust7': (True if str(report.aquabus).find('poweradjust7') != -1 else False),
                        'poweradjust8': (True if str(report.aquabus).find('poweradjust8') != -1 else False),
                        'mps1': (True if str(report.aquabus).find('mps1') != -1 else False),
                        'mps2': (True if str(report.aquabus).find('mps2') != -1 else False),
                        'mps3': (True if str(report.aquabus).find('mps3') != -1 else False),
                        'mps4': (True if str(report.aquabus).find('mps4') != -1 else False),
                        'rtc': (True if str(report.aquabus).find('rtc') != -1 else False),
                        'aquaero5slave': (True if str(report.aquabus).find('aquaero5slave') != -1 else False),
                        'farbwerk1': (True if str(report.aquabus).find('farbwerk1') != -1 else False),
                        'farbwerk2': (True if str(report.aquabus).find('farbwerk2') != -1 else False)
                    },

                    # 'adcRAW': '|'.join([str(x) for x in report.adcRAW]),

                    'temperatures': {
                        'temperaturesensor1': (report.temperatures[0] if report.temperatures[0] != 0x7fff else None),
                        'temperaturesensor2': (report.temperatures[1] if report.temperatures[1] != 0x7fff else None),
                        'temperaturesensor3': (report.temperatures[2] if report.temperatures[2] != 0x7fff else None),
                        'temperaturesensor4': (report.temperatures[3] if report.temperatures[3] != 0x7fff else None),
                        'temperaturesensor5': (report.temperatures[4] if report.temperatures[4] != 0x7fff else None),
                        'temperaturesensor6': (report.temperatures[5] if report.temperatures[5] != 0x7fff else None),
                        'temperaturesensor7': (report.temperatures[6] if report.temperatures[6] != 0x7fff else None),
                        'temperaturesensor8': (report.temperatures[7] if report.temperatures[7] != 0x7fff else None),

                        'softwaresensor1': (report.temperatures[16] if report.temperatures[16] != 0x7fff else None),
                        'softwaresensor2': (report.temperatures[17] if report.temperatures[17] != 0x7fff else None),
                        'softwaresensor3': (report.temperatures[18] if report.temperatures[18] != 0x7fff else None),
                        'softwaresensor4': (report.temperatures[19] if report.temperatures[19] != 0x7fff else None),
                        'softwaresensor5': (report.temperatures[20] if report.temperatures[20] != 0x7fff else None),
                        'softwaresensor6': (report.temperatures[21] if report.temperatures[21] != 0x7fff else None),
                        'softwaresensor7': (report.temperatures[22] if report.temperatures[22] != 0x7fff else None),
                        'softwaresensor8': (report.temperatures[23] if report.temperatures[23] != 0x7fff else None),

                        'virtualsensor1': (report.temperatures[24] if report.temperatures[24] != 0x7fff else None),
                        'virtualsensor2': (report.temperatures[25] if report.temperatures[25] != 0x7fff else None),
                        'virtualsensor3': (report.temperatures[26] if report.temperatures[26] != 0x7fff else None),
                        'virtualsensor4': (report.temperatures[27] if report.temperatures[27] != 0x7fff else None),

                        'fanamplifier1': (report.temperatures[44] if report.temperatures[44] != 0x7fff else None),
                        'fanamplifier2': (report.temperatures[45] if report.temperatures[45] != 0x7fff else None),
                        'fanamplifier3': (report.temperatures[46] if report.temperatures[46] != 0x7fff else None),
                        'fanamplifier4': (report.temperatures[47] if report.temperatures[47] != 0x7fff else None),
                    },

                    # 'rawRpmFlow': '|'.join([str(x) for x in report.rawRpmFlow]),
                    # 'flow': '|'.join([str(x) for x in report.flow]),

                    # 'powerConsumption': {
                    #     '1': {
                    #         'flow': report.powerConsumption[0].flow,
                    #         'sensor1': report.powerConsumption[0].sensor1,
                    #         'sensor2': report.powerConsumption[0].sensor2,
                    #         'deltaT': report.powerConsumption[0].deltaT,
                    #         'power': report.powerConsumption[0].power,
                    #         'rth': report.powerConsumption[0].rth
                    #     },

                    #     '2': {
                    #         'flow': report.powerConsumption[1].flow,
                    #         'sensor1': report.powerConsumption[1].sensor1,
                    #         'sensor2': report.powerConsumption[1].sensor2,
                    #         'deltaT': report.powerConsumption[1].deltaT,
                    #         'power': report.powerConsumption[1].power,
                    #         'rth': report.powerConsumption[1].rth
                    #     },

                    #     '3': {
                    #         'flow': report.powerConsumption[2].flow,
                    #         'sensor1': report.powerConsumption[2].sensor1,
                    #         'sensor2': report.powerConsumption[2].sensor2,
                    #         'deltaT': report.powerConsumption[2].deltaT,
                    #         'power': report.powerConsumption[2].power,
                    #         'rth': report.powerConsumption[2].rth
                    #     },

                    #     '4': {
                    #         'flow': report.powerConsumption[3].flow,
                    #         'sensor1': report.powerConsumption[3].sensor1,
                    #         'sensor2': report.powerConsumption[3].sensor2,
                    #         'deltaT': report.powerConsumption[3].deltaT,
                    #         'power': report.powerConsumption[3].power,
                    #         'rth': report.powerConsumption[3].rth
                    #     }
                    # },

                    # 'level': '|'.join([str(x) for x in report.level]),
                    # 'humidity': '|'.join([str(x) for x in report.humidity]),
                    # 'conductivity': '|'.join([str(x) for x in report.conductivity]),
                    # 'pressure': '|'.join([str(x) for x in report.pressure]),
                    # 'tacho': report.tacho,

                    'fans': {
                        'fan1': {
                            'rpm': report.fans[0].rpm,
                            'power': report.fans[0].power,
                            'voltage': report.fans[0].voltage,
                            'current': report.fans[0].current,
                            'performance': report.fans[0].performance,
                            'torque': report.fans[0].torque
                        },

                        'fan2': {
                            'rpm': report.fans[1].rpm,
                            'power': report.fans[1].power,
                            'voltage': report.fans[1].voltage,
                            'current': report.fans[1].current,
                            'performance': report.fans[1].performance,
                            'torque': report.fans[1].torque
                        },

                        'fan3': {
                            'rpm': report.fans[2].rpm,
                            'power': report.fans[2].power,
                            'voltage': report.fans[2].voltage,
                            'current': report.fans[2].current,
                            'performance': report.fans[2].performance,
                            'torque': report.fans[2].torque
                        },

                        'fan4': {
                            'rpm': report.fans[3].rpm,
                            'power': report.fans[3].power,
                            'voltage': report.fans[3].voltage,
                            'current': report.fans[3].current,
                            'performance': report.fans[3].performance,
                            'torque': report.fans[3].torque
                        },

                        'fan5': {
                            'rpm': report.fans[4].rpm,
                            'power': report.fans[4].power,
                            'voltage': report.fans[4].voltage,
                            'current': report.fans[4].current,
                            'performance': report.fans[4].performance,
                            'torque': report.fans[4].torque
                        },

                        'fan6': {
                            'rpm': report.fans[5].rpm,
                            'power': report.fans[5].power,
                            'voltage': report.fans[5].voltage,
                            'current': report.fans[5].current,
                            'performance': report.fans[5].performance,
                            'torque': report.fans[5].torque
                        },

                        'fan7': {
                            'rpm': report.fans[6].rpm,
                            'power': report.fans[6].power,
                            'voltage': report.fans[6].voltage,
                            'current': report.fans[6].current,
                            'performance': report.fans[6].performance,
                            'torque': report.fans[6].torque
                        },

                        'fan8': {
                            'rpm': report.fans[7].rpm,
                            'power': report.fans[7].power,
                            'voltage': report.fans[7].voltage,
                            'current': report.fans[7].current,
                            'performance': report.fans[7].performance,
                            'torque': report.fans[7].torque
                        },

                        'fan9': {
                            'rpm': report.fans[8].rpm,
                            'power': report.fans[8].power,
                            'voltage': report.fans[8].voltage,
                            'current': report.fans[8].current,
                            'performance': report.fans[8].performance,
                            'torque': report.fans[8].torque
                        },

                        'fan10': {
                            'rpm': report.fans[9].rpm,
                            'power': report.fans[9].power,
                            'voltage': report.fans[9].voltage,
                            'current': report.fans[9].current,
                            'performance': report.fans[9].performance,
                            'torque': report.fans[9].torque
                        },

                        'fan11': {
                            'rpm': report.fans[10].rpm,
                            'power': report.fans[10].power,
                            'voltage': report.fans[10].voltage,
                            'current': report.fans[10].current,
                            'performance': report.fans[10].performance,
                            'torque': report.fans[10].torque
                        },

                        'fan12': {
                            'rpm': report.fans[11].rpm,
                            'power': report.fans[11].power,
                            'voltage': report.fans[11].voltage,
                            'current': report.fans[11].current,
                            'performance': report.fans[11].performance,
                            'torque': report.fans[11].torque
                        }
                    },

                    # 'aquastream': {
                    #     'pump1': {
                    #         'rpm': report.aquastream[0].rpm,
                    #         'voltage': report.aquastream[0].voltage,
                    #         'current': report.aquastream[0].current
                    #     },
                        
                    #     'pump2': {
                    #         'rpm': report.aquastream[1].rpm,
                    #         'voltage': report.aquastream[1].voltage,
                    #         'current': report.aquastream[1].current
                    #     },
                        
                    #     'pump3': {
                    #         'rpm': report.aquastream[2].rpm,
                    #         'voltage': report.aquastream[2].voltage,
                    #         'current': report.aquastream[2].current
                    #     },
                        
                    #     'pump4': {
                    #         'rpm': report.aquastream[3].rpm,
                    #         'voltage': report.aquastream[3].voltage,
                    #         'current': report.aquastream[3].current
                    #     },
                        
                    #     'pump5': {
                    #         'rpm': report.aquastream[4].rpm,
                    #         'voltage': report.aquastream[4].voltage,
                    #         'current': report.aquastream[4].current
                    #     },
                        
                    #     'pump6': {
                    #         'rpm': report.aquastream[5].rpm,
                    #         'voltage': report.aquastream[5].voltage,
                    #         'current': report.aquastream[5].current
                    #     },
                        
                    #     'pump7': {
                    #         'rpm': report.aquastream[6].rpm,
                    #         'voltage': report.aquastream[6].voltage,
                    #         'current': report.aquastream[6].current
                    #     },
                        
                    #     'pump8': {
                    #         'rpm': report.aquastream[7].rpm,
                    #         'voltage': report.aquastream[7].voltage,
                    #         'current': report.aquastream[7].current
                    #     }
                    # }
                }

                output = {
                    'status': 'success',
                    'message': output
                }

                return json.dumps(output) 
            else:
                output = {
                    'status': 'failed',
                    'message': 'Aquaero data are currupt!'
                }

                return json.dumps(output) 
        else:
            output = {
                'status': 'failed',
                'message': 'Aquaero device not found on USB port!'
            }

            return json.dumps(output) 

aquaero = Aquaero()

class HTTPHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        aquaero.connect()
        self._set_headers()
        self.wfile.write(aquaero.read())

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        aquaero.connect()
        self._set_headers()
        self.wfile.write(aquaero.read())
        
def run(server_class=HTTPServer, handler_class=HTTPHandler, port=8000):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting aquaero httpd server...'
    httpd.serve_forever()

if __name__ == "__main__":
    run()
