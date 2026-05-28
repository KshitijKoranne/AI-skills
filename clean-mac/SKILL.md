---
name: clean-mac
description: Audit and clean macOS storage safely. Use when a user asks to free disk space, find removable caches, remove app leftovers after uninstalling apps, inspect AI/editor tool artifacts, clean Xcode/simulator/developer build outputs, locate screenshot clutter, or produce a confirmation-first cleanup plan for a Mac.
---

# Clean Mac

## Workflow

Use this skill as a confirmation-first macOS cleanup assistant.

1. Run the read-only audit script:

```bash
python3 scripts/audit_mac.py
```

Use `--json` only if structured post-processing is needed.

2. Summarize findings by risk:

- **Low risk**: rebuildable caches and build outputs such as `~/Library/Caches`, npm/npx caches, Playwright caches, Homebrew cache, Xcode DerivedData, unavailable simulator devices, old project `node_modules`, `.next`, `dist`, `build`, `target`.
- **App leftovers**: app-support/cache/preference/log folders for apps not installed in `/Applications`, `/System/Applications`, or `~/Applications`.
- **Review first**: personal folders, screenshots, Downloads, Desktop backups, app state with account/session data, AI/editor conversation or uploaded-file caches.
- **Do not touch by default**: system Apple data, currently installed app data, password/keychain data, Mail/Messages/Photos libraries, iCloud/File Provider data, browser profiles, active project source, Git history, Time Machine/local snapshots.

3. Show exact paths, sizes, and likely impact before deletion. Ask for explicit confirmation for each group unless the user has already named the group to remove.

4. Prefer deleting only these kinds of targets after confirmation:

- Rebuildable cache directories.
- Generated dependency/build folders inside workspaces.
- Confirmed app leftovers for apps not installed anymore.
- Empty or tiny preference/log files for confirmed uninstalled apps.

5. Re-measure with `df -h /System/Volumes/Data` and report before/after free space.

## Cleanup Catalog

Read `references/cleanup_catalog.md` when deciding whether a path is safe, risky, or likely app-specific. The catalog lists common macOS cleanup locations, AI/editor artifacts, developer caches, screenshot behavior, and app-leftover heuristics.

## Safety Rules

- Do not delete personal files without clear confirmation.
- Do not remove a folder just because it is large; explain the app/function impact.
- Treat AI/editor app-support folders as sensitive because they may include chats, uploaded screenshots/files, workspace metadata, extensions, auth state, and caches.
- For `rm -rf`, list exact paths in the user-visible plan or make it clear the deletion is limited to a confirmed category.
- If deletion fails because files are root-owned or protected, report the remnant and size; do not force admin cleanup unless the user asks.
- If the user wants a reusable/public workflow, keep scripts read-only by default and separate audit from deletion.
