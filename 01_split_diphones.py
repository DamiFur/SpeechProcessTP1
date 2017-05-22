"""This file splits every diphone in each wav."""
import glob
from audio import split_diphones


def main(wav_files):
    """Process each wav file."""
    for wav_path in wav_files:
        try:
            split_diphones(wav_path)
        except Exception:
            print("Missing textgrid for {}???".format(wav_path))

if __name__ == "__main__":
    main(glob.glob("wav/jmp/*.wav"))
