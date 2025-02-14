import os
import time
import mido
from mido import Message, MidiFile, MidiTrack

# Class for handling the recording
"""
@port is the midi input port
@device_id is the id passed for note-on messages (sometimes keyboards pass note-off as a different id or as velocity=0)
@tempo is the bpm tempo for the midi recording *** HAS TO BE SET **
@debug is for posting messages on console or not

"""
class CK_rec(object):
    def __init__(self, port, device_id, tempo=120, debug=True, save_after=60, recording_folder = None):
        self.port = port
        self.tempo = tempo
        self.debug = debug
        self.on_id = device_id
        self.__mid = MidiFile()
        self.__track = MidiTrack()
        self.prepareTrack()
        self.__activesense = 0
        self.last_note_on_time = time.time()
        self.n_notes_since_last_save = 0
        if recording_folder:
            self.recording_folder = recording_folder
            assert(os.path.isdir(self.recording_folder))
            print(f"Using given recording folder {self.recording_folder}")
        else:
            self.recording_folder = "Recordings"
            if not os.path.isdir("Recordings"):
                os.mkdir("Recordings")
                
    def prepareTrack(self):
        #input("Press [ENTER] to start recording...")
        print("\n**** 📹 You are now RECORDING *****")
        print("(Press Control-C to stop the recording)\n")
        self.__mid.tracks.append(self.__track)

    def __call__(self, event, data=None):
        message, deltatime = event
        # if message[0] == 254:  #compensate for active sense delta times
        self.__activesense += deltatime
        # else:
        #     self.__activesense = deltatime
        if message[0] != 254: #ignore active sense
            miditime = int(round(mido.second2tick(self.__activesense, self.__mid.ticks_per_beat, mido.bpm2tempo(self.tempo))))
            if self.debug:
                print(f'deltatime:  {deltatime:7.4f} msg: {str(message):25} activecomp:  {self.__activesense:7.4f}')
            else:
                #only print note on
                if message[0] == 144: print(message[1])
            if message[0] == self.on_id:
                self.__track.append(Message('note_on', note=message[1], velocity=message[2], time=miditime))
                self.__activesense = 0
                self.last_note_on_time = time.time()
                self.n_notes_since_last_save +=1
            elif message[0] == 176:
                self.__track.append(Message('control_change', channel=1, control=message[1], value=message[2], time=miditime))
                self.__activesense = 0
                self.last_note_on_time = time.time()
                # self.n_notes_since_last_save +=1
                # print("control change")
            else:
                # print("note off!")
                self.__track.append(Message('note_off', note=message[1], velocity=message[2], time=miditime))
                self.__activesense = 0
                self.last_note_on_time = time.time()


    def saveTrack(self, name):
        save_path = os.path.join(self.recording_folder, name+'.mid')
        self.__mid.save(save_path)
        print("\nRecording saved as "+name+".mid in the Recordings folder\n")
