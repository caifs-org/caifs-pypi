from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from caifs.cli import _VENDOR_DIR, main


def test_main_returns_error_when_vendor_missing(tmp_path: Path) -> None:
    """main() should return 1 when the vendored binary doesn't exist."""
    with patch("caifs.cli._VENDOR_DIR", tmp_path):
        assert main() == 1


def test_collections_env_set(tmp_path: Path, monkeypatch: object) -> None:
    """CAIFS_LOCAL_COLLECTIONS should point to _vendor/collections/."""
    vendor = tmp_path / "vendor"
    bin_dir = vendor / "bin"
    bin_dir.mkdir(parents=True)
    caifs_bin = bin_dir / "caifs"
    # Write a script that prints the env var
    caifs_bin.write_text('#!/bin/sh\necho "$CAIFS_LOCAL_COLLECTIONS"')

    captured_env: dict[str, str] = {}

    def fake_run(cmd: list[str], *, env: dict[str, str]) -> object:
        captured_env.update(env)

        class Result:
            returncode = 0

        return Result()

    with (
        patch("caifs.cli._VENDOR_DIR", vendor),
        patch("caifs.cli.subprocess.run", fake_run),
    ):
        main()

    assert captured_env["CAIFS_LOCAL_COLLECTIONS"] == str(vendor / "collections")


def test_collections_env_not_overridden(tmp_path: Path, monkeypatch: object) -> None:
    """User-set CAIFS_LOCAL_COLLECTIONS should be respected."""
    import os

    vendor = tmp_path / "vendor"
    bin_dir = vendor / "bin"
    bin_dir.mkdir(parents=True)
    (bin_dir / "caifs").write_text("#!/bin/sh\ntrue")

    captured_env: dict[str, str] = {}

    def fake_run(cmd: list[str], *, env: dict[str, str]) -> object:
        captured_env.update(env)

        class Result:
            returncode = 0

        return Result()

    with (
        patch("caifs.cli._VENDOR_DIR", vendor),
        patch("caifs.cli.subprocess.run", fake_run),
        patch.dict(os.environ, {"CAIFS_LOCAL_COLLECTIONS": "/custom/path"}),
    ):
        main()

    assert captured_env["CAIFS_LOCAL_COLLECTIONS"] == "/custom/path"


def test_vendor_dir_points_to_package() -> None:
    """_VENDOR_DIR should be inside the caifs package."""
    assert _VENDOR_DIR.name == "_vendor"
    assert _VENDOR_DIR.parent.name == "caifs"
