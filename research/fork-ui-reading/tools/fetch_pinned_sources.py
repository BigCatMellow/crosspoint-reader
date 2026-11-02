#!/usr/bin/env python3
"""Fetch pinned upstream files to research/downloaded_sources only.

Requires Internet access; does not modify runtime firmware or repo sources.
"""
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
import hashlib
import json

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "SOURCE_MANIFEST.json").read_text("utf-8"))
for item in manifest["sources"]:
    owner, repo = item["repo"].split("/")
    rel = item["path"]
    url = "https://raw.githubusercontent.com/" + quote(owner) + "/" + quote(repo) + "/" + item["commit"] + "/" + quote(rel, safe="/")
    with urlopen(url, timeout=20) as response:
        content = response.read()
    if item["blob_sha"]:
        digest = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\x00" + content).hexdigest()
        if digest != item["blob_sha"]:
            raise RuntimeError("Unexpected blob SHA: " + item["repo"] + "/" + rel)
    path = root / "downloaded_sources" / owner / repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    print(item["repo"], rel, len(content))
