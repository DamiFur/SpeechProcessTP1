"""Audio Helpers."""
import os
import subprocess
import tempfile
import distutils
import ConfigParser
from pydub import AudioSegment
import ml.parsing.textgrid_reader

"""
Boilerplate to load configuration
"""
config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("config.ini")


def textgrid_path(path):
    """Return textgrid path for given wav file."""
    return os.path.splitext(path)[0] + ".TextGrid"


def split_diphones(wav_path, outdir=None):
    """Create diphones from wav_file."""
    tg = ml.parsing.textgrid_reader.read(textgrid_path(wav_path))
    word = os.path.splitext(os.path.basename(wav_path))[0]

    wav_dir = os.path.dirname(wav_path)
    diphones_dir = os.path.join(wav_dir, "diphones")

    if not os.path.exists(diphones_dir):
        os.mkdir(diphones_dir)

    wav = AudioSegment.from_file(wav_path)
    for (begin, end, diphone) in tg[u'phones']:
        diphone = diphone.strip().replace("-", "_")
        if len(diphone) > 0 and diphone[0] != ".":
            diphone_file = "{}_{}.wav".format(diphone, word)
            diphone_path = os.path.join(diphones_dir, diphone_file)

            # Works in milliseconds
            segment = wav[(begin * 1000):(end * 1000)]
            print("Saving {} ({} - {})".format(diphone_path, begin, end))
            segment.export(diphone_path, format="wav")
        elif diphone[0] == ".":
            print("skipping {}".format(diphone))


def get_pitch_tier(wav_path):
    """Return a new file with the pitch tier of the given wav.

    Parameters
    ----------

    wav_path: string
        Path to the wav

    Returns
    -------

    tempfile: NamedTemporaryFile
        A tempfile with .PitchTier extension with the pitch
    """
    script_path = os.path.abspath(config.get("SCRIPTS", "extract_pitch"))
    praat_path = distutils.spawn.find_executable("praat")
    temp = tempfile.NamedTemporaryFile(suffix=".PitchTier")
    wav_path = os.path.abspath(wav_path)

    command = [
        praat_path,
        script_path,
        wav_path,
        temp.name,
        "50",
        "300",
    ]
    print(command)
    subprocess.call(command)

    temp.seek(0)

    return temp
