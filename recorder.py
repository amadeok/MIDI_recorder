import time
import rtmidi
#import from parrentdir
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from CK_rec.setup import Setup
from CK_rec.rec_classes import CK_rec


#mode
debug = True

# Start the Device
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
on_id = codeK.get_device_id()
print('your note on id is: ', on_id, '\n')


# record
codeK.set_callback(CK_rec(myPort, 120))

# Loop to program to keep listening for midi input
try:
    while True:
        time.sleep(0.001)
except KeyboardInterrupt:
    print('')
finally:
    name = input('save midi recording as: ')
    CK_rec.saveTrack(name)
    codeK.end()
