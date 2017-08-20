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

deviceTypes = {
    0: 'Aquaero LT',
    1: 'Aquaero PRO',
    2: 'Aquaero XT',
    3: 'Aquaduct MK4 361',
    4: 'Aquaduct MK4 360',
    5: 'Aquaduct MK4 720',
    6: 'Aquaduct MK5 360',
    7: 'Aquaduct MK5 720'
}

aquabusStatusFields = [
    'aquastream1',
    'aquastream2',
    'poweradjust1',
    'poweradjust2',
    'poweradjust3',
    'poweradjust4',
    'poweradjust5',
    'poweradjust6',
    'poweradjust7',
    'poweradjust8',
    'mps1',
    'mps2',
    'mps3',
    'mps4',
    'rtc',
    'aquaero5slave',
    'farbwerk1',
    'farbwerk2'
]

# currenty not used
temperatureSensorFields = {
    0: 'temperaturesensor1',
    1: 'temperaturesensor2',
    2: 'temperaturesensor3',
    3: 'temperaturesensor4',
    4: 'temperaturesensor5',
    5: 'temperaturesensor6',
    6: 'temperaturesensor7',
    7: 'temperaturesensor8',
    16: 'softwaresensor1',
    17: 'softwaresensor2',
    18: 'softwaresensor3',
    19: 'softwaresensor4',
    20: 'softwaresensor5',
    21: 'softwaresensor6',
    22: 'softwaresensor7',
    23: 'softwaresensor8',
    24: 'virtualsensor1',
    25: 'virtualsensor2',
    26: 'virtualsensor3',
    27: 'virtualsensor4',
    44: 'fanamplifier1',
    45: 'fanamplifier2',
    46: 'fanamplifier3',
    47: 'fanamplifier4'
}
