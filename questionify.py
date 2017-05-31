"""Questionify module."""
import ConfigParser
import os
import tempfile
import distutils
import subprocess
"""
Boilerplate to load configuration
"""
config = ConfigParser.ConfigParser()
config.optionxform = str
config.read("config.ini")


def questionify_pitch(input_file):
    """Questionify pitch."""
    points = 0
    text = input_file.read()
    lines = text.split('\n')
    for line in lines:
        if "points: size" in line:
            points = int(line.split("= ", 1)[1])
            break

    limit1 = points * 0.80
    limit2 = points * 0.93

    pointvalues = text.split("points [")

    i = 0
    ans = pointvalues[0]
    constant = 1.05
    for p in pointvalues:
        if i > limit1:
            aux = p.split("value = ", 1)
            tmp = float(aux[1])
            tmp = tmp * constant
            if i < limit2:
                constant += 0.02
            else:
                constant -= 0.04
            ans += "points [" + aux[0] + "value = " + str(tmp) + "\n"
            print constant
        else:
            if i != 0:
                ans += "points [" + p
        i += 1

    output_file = tempfile.NamedTemporaryFile(suffix=".PitchTier")

    output_file.write(ans)
    output_file.flush()

    return output_file


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
    subprocess.call(command)

    temp.seek(0)

    return temp


def replace_pitch_tier(wav_path, pitch_tier_path, output_path):
    """Return a new file with the pitch tier replaced."""
    script_path = os.path.abspath(config.get("SCRIPTS", "replace_pitch"))
    praat_path = distutils.spawn.find_executable("praat")
    wav_path = os.path.abspath(wav_path)

    command = [
        praat_path,
        script_path,
        wav_path,
        pitch_tier_path,
        output_path,
        "50",
        "300",
    ]

    print command

    subprocess.call(command)


def questionify(wav_path, output_path):
    """Convert wav to a question."""
    wav_path = os.path.abspath(wav_path)
    output_path = os.path.abspath(output_path)

    pitch_tier = get_pitch_tier(wav_path)
    modified_pitch_tier = questionify_pitch(pitch_tier)
    replace_pitch_tier(wav_path, modified_pitch_tier.name, output_path)
