"""
`rs485_wrapper`
================================================================================

Library to wrap UART objects for RS485 communication.

* Author(s): Adam Cummick
"""

import time
import digitalio

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/facts-engineering/CircuitPython_rs485_wrapper.git"

class RS485:
    """
    Class Takes a UART object and wraps it in a class that can be used to
    communicate with an RS485 device.
    
    DE and RE pins can be specified, or they can be shared. 
    DE and RE are automatically controlled when auto_de_re is True. The auto_idle_time
    """
    def __init__(
        self,
        busio_uart,
        de_pin,
        re_pin=None,
        *,
        auto_de_re=True,
        auto_idle_time=0.005,
        de_polarity=True,
        re_polarity=False,
        idle_transmitting=False
    ):

        self._uart = busio_uart
        self._auto_de_re = auto_de_re
        self._auto_idle_time = auto_idle_time
        self._de_polarity = de_polarity
        self._idle_transmitting = (
            idle_transmitting  # whether to rest with transmitter on or off
        )

        if de_pin is not None:
            self._de = self._init_pin(de_pin)
            self.transmitting(self._idle_transmitting)

        if de_pin is re_pin or re_pin is None:
            self._shared_de_re = True
            self._re_polarity = not de_polarity
            self._re = self._de
        else:
            self._shared_de_re = False
            self._re_polarity = re_polarity
            self._re = self._init_pin(re_pin)

    def _init_pin(self, pin):
        try:
            control_pin = pin
            control_pin.switch_to_output()
        except AttributeError:
            control_pin = digitalio.DigitalInOut(pin)
        except Exception as e:
            raise e
        control_pin.switch_to_output()
        return control_pin

    def transmitting(self, state):
        self._de.value = state == self._de_polarity

    def receiving(self, state):
        self._re.value = state == self._re_polarity

    def idle(self):
        time.sleep(self._auto_idle_time)
        self.transmitting(self._idle_transmitting)

    def write(self, buf):
        if self._auto_de_re:
            self.transmitting(True)
            time.sleep(self._auto_idle_time)
        ret = self._uart.write(buf)
        if self._auto_de_re:
            self.idle()
        return ret

    def read(self, nbytes=None):
        if self._auto_de_re:
            self.receiving(True)
            time.sleep(self._auto_idle_time)
        ret = self._uart.read(nbytes)
        if self._auto_de_re:
            self.idle()
        return ret

    def readinto(self, buf):
        if self._auto_de_re:
            self.receiving(True)
            time.sleep(self._auto_idle_time)
        ret = self._uart.readinto(buf)
        if self._auto_de_re:
            self.idle()
        return ret

    def readline(self):
        if self._auto_de_re:
            self.receiving(True)
            time.sleep(self._auto_idle_time)
        ret = self._uart.readline()
        if self._auto_de_re:
            self.idle()
        return ret

    def reset_input_buffer(self):
        self._uart.reset_input_buffer()

    @property
    def in_waiting(self):
        return self._uart.in_waiting
    
    @property
    def baudrate(self):
        return self._uart.baudrate

    @property
    def timeout(self):
        return self._uart.timeout

    @timeout.setter
    def timeout(self, timeout):
        self._uart.timeout = timeout
