# circuitpython-RS485-wrapper
Simple wrapper class to convert a UART object into a RS485 object for CircuitPython.

## Usage
```python
import time
import board
import busio
from rs485_wrapper import RS485
from p1am_200_helpers import set_serial_mode

# Set P1AM-Serial ports to RS485 mode
port1_de = set_serial_mode(1, 485)
port2_de = set_serial_mode(2, 485)

test_msg_len = 32

port1 = busio.UART(board.TX1, board.RX1, baudrate=115200, receiver_buffer_size=test_msg_len)
RS485_RX = RS485(port1, port1_de)
port2 = busio.UART(board.TX2, board.RX2, baudrate=115200)
RS485_TX = RS485(port2, port2_de, idle_transmitting=True)

counter = 1
while True:

    msg = b"Message #%d" % counter
    RS485_TX.write(msg)
    rx_data = RS485_RX.read(len(msg))  

    if rx_data == msg:
       print(rx_data)
       counter += 1
    else:
        print("No message received")
    time.sleep(1)

```