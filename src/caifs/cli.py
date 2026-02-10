"""Thin wrapper that execs the vendored caifs shell script."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_VENDOR_DIR = Path(__file__).parent / "_vendor"


def main() -> int:
    caifs_bin = _VENDOR_DIR / "bin" / "caifs"
    if not caifs_bin.exists():
        print(
            "caifs: vendored binary not found. Run scripts/vendor.sh first.",
            file=sys.stderr,
        )
        return 1

    env = os.environ.copy()
    if "CAIFS_LOCAL_COLLECTIONS" not in env:
        env["CAIFS_LOCAL_COLLECTIONS"] = str(_VENDOR_DIR / "collections")

    result = subprocess.run(
        ["sh", str(caifs_bin), *sys.argv[1:]],
        env=env,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
