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

def normalizeValue(obj):
    if isinstance(obj, ctypes.Array):
        return list(obj)
    return obj

def normalize(obj):
    return {k[0]: normalizeValue(getattr(obj, k[0])) for k in obj._fields_}

def formatValue(value):
    if value is None: return ''
    if isinstance(value, str): return ': ' + value
    return ': ' + repr(value)

def filterFeatures(features, getter = None):
    if isinstance(getter, list):
        getter = lambda i: getter[i]
    return filter(getter, features)

def formatFeatures(features):
    return ', '.join(':' + name for name in features)

def formatDict(obj, valueFunc = formatValue):
    return ', '.join(str(key) + valueFunc(value) for key, value in obj.items())

def simpleFormat(obj):
    if isinstance(obj, ctypes.Structure): return ''
    if isinstance(obj, list): return ' ({:d})'.format(len(obj))
    return formatValue(obj)
