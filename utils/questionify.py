"""Questionify."""
import tempfile
import copy
import numpy as np
from pydub import AudioSegment
from pitch_tier import get_pitch_tier, replace_pitch_tier


def _questionify_tier(tier, limit1, limit2, increase_factor=0.2):
    time, values = tier["time"], tier["values"]

    """ Hice la cuenta de esto.."""
    mu = values.mean()
    a = (-increase_factor * mu) / float((limit2 - limit1) / 2)**2

    def f(x):
        if limit1 <= x and x <= limit2:
            return a * (x - limit1) * (x - limit2)
        else:
            return 0

    fv = np.vectorize(f)

    x = fv(time)

    new_tier = copy.deepcopy(tier)

    new_tier['values'] = x + values

    return new_tier


def questionify(audio_segment, limit1, limit2, increase_factor=0.2):
    """Questionify wav"""
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav_path = tmp_wav.name

    audio_segment.export(tmp_wav.name, format="WAV")
    tier = get_pitch_tier(wav_path)

    question_tier = _questionify_tier(tier, limit1, limit2, increase_factor)
    replace_pitch_tier(wav_path, question_tier, wav_path)

    return AudioSegment.from_file(wav_path)
