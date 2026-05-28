#!/usr/bin/env python3
"""Read-only macOS storage audit for the clean-mac skill."""

from __future__ import annotations

import argparse
import json
import os
import plistlib
import subprocess
from pathlib import Path


HOME = Path.home()
APP_DIRS = [
    Path("/Applications"),
    Path("/System/Applications"),
    Path("/System/Library/CoreServices/Applications"),
    HOME / "Applications",
]

APP_SUPPORT_CANDIDATES = [
    "Cursor",
    "Code",
    "dev.warp.Warp-Stable",
    "Windsurf",
    "Trae",
    "Antigravity",
    "Docker Desktop",
    "GitHub Desktop",
    "Riot Games",
    "riot-client-ux",
    "LibreOffice",
    "CleanMyMac X",
    "BatFi",
    "SuperAnnotate",
    "every-pdf",
    "float-note",
    "Ollama",
    "Godot",
    "Samsung",
    "Samsung Magician",
]

REBUILDABLE_PATHS = [
    "~/Library/Caches",
    "~/.cache",
    "~/.npm",
    "~/.pnpm-store",
    "~/.yarn",
    "~/Library/Caches/ms-playwright",
    "~/Library/Caches/Homebrew",
    "~/Library/Developer/Xcode/DerivedData",
    "~/Library/Developer/Xcode/Archives",
    "~/Library/Developer/CoreSimulator/Devices",
    "~/.gradle/caches",
    "~/.m2/repository",
    "~/.cargo/registry",
    "~/.cargo/git",
]

PERSONAL_REVIEW_PATHS = [
    "~/Desktop",
    "~/Downloads",
    "~/Documents",
    "~/Movies",
    "~/Pictures",
]

AI_EDITOR_PATHS = [
    "~/Library/Application Support/Claude",
    "~/Library/Application Support/Codex",
    "~/Library/Application Support/Cursor",
    "~/Library/Application Support/Code",
    "~/Library/Application Support/Windsurf",
    "~/Library/Application Support/Trae",
    "~/Library/Application Support/Antigravity",
    "~/Library/Application Support/OpenCode",
    "~/Library/Application Support/dev.warp.Warp-Stable",
]


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        return ""
    except FileNotFoundError:
        return ""


def expand(path: str) -> Path:
    return Path(os.path.expanduser(path))


def du_bytes(path: Path) -> int | None:
    if not path.exists():
        return None
    output = run(["du", "-sk", str(path)])
    if not output:
        return None
    try:
        return int(output.split()[0]) * 1024
    except (ValueError, IndexError):
        return None


def human_size(size: int | None) -> str:
    if size is None:
        return "-"
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{size} B"


def installed_apps() -> dict[str, str]:
    apps: dict[str, str] = {}
    for root in APP_DIRS:
        if not root.exists():
            continue
        for app in root.rglob("*.app"):
            if app.is_dir():
                name = app.stem.lower()
                apps[name] = str(app)
                bundle_id = bundle_identifier(app)
                if bundle_id:
                    apps[bundle_id.lower()] = str(app)
    return apps


def bundle_identifier(app: Path) -> str | None:
    info = app / "Contents" / "Info.plist"
    if not info.exists():
        return None
    try:
        with info.open("rb") as f:
            data = plistlib.load(f)
        value = data.get("CFBundleIdentifier")
        return value if isinstance(value, str) else None
    except Exception:
        return None


def likely_installed(candidate: str, apps: dict[str, str]) -> bool:
    normalized = candidate.lower()
    aliases = {
        "code": ["visual studio code", "com.microsoft.vscode"],
        "dev.warp.warp-stable": ["warp", "dev.warp.warp-stable"],
        "docker desktop": ["docker", "com.electron.dockerdesktop"],
        "github desktop": ["github desktop", "com.github.githubclient"],
        "cleanmymac x": ["cleanmymac", "com.macpaw.cleanmymac4"],
    }
    names = [normalized, *aliases.get(normalized, [])]
    return any(name in apps for name in names)


def entry(path: Path, category: str, risk: str, note: str) -> dict[str, object]:
    return {
        "path": str(path),
        "size_bytes": du_bytes(path),
        "category": category,
        "risk": risk,
        "note": note,
    }


def collect() -> dict[str, object]:
    apps = installed_apps()
    results: dict[str, object] = {
        "disk": run(["df", "-h", "/System/Volumes/Data"]) or run(["df", "-h", "/"]),
        "installed_app_count": len({v for v in apps.values()}),
        "sections": {},
    }
    sections: dict[str, list[dict[str, object]]] = {}

    sections["rebuildable"] = [
        entry(expand(path), "rebuildable", "low", "Usually removable; may be recreated or redownloaded.")
        for path in REBUILDABLE_PATHS
        if expand(path).exists()
    ]

    app_support = HOME / "Library" / "Application Support"
    leftovers = []
    for name in APP_SUPPORT_CANDIDATES:
        path = app_support / name
        if path.exists() and not likely_installed(name, apps):
            leftovers.append(entry(path, "app-leftover", "medium", "App does not appear installed in common app locations."))
    sections["app_leftovers"] = leftovers

    sections["ai_editor_state"] = [
        entry(expand(path), "ai-editor-state", "review", "May include chats, uploaded files, settings, auth, extensions, runtimes, or caches.")
        for path in AI_EDITOR_PATHS
        if expand(path).exists()
    ]

    sections["personal_review"] = [
        entry(expand(path), "personal-review", "review", "Personal files; inspect before deleting.")
        for path in PERSONAL_REVIEW_PATHS
        if expand(path).exists()
    ]

    sections["screenshots"] = screenshot_findings()
    results["sections"] = sections
    return results


def screenshot_findings() -> list[dict[str, object]]:
    location = run(["defaults", "read", "com.apple.screencapture", "location"])
    base = Path(location) if location else HOME / "Desktop"
    findings = []
    if base.exists():
        matches = []
        for pattern in ("Screenshot*", "Screen Shot*", "CleanShot*"):
            matches.extend(base.glob(pattern))
        total = sum((du_bytes(path) or 0) for path in matches if path.is_file())
        findings.append({
            "path": str(base),
            "size_bytes": total,
            "category": "screenshots",
            "risk": "review",
            "note": f"Screenshot save location; found {len(matches)} usual screenshot-named files.",
        })
    return findings


def print_markdown(data: dict[str, object]) -> None:
    print("# macOS cleanup audit")
    print()
    disk = str(data.get("disk") or "").splitlines()
    if disk:
        print("## Disk")
        print("```")
        print("\n".join(disk))
        print("```")
        print()
    sections = data["sections"]
    assert isinstance(sections, dict)
    for name, items in sections.items():
        print(f"## {name.replace('_', ' ').title()}")
        if not items:
            print("No findings.")
            print()
            continue
        sorted_items = sorted(items, key=lambda item: int(item.get("size_bytes") or 0), reverse=True)
        print("| Size | Risk | Path | Note |")
        print("| ---: | --- | --- | --- |")
        for item in sorted_items:
            print(
                f"| {human_size(item.get('size_bytes'))} | {item['risk']} | `{item['path']}` | {item['note']} |"
            )
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only macOS cleanup audit.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    args = parser.parse_args()
    data = collect()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print_markdown(data)


if __name__ == "__main__":
    main()
