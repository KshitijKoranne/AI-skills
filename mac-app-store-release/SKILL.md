---
name: "mac-app-store-release"
description: "Ship a Tauri (or other non-Xcode) macOS app to the Mac App Store and as a signed, notarized website DMG for your Apple developer account. Use for any Mac app submission, re-upload, or website download."
---

# Mac App Store + notarized DMG

Account facts (not secrets):
- Individual account, seller name "<your name>". Team ID `<TEAM_ID>`.
- Contact email for listings, support pages and review contact: <your contact email>. Ask for the review phone number; never guess.
- Notarization key (team-wide, works for every app): Key ID `<KEY_ID>`, Issuer `<ISSUER_ID>`, file `~/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8` on your Mac.
- Certificates already in your keychain (Xcode -> Settings -> Apple Accounts -> team -> Manage Certificates): Apple Development, Apple Distribution, Mac Installer Distribution, Developer ID Application. Renew there when they expire (Sep 2027).

## Mac App Store build (Tauri 2)

Add, keep minimal:
- `src-tauri/Entitlements.appstore.plist`: app-sandbox, network.client (if it uses network), files.user-selected.read-write (if it uses open/save panels), `com.apple.application-identifier` = `<TEAM_ID>.<bundle id>`, `com.apple.developer.team-identifier` = `<TEAM_ID>`.
- `src-tauri/Info.appstore.plist`: `ITSAppUsesNonExemptEncryption` false (HTTPS only).
- `src-tauri/tauri.appstore.conf.json` (merged with `--config`): minimumSystemVersion 12.0, bundleVersion "1" (bump every upload), signingIdentity "Apple Distribution", entitlements, infoPlist, `files: {"embedded.provisionprofile": "./embedded.provisionprofile"}`, copyright "<year> <your name>".
- git-ignore `src-tauri/embedded.provisionprofile` and `*.pkg`.
- Script `mas:build`: `tauri build --bundles app --target universal-apple-darwin --config src-tauri/tauri.appstore.conf.json && xcrun productbuild --sign "3rd Party Mac Developer Installer" --component src-tauri/target/universal-apple-darwin/release/bundle/macos/<App>.app /Applications <App>.pkg`
- Sandbox moves app data to `~/Library/Containers/<bundle id>`; fix any in-app text that names the old path.
- Keep web links out of the app window (Tauri `on_navigation` plugin that sends http(s) to the browser) and remove in-app mentions of other download channels.

## Apple website steps (do them in Chrome for him)

1. developer.apple.com -> Identifiers -> + -> App ID, explicit bundle ID, no capabilities.
2. Profiles -> + -> Distribution -> Mac App Store Connect -> Mac -> App ID -> Apple Distribution cert. Download, move to `src-tauri/embedded.provisionprofile`.
3. App Store Connect -> Apps -> + -> New App (macOS, name max 30 chars, check it is not taken, SKU like `<APP>-MAC-001`).

## Listing (App Store Connect)

- Copy must read as human-written. Description, promo text, keywords (100 chars, no spaces, no words from name/subtitle), subtitle, support/marketing/privacy URLs, version, copyright.
- Needs a live privacy policy and support page (static HTML in the website's `public/`, push before submitting).
- Screenshots: use the `store-screenshots` skill.
- Review notes: how to test in 30 s, no login, list the native features (answers guideline 4.2 "website wrapper" risk).
- App Information: category; Content Rights (third-party content -> yes, has rights, only with the owner's OK); Age rating: answer honestly (an RSS/web-content reader = Unrestricted Web Access yes -> 16+).
- App Privacy: "Data Not Collected" if true. Publish.
- Pricing: set price (give USD and INR). Availability: exclude China mainland for news/content apps.
- EU DSA: set trader or non-trader to match the account.
- Release: automatic after approval.

## Upload and submit

- You run `npm run mas:build` (Claude can't type in Terminal). Verify the bundle from the linked folder: Info.plist keys, entitlements strings, embedded.provisionprofile present.
- Upload with Transporter (Mac app, signed in by him): + -> Cmd+Shift+G path to .pkg -> Deliver.
- When Transporter says processed / "ready for internal testing": version page -> Add Build -> Save -> Add for Review -> Submit for Review. Ask him before the final submit if not already approved.

## Website DMG (signed + notarized)

Script `mac:release`:
```
APPLE_SIGNING_IDENTITY='Developer ID Application' APPLE_API_ISSUER=<ISSUER_ID> APPLE_API_KEY=<KEY_ID> APPLE_API_KEY_PATH=$HOME/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8 tauri build --target universal-apple-darwin --bundles dmg && D=$(ls src-tauri/target/universal-apple-darwin/release/bundle/dmg/*.dmg) && xcrun notarytool submit "$D" --key $HOME/.appstoreconnect/private_keys/AuthKey_<KEY_ID>.p8 --key-id <KEY_ID> --issuer <ISSUER_ID> --wait && xcrun stapler staple "$D" && spctl -a -t open --context context:primary-signature -v "$D"
```
- Not sandboxed; no entitlements needed. Host the DMG on GitHub Releases; the website links to releases/latest.
- Remove any "macOS will warn you" copy once the DMG is notarized.

## Working notes

- If the user is a non-programmer: give one copy-paste Terminal command at a time, short steps.
- Git in the linked folder leaves lock files; clean `.git/*.lock` and `.git/objects/*/tmp_obj_*` after commits. The user pushes git changes themselves.