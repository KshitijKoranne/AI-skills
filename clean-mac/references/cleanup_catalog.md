# macOS Cleanup Catalog

Use this catalog to classify findings from `scripts/audit_mac.py`.

## Low-Risk Rebuildable Targets

These are usually safe to remove after confirming no related process is actively using them:

- `~/Library/Caches/*`
- `~/.cache/*`, except app-specific folders the user still cares about
- `~/.npm/_cacache`, `~/.npm/_npx`, `~/.npm/_logs`
- `~/.pnpm-store`, `~/.yarn/cache`, `~/Library/Caches/Yarn`
- `~/Library/Caches/ms-playwright`, `~/Library/Caches/ms-playwright-go`
- `~/Library/Caches/Homebrew`
- Python caches such as `~/Library/Caches/pip`
- Workspace generated folders: `node_modules`, `.next`, `.nuxt`, `.svelte-kit`, `.turbo`, `.vite`, `dist`, `build`, `coverage`, `target`
- Xcode generated data: `~/Library/Developer/Xcode/DerivedData`, `Archives`, unavailable simulator devices
- Android/Java generated caches: `~/.gradle/caches`, `~/.m2/repository` when dependencies can be redownloaded

Impact: apps or builds may be slower next time and may redownload dependencies.

## App Leftovers

Look for app artifacts when no matching `.app` exists in common app locations:

- `~/Library/Application Support/<App>`
- `~/Library/Caches/<bundle-id-or-app>`
- `~/Library/Logs/<App>`
- `~/Library/Preferences/<bundle-id>.plist`
- `~/Library/Preferences/ByHost/<bundle-id>*.plist`
- `~/Library/Saved Application State/<bundle-id>.savedState`
- `~/Library/WebKit/<bundle-id>`
- `~/Library/HTTPStorages/<bundle-id>`
- `~/Library/Cookies/<bundle-id>`

Cross-check installed apps under `/Applications`, `/System/Applications`, `/System/Library/CoreServices/Applications`, and `~/Applications`. Prefer exact app or bundle ID matches over fuzzy names.

## AI and Editor Artifacts

Common AI/editor storage folders:

- `~/Library/Application Support/Claude`
- `~/Library/Application Support/Codex`
- `~/Library/Application Support/Cursor`
- `~/Library/Application Support/Code`
- `~/Library/Application Support/Windsurf`
- `~/Library/Application Support/Trae`
- `~/Library/Application Support/Antigravity`
- `~/Library/Application Support/OpenCode`
- `~/Library/Application Support/dev.warp.Warp-Stable`

These may contain chats, uploaded file references, screenshots, workspace history, extensions, auth/session state, local runtimes, and caches. Caches are lower risk than full app-support folders. Removing app-support for an installed app can sign the user out, reset settings, remove extensions, or force runtime redownloads.

Claude VM bundles such as `~/Library/Application Support/Claude/vm_bundles` are local runtime packages. They can often be redownloaded/recreated, but deleting them can break or slow local agent/code features until Claude recreates them.

## Screenshot Locations

Check the screenshot location with:

```bash
defaults read com.apple.screencapture location
```

If unset, normal screenshots save to `~/Desktop`. The lower-right floating thumbnail disappearing usually means the screenshot has been saved. If the user uses Control with screenshot shortcuts or chooses Clipboard in Screenshot Options, a file may not be created.

Search common screenshot names:

- `Screenshot*`
- `Screen Shot*`
- `CleanShot*`

## Review-First Personal Data

Never auto-delete these without very explicit user selection:

- `~/Desktop`, `~/Downloads`, `~/Documents`, `~/Movies`, `~/Pictures`
- photo/video backups and exported archives
- `.dmg`, `.zip`, `.pkg`, installers unless the user confirms
- large files found by size search
- browser profiles, Mail, Messages, Photos libraries
- iCloud Drive, Google Drive, Dropbox, OneDrive, File Provider data

## Do Not Touch By Default

- `/System`, `/Library` system-owned content, and SIP-protected paths
- `~/Library/Keychains`
- `~/Library/Mail`
- `~/Library/Messages`
- `~/Library/Group Containers` unless a specific app leftover is clearly identified
- `~/Library/CloudStorage`
- active source repositories, `.git`, and user-authored project files
- Time Machine backups or local snapshots unless the user specifically asks
