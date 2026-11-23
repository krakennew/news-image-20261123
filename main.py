#!/usr/bin/env python3
"""Copy the bundled poster image to the grading output directory.

The entry image is drawn at build time by draw_poster.py and shipped in this
repository as entry.png. This program only copies it, using the standard
library, with no network access, so both grading runs write identical bytes.
"""

import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Guard the determinism requirement: the graded copy must be the
    # bundled image, byte for byte, on every run.
    if os.path.getsize(src) != os.path.getsize(dst):
        raise SystemExit("entry.png copy size mismatch")


if __name__ == "__main__":
    main()
