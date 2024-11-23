#!/usr/bin/env python3

import json
import mido
import argparse
from tqdm import tqdm
import os

if __name__=="__main__":
    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("quantization", type=int, help="Quantization of the chorales", choices=[16, 8, 4], default=16)
    parser.add_argument("-t", "--twelveKeysTranspose", action="store_true", help="Transpose the chorales to all 12 keys")
    args = parser.parse_args()
    quantization = args.quantization

    if quantization == 16 or quantization == 8:
        filename = f"jsb-chorales-{quantization}th.json"
    elif quantization == 4:
        filename = "jsb-chorales-quarter.json"
    else:
        raise ValueError("Invalid quantization")
    
    # Ensure the directory midi-outputs exists, with subdirectories train, valid, and test
    if not os.path.exists("midi-outputs"):
        os.makedirs("midi-outputs")
    if not os.path.exists("midi-outputs/train"):
        os.makedirs("midi-outputs/train")
    if not os.path.exists("midi-outputs/valid"):
        os.makedirs("midi-outputs/valid")
    if not os.path.exists("midi-outputs/test"):
        os.makedirs("midi-outputs/test")

    print(f"Converting {filename} to MIDI files.")
    with open(filename) as f:
        chorales = json.load(f)

    transpositions = [0] if not args.twelveKeysTranspose else range(12)

    for subset in ["train", "valid", "test"]:
        for transposition in transpositions:
            for n, chorale in tqdm(enumerate(chorales[subset])):
                midiFile = mido.MidiFile()
                quantizationTime = int(midiFile.ticks_per_beat // (quantization / 4))

                # Keep track of the last note played for each voice
                lastChord = [-1] * 4
                tracks = []
                times = []

                # Create a track for each voice
                for i in range(len(lastChord)):
                    track = mido.MidiTrack()
                    midiFile.tracks.append(track)
                    tracks.append(track)
                    track.append(mido.Message("program_change", program=i, channel=i, time=0))
                    times.append(0)

                # Build the MIDI file
                for i, chord in enumerate(chorale):
                    # Notes off
                    for j, note in enumerate(chord):
                        # If the note is different from the last one and the last one is not -1, turn it off
                        if note != lastChord[j] and lastChord[j] != -1:
                            tracks[j].append(mido.Message("note_off", note=int(lastChord[j]+transposition), velocity=64, channel=j, time=(i*quantizationTime) - times[j] - 1))
                            times[j] = i*quantizationTime

                    
                    for j, note in enumerate(chord):
                        if note != lastChord[j]:
                            tracks[j].append(mido.Message("note_on", note=int(note+transposition), velocity=64, channel=j, time=0 if i == 0 and j == 0 else 1))
                            lastChord[j] = note

                # Notes off at the end
                for i in range(len(lastChord)):
                    tracks[i].append(mido.Message("note_off", note=int(lastChord[i]+transposition), velocity=64, channel=i, time=midiFile.ticks_per_beat*4))

                if args.twelveKeysTranspose:
                    midiFilename = f"midi-outputs/{subset}/chorale_{subset}_{n:03d}_{transposition:02d}.mid"
                else:
                    midiFilename = f"midi-outputs/{subset}/chorale_{subset}_{n:03d}.mid"
                midiFile.save(midiFilename)