import time,os
import  mido, datetime
#import from parrentdir
from . import setup_, rec_classes

# from setup_ import Setup

class AutoRecorder():
    def __init__(self, save_after=60, recording_folder = None) -> None:  
        self.exit = False
        self.device = "clone 3"
        self.myPort = 4
        self.__thread = None
        self.save_after = save_after
        self.recording_folder = recording_folder
    
    def loop(self):
        while 1:
            codeK = setup_.Setup()
            for i, d in enumerate(mido.get_input_names()):
                if self.device in d:
                    self.myPort = i
                    break
            codeK.open_port(self.myPort)
            on_id = 144#codeK.get_device_id()
            print('your note on id is: ', on_id)

            midiRec = rec_classes.CK_rec(self.myPort, on_id, debug=True, save_after=5, recording_folder=self.recording_folder)
            codeK.set_callback(midiRec)
            
            while True:
                d = time.perf_counter() - midiRec.last_note_on_time
                if d > self.save_after:
                    #raise Exception("break")
                    print("timeout")
                    midiRec.last_note_on_time = time.perf_counter()
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
    autorec = AutoRecorder(10, recording_folder=os.path.expandvars(r"C:\Users\%username%\Documents\Studio One\Songs\midi_backups"))
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
