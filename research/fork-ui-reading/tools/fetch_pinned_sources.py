#!/usr/bin/env python3
"""Fetch the pinned fork files listed in SOURCE_MANIFEST.json.

Files go to research/fork-ui-reading/downloaded_sources/ (git-ignored).
Requires Internet access. Does not modify firmware or tracked repo sources.

Exit code: 0 when every file was fetched and every known hash matched,
1 when any file failed. Files without a recorded blob_sha are fetched but
reported as UNVERIFIED.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "downloaded_sources"


def git_blob_sha(content: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(content)).encode() + b"\x00" + content).hexdigest()


def safe_relative(*parts: str) -> PurePosixPath:
    """Reject absolute paths and '..' so a manifest entry cannot escape DEST."""
    rel = PurePosixPath(*parts)
    if rel.is_absolute() or ".." in rel.parts or not rel.parts:
        raise ValueError(f"unsafe path: {rel}")
    return rel


def fetch(item: dict) -> str:
    owner, repo = item["repo"].split("/")
    rel = safe_relative(owner, repo, item["path"])
    url = ("https://raw.githubusercontent.com/" + quote(owner) + "/" + quote(repo) + "/"
           + item["commit"] + "/" + quote(item["path"], safe="/"))
    with urlopen(url, timeout=20) as response:
        content = response.read()
    expected = item.get("blob_sha")
    if expected and git_blob_sha(content) != expected:
        raise RuntimeError("blob SHA mismatch")
    target = DEST / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    return "ok" if expected else "UNVERIFIED"


def main() -> int:
    manifest = json.loads((ROOT / "SOURCE_MANIFEST.json").read_text("utf-8"))
    failures = 0
    unverified = 0
    for item in manifest["sources"]:
        label = item["repo"] + "/" + item["path"]
        try:
            status = fetch(item)
        except (URLError, OSError, RuntimeError, ValueError, KeyError) as err:
            failures += 1
            print(f"FAIL        {label}: {err}")
            continue
        unverified += status == "UNVERIFIED"
        print(f"{status:<11} {label}")
    total = len(manifest["sources"])
    print(f"\n{total - failures}/{total} fetched, {unverified} without a recorded hash, {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
