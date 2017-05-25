"""Archivo principal del proyecto."""
import sys
import ConfigParser

from pydub import AudioSegment
from pydub.playback import play

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("config.ini")
voice = "JMP"


inputWord = sys.argv[1]
outputFile = sys.argv[2]

ans = ["-" + inputWord[0]]

for i in range(len(inputWord) - 1):
    ans.append(inputWord[i] + inputWord[i + 1])

ans.append(inputWord[-1] + "-")


resp = AudioSegment.silent()

for phono in ans:
    print(phono)
    diphone = AudioSegment.from_wav(config.get(voice, phono))
    resp = resp + diphone

play(resp)
