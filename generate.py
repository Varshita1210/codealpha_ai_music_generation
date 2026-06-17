import random
import numpy as np
from tensorflow.keras.models import load_model
from music21 import note, stream

# Load notes
with open("notes.txt", "r") as file:
    notes = file.read().splitlines()

pitchnames = sorted(set(notes))

note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

sequence_length = 50

network_input = []

for i in range(len(notes) - sequence_length):
    sequence = notes[i:i + sequence_length]
    network_input.append([note_to_int[n] for n in sequence])

model = load_model("music_model.keras")

start = random.randint(0, len(network_input) - 1)

pattern = network_input[start]

prediction_output = []

for note_index in range(1000):

    prediction_input = np.reshape(pattern, (1, len(pattern), 1))
    prediction_input = prediction_input / float(len(pitchnames))

    prediction = model.predict(prediction_input, verbose=0)

    index = np.argmax(prediction)

    result = int_to_note[index]

    prediction_output.append(result)

    pattern.append(index)
    pattern = pattern[1:]

offset = 0
output_notes = []

for pattern in prediction_output:

    new_note = note.Note(pattern)
    new_note.offset = offset

    output_notes.append(new_note)

    offset += 0.5

midi_stream = stream.Stream(output_notes)

midi_stream.write('midi', fp='generated_music.mid')

print("Generated Music Saved as generated_music.mid")