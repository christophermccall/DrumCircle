from music21 import note, stream, tempo, midi

s = stream.Stream()

s.append(tempo.MetronomeMark(number=120))

snare = note.Note(38)
snare.quarterLength = 4

s.append(snare)

sp = midi.realtime.StreamPlayer(s)

sp.play()
