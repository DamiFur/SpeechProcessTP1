"""Archivo principal del proyecto."""
import sys
import ConfigParser

from pydub import AudioSegment
from pydub.playback import play


def split_word_into_diphones(word):
    """Get a list of diphones needed to synthesize the word."""
    ans = ["-" + word[0]]

    for i in range(len(word) - 1):
        ans.append(word[i] + word[i + 1])

    ans.append(word[-1] + "-")

    return ans


def synthesize(word, voice):
    """Synthesize the word using diphones"""
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.read("config.ini")

    word_diphones = split_word_into_diphones(word)

    resp = AudioSegment.silent()

    for phono in word_diphones:
        diphone = AudioSegment.from_wav(config.get(voice, phono))
        resp = resp + diphone

    return resp

if __name__ == "__main__":
    word = sys.argv[1]
    outfile = sys.argv[2]

    resp = synthesize(word, "JMP")

    play(resp)
    resp.export(outfile, format="wav")

