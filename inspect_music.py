from music21 import converter

midi = converter.parse("generated_music.mid")

notes = midi.flatten().notes

print("Total Generated Notes:", len(notes))

for n in notes[:20]:
    print(n)