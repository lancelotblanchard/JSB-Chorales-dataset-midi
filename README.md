# JSB-Chorales-dataset-midi
A Python script to turn the JSB Chorales dataset (from [Boulanger-Lewandowski (2012)][http://www-etud.iro.umontreal.ca/~boulanni/icml2012]) into MIDI files. Adapted from [czhuang/JSB-Chorales-dataset](https://github.com/czhuang/JSB-Chorales-dataset), especially for the train, test, and validation split. The data does not distinguish between held and repeated notes, and interprets repeated notes as legato.

## How to run

1. Install dependencies with `pip install -r requirements.txt`

2. Run `./JsbToMidi.py QUANTIZATION` by replacing `QUANTIZATION` with the desired quantization level (4, 8, or 16).

3. Collect the MIDI files in `midi-outputs`.