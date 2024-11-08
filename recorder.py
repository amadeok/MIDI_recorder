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
import signal


class AutoRecorder():
    def __init__(self, save_after=60) -> None:  
        self.exit = False
        self.device = "clone 3"
        self.myPort = 4
        self.__thread = None
        self.save_after = save_after
    
        
    def loop(self):
        while 1:
            codeK = Setup()
            for i, d in enumerate(mido.get_input_names()):
                if self.device in d:
                    self.myPort = i
                    break
            codeK.open_port(self.myPort)
            on_id = 144#codeK.get_device_id()
            print('your note on id is: ', on_id)

            midiRec = CK_rec(self.myPort, on_id, debug=True, save_after=5)
            codeK.set_callback(midiRec)
            
            while True:
                d = time.time() - midiRec.last_note_on_time
                if d > self.save_after:
                    #raise Exception("break")
                    print("timeout")
                    midiRec.last_note_on_time = time.time()
                    break
                print("elapsed time", round(d, 3),  " of ", self.save_after)
                time.sleep(1)
                if self.exit: break
                
            if midiRec.n_notes_since_last_save:
                name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")# input('\nsave midi recording as? (leaving the name blank discards the recording): ')
                midiRec.saveTrack(name)
                midiRec.n_notes_since_last_save = 0
            else:
                print("No notes recorded")

            time.sleep(1)

            codeK.end() 
            if self.exit:
                print("Exiting...")
                break
            
    def start_on_other_thread(self):
        import threading
        self.__thread = threading.Thread(target=self.loop)
        self.__thread.start()
        
    def join(self):
        if self.__thread:
            self.__thread.join()
        
    def stop(self):
        self.exit = True

if __name__ == "__main__":
    autorec = AutoRecorder(10)
    autorec.start_on_other_thread()
    #time.sleep(5)
    #autorec.stop()
    autorec.join()

# codeK.perform_setup()
# def signal_handler(signum, frame):
#     print(f"Signal handler called with signal: {signum}")
#     # Perform any cleanup or exit operations here
#     print("Exiting gracefully")
#     global exit
#     exit = True

# # Register the signal handler for SIGINT
# signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)
# print("Process ID:", os.getpid())

# Loop to program to keep listening for midi input
