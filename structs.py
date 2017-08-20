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

import ctypes
import struct
from utils import *
from enums import *


class ReportDeviceCapabilities(ctypes.BigEndianStructure):
    # typedef union {
    #    uint16_t data;
    #    struct {
    #       uint16_t HasDisplay :1;
    #       uint16_t HasKeys :1;
    #       uint16_t HasTouch :1;
    #       uint16_t HasIrReciver :1;
    #    } Bits;
    # } DeviceCapabilities;

    _pack_ = 1
    _fields_ = [('bits', ctypes.c_uint16)]

    def __repr__(self):
        l = formatFeatures(self.listCapabilities())
        return '<ReportDeviceCapabilities' + (' ' if len(l) else '') + l + '>'

    def listCapabilities(self):
        deviceCapabilities = ['display', 'keys', 'touch', 'remote']
        return list(filterFeatures(deviceCapabilities, lambda f: getattr(self, 'has' + f[0].upper() + f[1:])()))

    def hasDisplay(self):
        return bool(self.bits & 1)

    def hasKeys(self):
        return bool(self.bits & 2)

    def hasTouch(self):
        return bool(self.bits & 4)

    def hasRemote(self):
        return bool(self.bits & 8)


class ReportDeviceInfo(ctypes.BigEndianStructure):
    # typedef struct 
    # {
    #    uint16_t serial[2];              //serial number - 2x 16 bit value
    #    uint16_t firmware;               //firmware version
    #    uint16_t bootloader;             //bootloader id
    #    uint16_t hardware;               //hardware id
    #    uint32_t uptime;                 //uptime poweron -> now
    #    uint32_t uptimeTotal;            //uptime total
    #    DeviceStatus status;             //iunt8_t, supply state
    #    SystemLockControl lockControl;   //uint16_t, gerätesperren verwalten
    #    DeviceType_t deviceType;
    #    DeviceCapabilities capabilities;
    # }tDeviceInfo;

    _pack_ = 1
    _fields_ = [('serial', ctypes.c_uint16 * 2),
                ('firmware', ctypes.c_uint16),
                ('bootloader', ctypes.c_uint16),
                ('hardware', ctypes.c_uint16),
                ('uptime', ctypes.c_uint32),
                ('uptimeTotal', ctypes.c_uint32),
                ('status', ctypes.c_uint8),
                ('lockControl', ctypes.c_uint16),
                ('type', ctypes.c_uint8),
                ('capabilities', ReportDeviceCapabilities)]

    def __repr__(self):
        rep = normalize(self)
        rep['serial'] = '\'{:05d}-{:05d}\''.format(*rep['serial'])
        rep['type'] = '{:d} ({:s})'.format(self.type, deviceTypes.get(self.type, 'unknown'))
        rep['capabilities'] = None

        return '<ReportDeviceInfo ' + formatDict(rep) + '>'


class ReportPowerConsumption(ctypes.BigEndianStructure):
    # typedef struct
    # {
    #    int16_t flow;                 //flow
    #    int16_t sensor1;              //sensor 1
    #    int16_t sensor2;              //sensor 2
    #    int16_t detaT;                //absolute delta temperature between s1 und s2
    #    int16_t power;                //calculated power consumption
    #    int16_t rth;                  //thermal resistance
    # }tPowerConsumptionData;

    _pack_ = 1
    _fields_ = [('flow', ctypes.c_int16),
                ('sensor1', ctypes.c_int16),
                ('sensor2', ctypes.c_int16),
                ('deltaT', ctypes.c_int16),
                ('power', ctypes.c_int16),
                ('rth', ctypes.c_int16)]

    def __repr__(self):
        return '<ReportPowerConsumption ' + formatDict(normalize(self)) + '>'


class ReportFanData(ctypes.BigEndianStructure):
    # typedef struct 
    # {
    #    int16_t rpm;                     //fan rpm
    #    int16_t power;                   //fan power in %
    #    int16_t voltage;                 //fan voltage
    #    int16_t current;                 //fan current
    #    int16_t performance;             //power consumption in W
    #    int16_t torque;                  //torque in Nm
    # }tFanData;

    _pack_ = 1
    _fields_ = [('rpm', ctypes.c_int16),
                ('power', ctypes.c_int16),
                ('voltage', ctypes.c_int16),
                ('current', ctypes.c_int16),
                ('performance', ctypes.c_int16),
                ('torque', ctypes.c_int16)]

    def __repr__(self):
        return '<ReportFanData ' + formatDict(normalize(self)) + '>'


class ReportAquabusStatus(ctypes.BigEndianStructure):
    # typedef union {
    #    uint32_t data;
    #    struct {
    #       uint32_t aquastream1 :1;   //0x0001
    #       uint32_t aquastream2 :1;   //0x0002
          
    #       uint32_t poweradjust1 :1;  //0x0004
    #       uint32_t poweradjust2 :1;  //0x0008
    #       uint32_t poweradjust3 :1;  //0x0010
    #       uint32_t poweradjust4 :1;  //0x0020
    #       uint32_t poweradjust5 :1;  //0x0040
    #       uint32_t poweradjust6 :1;  //0x0080
    #       uint32_t poweradjust7 :1;  //0x0100
    #       uint32_t poweradjust8 :1;  //0x0200
          
    #       uint32_t mps1 :1;          //0x0400
    #       uint32_t mps2 :1;          //0x0800
    #       uint32_t mps3 :1;          //0x1000
    #       uint32_t mps4 :1;          //0x2000
          
    #       uint32_t rtc :1;           //0x4000
    #       uint32_t aquaero5slave :1; //0x8000  
          
    #       uint32_t farbwerk1 :1;     //0x10000
    #       uint32_t farbwerk2 :1;     //0x20000
          
    #    } Bits;
    # } AquabusStatus;

    _pack_ = 1
    _fields_ = [('bits', ctypes.c_uint32)]

    def __getattribute__(self, name):
        try:
            index = aquabusStatusFields.index(name)
        except ValueError:
            return super(ReportAquabusStatus, self).__getattribute__(name)
        return int(bool(self.bits & (1 << index)))

    def __repr__(self):
        active = self.listActive()
        if len(active):
            return '<ReportAquabusStatus ' + formatFeatures(active) + '>'
        else:
            return '<ReportAquabusStatus>'

    def listActive(self):
        return list(filterFeatures(aquabusStatusFields, lambda f: getattr(self, f)))


class ReportAquastreamStatus(ctypes.BigEndianStructure):
    # typedef union {
    #    uint8_t data;
    #    struct {
    #       uint8_t available :1;  //pump is connected
    #       uint8_t alarm :1;      //is alarm active
    #    } Bits;
    # } tAquastreamStatus;

    _pack_ = 1
    _fields_ = [('data', ctypes.c_uint8)]

    def __repr__(self):
        rep = {
            'available': self.isAvailable(),
            'alarmActive': self.isAlarmActive()
        }

        return '<ReportAquastreamStatus ' + formatDict(rep) + '>'

    def isAvailable(self):
        return bool(self.data & 1)

    def isAlarmActive(self):
        return bool(self.data & 2)


class ReportPumpData(ctypes.BigEndianStructure):
    # typedef struct 
    # {
    #    tAquastreamStatus status;     //pump state
    #    tAquastreamMode mode;         //pump mode
    #    int16_t rpm;                  //pump speed in rpm
    #    int16_t voltage;              //pump voltage in 1/10V
    #    int16_t current;              //pump current in mA
    # }tPumpData;

    _pack_ = 1
    _fields_ = [('status', ReportAquastreamStatus),
                ('mode', ctypes.c_uint8),
                ('rpm', ctypes.c_int16),
                ('voltage', ctypes.c_int16),
                ('current', ctypes.c_int16)]

    def __repr__(self):
        rep = normalize(self)
        rep['status'] = None

        return '<ReportPumpData ' + formatDict(rep) + '>'


class ReportControllers(ctypes.BigEndianStructure):
    # typedef struct 
    # {
    #    int16_t twoPoint[16];     //2controller outputs
    #    int16_t constant[32];     //constant preset outputs
    #    int16_t rgbLed[12];       //rgb controller outputs
    #    int16_t setPoint[8];      //setpoint controller
    #    int16_t curve[4];         //curve controller
    #    ...
    # }tReportControllers;

    _pack_ = 1
    _fields_ = [('twoPoint', ctypes.c_int16 * 16),
                ('constant', ctypes.c_int16 * 32),
                ('rgbLed', ctypes.c_int16 * 12),
                ('setPoint', ctypes.c_int16 * 8),
                ('curve', ctypes.c_int16 * 4)]

    def __repr__(self):
        return '<ReportControllers ' + formatDict(normalize(self)) + '>'


class Report(ctypes.BigEndianStructure):
    _pack_ = 1
    _fields_ = [('reportId', ctypes.c_uint8),                       # usb report id
                ('timestamp', ctypes.c_uint32),                     # current UTC device datetime in 32bit unix format
                ('structureVersion', ctypes.c_uint16),              # structure id (data lyout version)

                ('deviceInfo', ReportDeviceInfo),                   # device info (serial...)
                ('lastSettingsUpdateTime', ctypes.c_uint32),        # last settings change

                ('lcdstate', ctypes.c_uint8 * 20),                  # only for internal handling (20bytes)
                ('alarmlevel', ctypes.c_uint8),                     # 0:normal, 1:warn, 2:alarm, 3:x
                ('actualProfile', ctypes.c_uint8),                  # current profile
                ('aquabus', ReportAquabusStatus),                   # aquabus devices

                ('adcRAW', ctypes.c_uint16 * 20),                   # adc raw values range:0..0xffff
                ('temperatures', ctypes.c_int16 * 64),              # 64 temperaturesensoren, invalid: 0x7fff (32767)
                ('rawRpmFlow', ctypes.c_uint32 * 5),                # impulse rpm times in 1/100ms == 0.01e10-3s
                ('flow', ctypes.c_uint16 * 14),                     # 2xinternal flow + 8xpoweradjust + 4xmps flow
                ('powerConsumption', ReportPowerConsumption * 4),   # power consumption data
                ('level', ctypes.c_int16 * 4),                      # fill level sensors
                ('humidity', ctypes.c_int16 * 4),                   # humidity sensor data (not available yet)
                ('conductivity', ctypes.c_int16 * 4),               # water quality (aquaduct only)
                ('pressure', ctypes.c_int16 * 4),                   # pressure sensors (mps)

                ('tacho', ctypes.c_int16),                          # rpm output
                ('fans', ReportFanData * 12),                       # fan data
                ('aquastream', ReportPumpData * 8),                 # pump data
                ('outputAvailable', ctypes.c_uint32),               # output states, 64bits == outputs[64]
                ('outputs', ctypes.c_int16 * 64),                   # output values
                                                                    # #define OUTPUT_LED_R       0
                                                                    # #define OUTPUT_LED_G       1
                                                                    # #define OUTPUT_LED_B       2
                                                                    # #define OUTPUT_RELAY       3
                                                                    # #define OUTPUT_POWER1      4
                                                                    # #define OUTPUT_POWER2      5
                                                                    # #define OUTPUT_FARBWERK    6   
                                                                    # #define OUTPUT_AQUASTREAM  30
                                                                    # #define OUTPUT_MPS         32

                ('controllers', ReportControllers)]                 # controller outputs, scaled from 0..100% [0...10000]

    def __repr__(self):
        print formatDict(normalize(self))
        return '<Report ' + formatDict(normalize(self), simpleFormat) + '>'


def createReport(data):
    return Report.from_buffer_copy(data)
