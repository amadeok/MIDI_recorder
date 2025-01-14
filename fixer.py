import mido, os

def correct_pedal_messages(input_file):
    # Load the MIDI file
    midi = mido.MidiFile(input_file)
    
    # Iterate over all tracks in the MIDI file
    for track in midi.tracks:
        # Initialize variables to track time and fix pedal messages
        running_time = 0
        new_messages = []

        for message in track:
            running_time = message.time  # Accumulate the running time
            
            if message.type == 'control_change' and message.control in (64,):#, 66):  # Sustain or Sostenuto pedal
                pass
                running_time = 5
                # running_time = 0
            
            # Create a new message to preserve other properties
            new_message = message.copy(time=running_time)
            new_messages.append(new_message)

        # Replace the old messages in the track with the new ones
        track.clear()
        track.extend(new_messages)

    # Save the corrected MIDI file
    base_name, ext = os.path.splitext(input_file)
    output_file = f"{base_name}_pedal_corrected{ext}"
    
    midi.save(output_file)

# Example usage
input_file = os.path.expandvars (r"C:\Users\%username%\Documents\Studio One\Songs\livestream\2024-10-26\4.mid")  # Replace with your input MIDI file path
# output_file = "output_corrected.mid"  # Replace with your desired output file path
correct_pedal_messages(input_file)
