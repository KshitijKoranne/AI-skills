---
name: "store-screenshots"
description: "Make App Store / Mac App Store / Play Store marketing screenshots (framed, captioned, exact store sizes) and optional app preview videos for any app. Use whenever an app listing needs screenshots or a preview."
---

# Store screenshots

Use this for every app that goes to a store, without being asked again.

## Tool

AppShot (free, offline, MIT-style, renders HTML with Playwright): https://github.com/Gooreum/appshot

```bash
git clone --depth 1 https://github.com/Gooreum/appshot <scratch>/appshot
cd <scratch>/appshot && npm install --ignore-scripts
```

- If Chromium is preinstalled (e.g. /opt/pw-browsers), do not run `playwright install`. Patch `src/render.js`: `chromium.launch({ executablePath: process.env.PW_CHROMIUM || undefined })` and set `PW_CHROMIUM` to the chrome binary.
- Its SKILL.md is in Korean; the CLI is `node <appshot>/bin/appshot.mjs doctor|init|render`.

## Steps

1. **Raw screens.** Real app content, no placeholder data that impersonates real outlets.
   - Web-tech apps (Tauri, Electron, PWA): run the dev server, drive it with Playwright at 1440x900, deviceScaleFactor 2 -> 2880x1800. Shim any native bridge so the app shows its desktop mode. Never screenshot a marketing/landing page.
   - Native apps: simulator capture or PNGs from the user.
   - Take 4-5 screens that each show one idea (main view, search, focus mode, onboarding, settings).
2. **Init.** In a scratch project dir: `appshot init --platform macos|ios|android`, put screens in `screens/`.
3. **Brand.** Use the app's own colours and fonts. Fonts: `npm pack @fontsource/<font>`, then prepend `@font-face` rules with base64 data URIs to `<appshot>/templates/base.css` (GitHub raw downloads may be blocked). Set `theme.fontStack` to that font.
4. **Captions.** Headline 3-5 words, subhead one short sentence. Must read as written by a person: plain, concrete, a bit dry. No emoji, no "seamless/effortless/unlock/elevate", no repeated sentence patterns. Match the app's existing voice (README, landing page).
5. **Layouts.** Mostly `caption-top`; one `caption-bottom` for variety. Mac: window frame on (`deviceFrame: true`).
6. **Render and check.** `appshot render`, then build a contact sheet (PIL) and look at every image. Confirm size and RGB (no alpha).
7. **Show the user before uploading.** They pick changes; do not upload until approved.

## Store specs (check Apple/Google docs if unsure)

- Mac App Store: 16:10 - 1280x800, 1440x900, 2560x1600 or 2880x1800. 1-10 screenshots.
- iPhone: 6.9" 1290x2796 (or 6.5"). iPad 13" 2064x2752 if the app runs on iPad.
- Google Play: at least 2, 4+ recommended; avoid device frames.

## Uploading to App Store Connect (browser)

- Screenshots and previews are locked while a version is "Waiting for Review". To change them: App Review -> submission -> Cancel Submission (status becomes Developer Rejected), replace, then Add for Review -> Submit for Review. Ask the user first.
- Browser upload bridges cap ~10 MB per call: upload one file at a time. After all are in, click Save and reload; the saved order is upload order. Verify the order from the "Screenshots from Mac" list.
- Close the "App Previews, Screenshots, and Localizations" OK dialog if it blocks typing.

## App preview video (only if the user wants it)

- Record with Playwright `recordVideo` (size = store size). Add a small visible cursor dot via init script. Script a 15-30 s flow that shows real content; blur focus from inputs before pressing shortcut keys.
- If the viewport is smaller than the video size, crop the real area and scale up with ffmpeg.
- Encode: `ffmpeg -ss <trim> -i raw.webm -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -shortest -vf "fps=30,format=yuv420p" -c:v libx264 -crf 16 -c:a aac -movflags +faststart preview.mp4` (Apple wants an audio track). Mac preview: 1920x1080.

## Deliver

Save final PNGs (and video) into the project folder (e.g. `appstore/v2/`, git-ignored) and show them to the user.