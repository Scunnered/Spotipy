#Team Activated Almonds
  
import fcntl #https://docs.python.org/2/library/fcntl.html - This module performs file control and I/O control on file descriptors. It is an interface to the fcntl() and ioctl() Unix routines. For a complete description of these calls, see fcntl(2) and ioctl(2) Unix manual pages.
import struct #https://docs.python.org/2/library/struct.html - This module performs conversions between Python values and C structs represented as Python strings. This can be used in handling binary data stored in files or from network connections, among other sources. It uses Format Strings as compact descriptions of the layout of the C structs and the intended conversion to/from Python values.
import array #https://docs.python.org/3/library/array.html - This module defines an object type which can compactly represent an array of basic values: characters, integers, floating point numbers.
import bluetooth #https://docs.pycom.io/tutorials/all/ble/
import bluetooth._bluetooth as bt #By doing it this way, you can refer to it as just bt through the rest of your script.
import RPi.GPIO as GPIO #https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/ - By doing it this way, you can refer to it as just GPIO through the rest of your script.
import time #https://docs.python.org/3/library/time.html - This module provides various time-related functions. For related functionality, see also the datetime and calendar modules.
import os #https://docs.python.org/3/library/os.html - This module provides a portable way of using operating system dependent functionality. If you just want to read or write a file see open(), if you want to manipulate paths, see the os.path module, and if you want to read all the lines in all the files on the command line see the fileinput module. For creating temporary files and directories see the tempfile module, and for high-level file and directory handling see the shutil module.
import datetime #https://docs.python.org/2/library/datetime.html - The datetime module supplies classes for manipulating dates and times in both simple and complex ways. While date and time arithmetic is supported, the focus of the implementation is on efficient attribute extraction for output formatting and manipulation. For related functionality, see also the time and calendar modules.

def bluetooth_rssi(addr):
    # Open hci socket
    hci_sock = bt.hci_open_dev()
    hci_fd = hci_sock.fileno()

    # Connect to device
    bt_sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
    bt_sock.settimeout(10)
    result = bt_sock.connect_ex((addr, 1))	# PSM 1 - Service Discovery

    try:
        # Get ConnInfo
        reqstr = struct.pack("6sB17s", bt.str2ba(addr), bt.ACL_LINK, "\0" * 17)
        request = array.array("c", reqstr )
        handle = fcntl.ioctl(hci_fd, bt.HCIGETCONNINFO, request, 1)
        handle = struct.unpack("8xH14x", request.tostring())[0]

        # Get Received Signal Strength Indicator (RSSI)
        cmd_pkt=struct.pack('H', handle)
        rssi = bt.hci_send_req(hci_sock, bt.OGF_STATUS_PARAM,
                     bt.OCF_READ_RSSI, bt.EVT_CMD_COMPLETE, 4, cmd_pkt)
        rssi = struct.unpack('b', rssi[3])[0]

        # Close sockets
        bt_sock.close()
        hci_sock.close()

        return rssi

    except:
        return None



far = True
far_count = 0

# assume phone is initially far away
rssi = -255
rssi_prev1 = -255
rssi_prev2 = -255

near_cmd = 'br -n 1'
far_cmd = 'br -f 1'

dagar_addr = '34:FC:EF:0C:8F:CB'
emily_addr = '43:29:B1:55:00:00'

debug = 1

while True:
    # get rssi reading for address
    rssi = bluetooth_rssi(dagar_addr)

    if debug:
        print datetime.datetime.now(), rssi, rssi_prev1, rssi_prev2, far, far_count


    if rssi == rssi_prev1 == rssi_prev2 == None:
        print datetime.datetime.now(), "can't detect address"
        time.sleep(0)

    elif rssi == rssi_prev1 == rssi_prev2 == 0:
        # change state if nearby
        if far:
            far = False
            far_count = 0
            os.system(near_cmd)
            print datetime.datetime.now(), "changing to near"
	    GPIO.setwarnings(False)
	    GPIO.setmode(GPIO.BCM)
	    GPIO.setup(17, GPIO.OUT)
	    GPIO.output(17, GPIO.LOW)
            time.sleep(1)

    elif rssi < -2 and rssi_prev1 < -2 and rssi_prev2 < -2:
        # if were near and single has been consisitenly low

        # need 10 in a row to set to far
        far_count += 1
        if not far and far_count > 10:
            # switch state to far
            far = True
            far_count = 0
            os.system(far_cmd)
            print datetime.datetime.now(), "changing to far"
	    GPIO.setmode(GPIO.BCM)
	    GPIO.setup(17, GPIO.OUT)
	    GPIO.output(17, GPIO.HIGH)
            time.sleep(1)

    else:
        far_count = 0


    rssi = rssi_prev1
    rssi_prev1  = rssi_prev2