"""Parse PitchTier files."""
import shlex


def parse_pitch_tier(f):
    """Parse a pitch tier file into a dict."""
    ret = _parse_header(f)

    line = f.readline()

    ret["points"] = []

    while len(line) > 0:
        time_line = f.readline()
        value_line = f.readline()

        time = float(shlex.split(time_line)[2])
        value = float(shlex.split(value_line)[2])
        ret["points"].append((time, value))

        line = f.readline()

    assert(len(ret["points"]) == ret["no_points"])
    return ret

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
    outfile.write(_header.format(info["xmin"], info["xmax"], info["no_points"]))

    for i, (time, value) in enumerate(info["points"]):
        outfile.write(_point.format(i + 1, time, value))


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
