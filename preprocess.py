from music21 import converter, instrument, note, chord
import glob

notes = []

files = glob.glob("dataset/*")

for file in files:
    print("Reading:", file)

    try:
        midi = converter.parse(file)

        try:
            parts = instrument.partitionByInstrument(midi)

            if parts:
                notes_to_parse = parts.parts[0].recurse()
            else:
                notes_to_parse = midi.flat.notes

        except:
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:

            if isinstance(element, note.Note):
                notes.append(str(element.pitch))

            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    except Exception as e:
        print("Skipping:", file)
        print("Reason:", e)
        continue

print("\nTotal Notes Extracted:", len(notes))

with open("notes.txt", "w") as f:
    for item in notes:
        f.write(item + "\n")

print("Notes saved successfully in notes.txt")