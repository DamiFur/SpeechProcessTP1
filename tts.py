"""Archivo principal del proyecto."""
import sys
import ConfigParser

from pydub import AudioSegment

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

    span = []
    current_sec = 0

    for phono in word_diphones:
        diphone = AudioSegment.from_wav(config.get(voice, phono))

        span.append({
            'diphone': phono,
            'limits': (current_sec, current_sec + diphone.duration_seconds)
        })

        current_sec += diphone.duration_seconds
        resp = resp + diphone

    return resp, span


def _find_peak_limits(span):
    duration = span[-1]["limits"][1]
    if len(span) == 3:
        # una sola slaba
        return 0, duration + 0.1
    else:
        before_last = span[-5]["limits"][1]
        return before_last, duration + 0.1


def synthesize(word, voice):
    """Synthesize the word using diphones."""
    is_question = False

    if word[-1] == '?':
        is_question = True
        word = word[:-1]

    resp, span = _synthesize_non_question(word, voice)

    if is_question:
        limit1, limit2 = _find_peak_limits(span)

        resp = questionify(resp, limit1, limit2, increase_factor=0.35)

    return resp


if __name__ == "__main__":
    word = sys.argv[1]
    outfile = sys.argv[2]

    resp = synthesize(word, "JMP")

    resp.export(outfile, format="wav")
