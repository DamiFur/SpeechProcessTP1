"""Parse PitchTier files."""
import shlex
import os
import numpy as np
import distutils
import subprocess
import ConfigParser
import tempfile

"""
Boilerplate to load configuration
"""

file_dir = os.path.abspath(os.path.dirname(__file__))
proj_dir = os.path.join(file_dir, "..")

config = ConfigParser.ConfigParser()
config.optionxform = str
config.read(os.path.join(proj_dir, "config.ini"))


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

    return _parse_pitch_tier(temp)


def _parse_pitch_tier(f):
    """Parse a pitch tier file into a dict."""
    ret = _parse_header(f)

    line = f.readline()

    ret["time"] = []
    ret["values"] = []

    while len(line) > 0:
        time_line = f.readline()
        value_line = f.readline()

        time = float(shlex.split(time_line)[2])
        value = float(shlex.split(value_line)[2])
        ret["time"].append(time)
        ret["values"].append(value)

        line = f.readline()

    assert(len(ret["time"]) == ret["no_points"])

    ret["time"] = np.array(ret["time"], dtype=float)
    ret["values"] = np.array(ret["values"], dtype=float)

    return ret


def _parse_header(f):
    f.readline()
    f.readline()
    f.readline()

    xmin = float(shlex.split(f.readline())[2])
    xmax = float(shlex.split(f.readline())[2])
    no_points = int(shlex.split(f.readline())[3])

    return {
        "xmin": xmin,
        "xmax": xmax,
        "no_points": no_points,
    }

_header = """File type = \"ooTextFile\"
Object class = \"PitchTier\"

xmin = {}
xmax = {}

points: size = {}
"""

_point = """points[{}]:
    number = {}
    value = {}
"""


def convert_to_pitch_tier(info, outfile):
    """Convert dict into pitch tier."""
    outfile.write(_header.format(info["xmin"],
                  info["xmax"], info["no_points"]))

    for i, (time, value) in enumerate(info["points"]):
        outfile.write(_point.format(i + 1, time, value))
