"""Archivo principal del proyecto."""
import sys
import ConfigParser

from pydub import AudioSegment
from pydub.playback import play

from utils.questionify import questionify

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("config.ini")


def split_word_into_diphones(word):
    """Get a list of diphones needed to synthesize the word."""
    ans = ["-" + word[0]]

    for i in range(len(word) - 1):
        ans.append(word[i] + word[i + 1])

    ans.append(word[-1] + "-")

    return ans


def _synthesize_non_question(word, voice):
    word_diphones = split_word_into_diphones(word)

    resp = AudioSegment.silent(0)

    for phono in word_diphones:
        diphone = AudioSegment.from_wav(config.get(voice, phono))
        resp = resp + diphone

    return resp


def synthesize(word, voice):
    """Synthesize the word using diphones"""
    is_question = False

    if word[-1] == '?':
        is_question = True
        word = word[:-1]

    resp = _synthesize_non_question(word, voice)

    if is_question:
        limit1 = resp.duration_seconds * 0.8
        limit2 = resp.duration_seconds * 1.1

        resp = questionify(resp, limit1, limit2, increase_factor=0.2)

    return resp


if __name__ == "__main__":
    word = sys.argv[1]
    outfile = sys.argv[2]

    resp = synthesize(word, "JMP")

    play(resp)
    resp.export(outfile, format="wav")
