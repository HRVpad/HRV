# Library check
from multiprocessing import Process, Value, Manager
from scipy import signal as sc
import numpy as np
import time
import sys
import os

try:
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtGui, QtCore
    import serial
except:
    from pip._internal import main
    main(['install', 'pyqtgraph'])
    main(['install', 'pyserial'])
    import pyqtgraph as pg
    from pyqtgraph.Qt import QtGui, QtCore
