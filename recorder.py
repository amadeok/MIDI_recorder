import time
import rtmidi, mido, datetime
#import from parrentdir
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from CK_rec.setup import Setup
from CK_rec.rec_classes import CK_rec


# Start the Device
codeK = Setup()

device = "clone 3"
myPort = 4
for i, d in enumerate(mido.get_input_names()):
    if device in d:
        myPort = i
        break

# codeK.perform_setup()
codeK.open_port(myPort)
on_id = 144#codeK.get_device_id()
print('your note on id is: ', on_id)

save_after = 60
midiRec = CK_rec(myPort, on_id, debug=False, save_after=5)
codeK.set_callback(midiRec)


# Loop to program to keep listening for midi input
while 1:
    while True:
        d = time.time() - midiRec.last_note_on_time
        if d > save_after:
            #raise Exception("break")
            print("timeout")
            midiRec.last_note_on_time = time.time()
            break
        print("elapsed time", round(d, 3),  " of ", save_after)
        time.sleep(1)


    if midiRec.n_notes_since_last_save:
        name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")# input('\nsave midi recording as? (leaving the name blank discards the recording): ')
        midiRec.saveTrack(name)
        midiRec.n_notes_since_last_save = 0
    else:
        print("No notes recorded")
    time.sleep(1)

    #codeK.end() 
