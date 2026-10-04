---
name: "motion-film"
description: "Make short motion-graphics videos (app ads, promos, launch teasers, showreels, explainer clips) as MP4 with synced sound, rendered from code. Use for any request for an animated video, motion ad, reel, promo or teaser."
---

# Motion Film

Make a 6–60s motion-graphics film as an MP4 with its own soundtrack. You design every frame in code (HTML canvas), render it frame by frame with Playwright, make the sound with numpy, and join them with ffmpeg. Nothing is filmed or taken from stock.

Target quality: a studio spot. Each video has one strong idea, sharp timing, and a look that is different from the last video.

## 0. The rules that matter most

1. **Hook in the first 1.5 s.** Start with motion or tension, not a logo. The logo comes after you earn it.
2. **One idea per shot.** Only one hero moves at a time. The other elements stay still or move quietly.
3. **Every visual hit has a sound, and every sound has a visual.** Put the cuts on the beats of the tempo map.
4. **Linear motion only for mechanical things** (scrolling, conveyor belts, rotation that never stops). Everything else uses easing.
5. **Scenes flow into each other.** The last frame of one scene becomes the first frame of the next (match cut, shape fill, wipe). Avoid hard cuts to blank screens, except for a planned flash or glitch.
6. **Copy is human and true.** Use the brand's own words when it has them. Do not invent claims, prices, reviews or statistics. Invent generic names for sources and people, never real brands.
7. **Never repeat a look.** Read the motion log (section 2) and change at least 4 variety axes from the last film.
8. **The tempo fits the film.** Choose it from the mood and the length. Long films change tempo, and the motion changes speed with the music (section 3b).
9. **No labels about craft** (such as principle names or timecodes) in ads. Use them only when the user asks for a showreel.

## 1. Workflow

1. **Collect facts before you ask questions.**
   - Check memory and project docs for the product.
   - If the product has a site, look at it with Playwright (section 4): its fonts, colors, CSS variables, headline copy, features and URL. Also check the Vercel/GitHub connectors for the live domain.
2. **Ask once, only for what you cannot find** (one AskUserQuestion). Ask about aspect ratio and destination if they are not clear: 16:9 for YouTube/web, 9:16 for Reels/Shorts/TikTok, 1:1 or 4:5 for feed. Also ask about length and the call to action (CTA). If the user is away, use 16:9, 15–20 s and the site URL as the CTA, and say so.
3. **Pick the variety profile** (section 2), **the structure** (section 3) and **the tempo map** (section 3b). Write a beat sheet with exact times taken from the tempo map: scene, energy level, hero action, transition in and out, text, sound.
4. **Build** `film.js` from the engine (section 5). Use one function per scene, and make each scene a pure function of `t`.
5. **Look once** (section 7): render about 25 stills into a contact sheet, fix what you see, then look at one or two full-size stills.
6. **Render** the full film (it takes about 1.5 min for 18 s), then **make the audio** (section 6) and **mux** the two.
7. **Check** the duration, the audio peak, and one frame taken from the final MP4.
8. **Deliver** the file to `/mnt/user-data/outputs/<name>.mp4` with SendUserFile, and give a short beat-by-beat summary.
9. **Add a line to the motion log.**

## 2. Variety system (so that no two films look alike)

Before you design, read the log in the project doc `claude/motion-log.md` (use `Projects project_read`; create it if it is not there). After you deliver, add one line to it: `date | film | profile values`.

Pick one value on each axis. Change at least 4 axes from the previous entry, and do not reuse the previous structure.

| Axis | Options |
|---|---|
| Palette strategy | brand-strict · mono + 1 accent · duotone · full-saturation color blocks · dark neon-free night · paper/print · gradient-mesh · black & white + one flash color |
| Type personality | heavy grotesk · wide extended · condensed tall · editorial serif · mono/technical · handwritten/script · variable-weight morphing · type as texture |
| Motion physics | springy (outBack/elastic) · snappy UI (expo) · liquid (sine, slow in-out) · mechanical (linear + hard stops) · stepped/on-twos (hand-made, 12 fps holds) · weighty (gravity, bounces) |
| Structure | see section 3 |
| Transition family | shaped wipes · shape-grow fills · masks/reveals · match cuts · whip pans · glitch/slice · grid/tile · zoom-through · iris · push/slide stack |
| Camera language | locked-off flat · slow push-in · parallax layers · continuous one-take pan · 3D perspective (tunnel, tilt) · handheld micro-shake |
| Texture | clean vector · film grain · halftone dots · paper noise · scanlines · soft shadows/depth · outlined/wireframe |
| Tempo map | a single tempo (70–150 BPM) · half-time ↔ double-time switch · 2–4 sections with different tempos · accelerando build · slow → fast → slow arc (see section 3b). Never use the tempo map of the last film again. |
| Sound palette | punchy electronic · warm electric piano/lo-fi · orchestral hits (synth) · minimal clicks + sub · percussive/body · glitchy |
| Composition | centered symmetry · left-aligned editorial grid · full-bleed type · split screen · off-center with big negative space · modular grid |

Log so far:
- 2026-09-25 | Claude showreel | color blocks · heavy wide grotesk · springy · principle chapters · shape-grow fills · locked-off + tunnel · clean · 120 · punchy electronic · centered
- 2026-09-25 | Tilde ad | brand-strict · grotesk + script logo · snappy/liquid · problem→relief · shaped wave wipes · locked-off · clean + soft shadows · 120 half-time · chaos→warm EP · left-aligned editorial

## 3. Structures (the story)

For ads, choose one and do not repeat the last one used:

- **Problem → Relief:** the noise of the old way, a brand gesture clears it, calm, promises, CTA. (Used for Tilde.)
- **Transformation:** one object keeps morphing to tell the story (dot → icon → UI → logo). One continuous shape, with no cuts.
- **One-take journey:** a camera moves across a long, connected world. Each feature is a place on the way.
- **Kinetic manifesto:** type only, one short line per beat. Rhythm and scale do the work. Good for 6–10 s.
- **Before / After split:** a split screen or a wipe that you scrub back and forth between the two states.
- **Countdown / list:** "3 things…" with big numbers as the hero objects.
- **Product as hero:** abstract UI parts assemble into the idea of the product (no real screens needed), then an orbit and a close-up.
- **Question → Answer:** a big question on screen, the tension grows, and the answer is the product.
- **Loop:** the last frame matches the first frame, for social autoplay (6–10 s).

For a showreel: chapters, each showing one technique or principle, with a recall montage and a name card.

Timing skeleton for a 15–20 s ad: hook 0–3 s · reveal 3–5.5 s · proof/features 5.5–14.5 s (1.5–3 s each) · end card ≥ 3 s, with the CTA readable for at least 2 s.

Timing skeleton for a 30–60 s film: intro (slow, sparse) · build (medium, more layers) · peak (fastest, densest) · breath (slow, open space, 1 idea) · finale (fast or big) · end card (slow, resolved). Draw this energy curve before you write the beat sheet.

## 3b. Tempo map (the music and the motion change speed together)

Do not use one fixed BPM for every film. Choose the tempo from the mood, the length and the structure.

**Starting tempo by mood:**

| Mood | BPM |
|---|---|
| calm, premium, emotional | 70–95 |
| friendly, product, lifestyle | 100–118 |
| energetic, launch | 120–132 |
| urgent, sport, tech hype | 135–150 |

A half-time feel (drums at half speed, same BPM) gives weight without a slow tempo.

**Sections by length:**

| Length | Tempo sections |
|---|---|
| ≤ 10 s | one tempo |
| 15–25 s | one tempo, plus a possible half-time ↔ double-time switch at the reveal or the drop |
| 30–60 s | 2–4 sections with different tempos, following the energy curve |

**Motion follows the tempo of each section:**

| Section | Cuts | Moves | Easing | Stagger | Holds |
|---|---|---|---|---|---|
| Slow (≤ 95) | 1 per bar or fewer | long (40–90 f) | sine, cubic, gentle bezier | wide | long, with room to read |
| Medium (100–125) | 1 per 2 beats | 20–40 f | cubic, expo | 3–4 f | normal |
| Fast (≥ 128) | on each beat or half beat | 10–24 f | expo, back | 2 f | short, plus shake and flash on the hits |

**How to change tempo cleanly:**

- Change only on a bar line (every 4 beats). Make each section a whole number of bars.
- Choose one bridge:
  - riser, then one beat of silence, then the new tempo hits (the strongest)
  - half-time switch (easiest, because the grid does not change)
  - filter sweep down, then open up again
  - accelerando ramp for a build scene (use a short ramp section, one BPM per beat)
  - hard cut on an impact
- Keep the same key across sections. To lift the finale, go up by 2 semitones.
- A visual transition sits exactly on the tempo change. The new section looks different: another color, another camera, another motion physics.

**One source of truth.** Write the map once in `tempo.json` as `[[startSeconds, bpm], ...]`. For example, a 40 s film: `[[0, 84], [8.571, 128], [23.571, 76], [29.887, 140]]` (3 slow bars, 8 fast bars, 2 slow bars for the breath, then the fast finale). Both the animation and the audio read beat times from this file. Never hard-code `0.5`.

build.py puts `TEMPO` into the page (section 5).

In film.js (after `DUR`):
```js
const BEATS = []; TEMPO.forEach(([s, bpm], i) => { const e = TEMPO[i + 1]?.[0] ?? DUR; for (let t = s; t < e - 1e-6; t += 60 / bpm) BEATS.push(t); });
const beat = n => BEATS[n];                                         // time of beat n
const bpmAt = t => TEMPO.findLast(s => s[0] <= t)[1];
const pulse = t => { const b = BEATS.findLast(b => b <= t); return b === undefined ? 0 : Math.exp(-(t - b) * bpmAt(t) / 15); }; // 1 on the beat, about 0 one beat later
```
In audio.py:
```python
import json; TEMPO = json.load(open('tempo.json'))
BEATS = [t for i, (s, bpm) in enumerate(TEMPO) for t in np.arange(s, (TEMPO[i+1][0] if i+1 < len(TEMPO) else D) - 1e-6, 60/bpm)]
```
Put drums, hats and chord changes on `BEATS`, with a different drum pattern in each section. To check that a section is a whole number of bars: `abs(((end - start) * bpm / 60 / 4) % 1) < 0.01` (or > 0.99). The bar length is `240 / bpm` seconds.

## 4. Brand extraction (Playwright)

```js
// node shot.mjs <url>  -> screenshot + fonts + :root tokens
import { execSync } from 'child_process';
const { chromium } = await import(execSync('npm root -g').toString().trim() + '/playwright/index.mjs');
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
await p.goto(process.argv[2], { waitUntil: 'networkidle' }); await p.screenshot({ path: 'site.png' });
console.log(await p.evaluate(() => JSON.stringify({
  font: getComputedStyle(document.body).fontFamily, bg: getComputedStyle(document.body).backgroundColor,
  h1: [...document.querySelectorAll('h1,h2')].slice(0, 4).map(h => [h.textContent, getComputedStyle(h).fontFamily, getComputedStyle(h).color]),
  fonts: [...document.querySelectorAll('link[href*=font]')].map(l => l.href),
  root: [...document.styleSheets].flatMap(s => { try { return [...s.cssRules].filter(r => r.selectorText === ':root').map(r => r.cssText) } catch { return [] } }),
})));
await b.close();
```

Read the screenshot. Note the logo treatment, corner radius, shadow style, and the site's own headline and feature words. Get fonts with `npm pack @fontsource/<family>` and embed them as base64 (section 5). Google Fonts direct downloads can fail; npm works.

## 5. The engine

Files, all in a work folder: `tempo.json` (the tempo map), `build.py` (fonts + tempo + js → html), `film.js` (scenes), `render.mjs` (frames → mp4), `audio.py`.

### build.py
```python
import base64, glob
F = lambda n: base64.b64encode(open(glob.glob(f'fontsource-*/files/{n}-normal.woff2')[0], 'rb').read()).decode()
faces = [('A', 800, 'archivo-latin-800'), ('K', 700, 'caveat-latin-700')]  # (family alias, weight, file stem)
css = ''.join(f"@font-face{{font-family:{f};font-weight:{w};src:url(data:font/woff2;base64,{F(n)})}}" for f, w, n in faces)
W, H = 1920, 1080  # 1080x1920 for 9:16, 1080x1080 / 1080x1350 for feed
open('film.html', 'w').write(f"<!doctype html><meta charset=utf-8><style>{css}html,body{{margin:0}}</style>"
  f"<canvas id=c width={W} height={H}></canvas><script>const TEMPO={open('tempo.json').read()};{open('film.js').read()}</script>")
```
To get the files: `npm pack @fontsource/archivo && mkdir fontsource-archivo && tar xzf fontsource-archivo-*.tgz -C fontsource-archivo --strip-components=1`

### render.mjs
```js
// node render.mjs stills 0.5 3.2 ...   |   node render.mjs video <seconds>      (FPS=30 env to change rate)
import { execSync, spawn } from 'child_process'; import fs from 'fs';
const { chromium } = await import(execSync('npm root -g').toString().trim() + '/playwright/index.mjs');
const [mode, ...a] = process.argv.slice(2), FPS = +(process.env.FPS || 60);
const b = await chromium.launch(), p = await b.newPage();
p.on('pageerror', e => { console.error('PAGEERR', e.message); process.exit(1); });
await p.goto('file://' + process.cwd() + '/film.html');
await p.evaluate(async f => { await Promise.all([...document.fonts].map(ff => ff.load())); window.FPS = f; }, FPS);
const png = async f => Buffer.from((await p.evaluate(f => renderFrame(f), f)).split(',')[1], 'base64');
if (mode === 'stills') for (const t of a) fs.writeFileSync(`still_${t}.png`, await png(Math.round(t * FPS)));
else {
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < Math.round(+a[0] * FPS); f++) { if (!ff.stdin.write(await png(f))) await new Promise(r => ff.stdin.once('drain', r)); }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await b.close();
```

### film.js core (copy this, then write the scenes)
```js
const out = document.getElementById('c'), o = out.getContext('2d'), W = out.width, H = out.height;
const sc = document.createElement('canvas'); sc.width = W; sc.height = H; const x = sc.getContext('2d'); // scene buffer
const TAU = Math.PI * 2, cl = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const P = (t, a, b) => cl((t - a) / (b - a));            // progress of t through [a,b]
const lerp = (a, b, k) => a + (b - a) * k;
const hs = i => { const s = Math.sin(i * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); }; // deterministic random
const gauss = (t, c, w) => Math.exp(-(((t - c) / w) ** 2)); // impulse, e.g. squash at contact time c
const E = {
  outExpo: k => k >= 1 ? 1 : 1 - 2 ** (-10 * k),  inExpo: k => k <= 0 ? 0 : 2 ** (10 * k - 10),
  inOutExpo: k => k <= 0 ? 0 : k >= 1 ? 1 : k < .5 ? 2 ** (20 * k - 10) / 2 : (2 - 2 ** (-20 * k + 10)) / 2,
  outCubic: k => 1 - (1 - k) ** 3, inCubic: k => k ** 3, inOutCubic: k => k < .5 ? 4 * k ** 3 : 1 - (-2 * k + 2) ** 3 / 2,
  inOutSine: k => -(Math.cos(Math.PI * k) - 1) / 2,
  outBack: k => { const c = 1.7; return 1 + (c + 1) * (k - 1) ** 3 + c * (k - 1) ** 2; },
  outElastic: k => k <= 0 ? 0 : k >= 1 ? 1 : 2 ** (-10 * k) * Math.sin((k * 10 - .75) * TAU / 3) + 1,
  steps: (n, f) => k => Math.floor(f(k) * n) / n,       // on-twos / stepped look
};
function bez(x1, y1, x2, y2) { const f = (u, a, b) => 3 * a * u * (1 - u) ** 2 + 3 * b * u * u * (1 - u) + u ** 3;
  return k => { let lo = 0, hi = 1; for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; f(m, x1, x2) < k ? lo = m : hi = m; } return f((lo + hi) / 2, y1, y2); }; }
const bg = c => { x.fillStyle = c; x.fillRect(0, 0, W, H); };
const F = (w, s, fam) => { x.font = `${w} ${s}px ${fam}`; };
// mask-reveal a line of text: it slides up inside its own clip box
function maskText(str, tx, base, size, k, col, w = '800', fam = 'A', align = 'left') {
  if (k <= 0) return; x.save(); F(w, size, fam); x.textAlign = align; x.textBaseline = 'alphabetic';
  const tw = x.measureText(str).width, l = align === 'center' ? tx - tw / 2 : tx;
  x.beginPath(); x.rect(l - 20, base - size * 1.05, tw + 40, size * 1.35); x.clip();
  x.fillStyle = col; x.fillText(str, tx, base + (1 - k) * size * 1.2); x.restore();
}

// scene table: [endTime, fn]. Each fn(t) draws the whole frame into x.
const SCENES = [[3, s1], [5.5, s2] /* … */, [99, sEnd]];
const scene = t => SCENES.find(s => t < s[0])[1](t);
const DUR = 18;
// + the tempo helpers from section 3b (BEATS, beat, bpmAt, pulse)

// Real motion blur: average 6 sub-frames over a 180° shutter (half a frame).
window.renderFrame = f => {
  const t = f / FPS, S = 6;
  for (let k = 0; k < S; k++) {
    const st = cl(t + (k / (S - 1) - .5) / (2 * FPS), 0, DUR - 1e-3);
    x.save(); scene(st); x.restore();
    o.globalAlpha = 1 / (k + 1); o.drawImage(sc, 0, 0);
  }
  o.globalAlpha = 1;
  // overlays that must stay sharp (HUD, fine text) are drawn on o here, after the blur
  return out.toDataURL('image/png');
};
```

Rules for the engine:
- Scenes are **pure functions of t**. Do not keep state between frames. Use `hs(i)` for randomness, never `Math.random`.
- Take the times from the tempo map (`beat(n)`, section 3b), not from a fixed `0.5`. Scale the durations and staggers with `60 / bpmAt(t)`, so that a fast section also moves faster.
- When one scene wipes over the next, the **outgoing scene must still render under the wipe**. Call it inside the incoming scene, and extend its visibility window until the wipe is complete.
- A glitch or recall montage draws an earlier scene into `sc`, copies it to a second buffer, then draws slices back with offsets. Never use `drawImage` of a canvas onto itself.
- For a stepped or hand-made look, set `S = 1` (no blur) and quantize t: `t = Math.floor(t * 12) / 12`.
- For vertical 9:16, keep text out of the top 250 px and the bottom 400 px (the platform's interface covers them), and keep the side margins at 80 px or more.

## 6. Sound (audio.py)

The music and effects come from numpy with scipy filters, on the beat times from the same tempo map as the animation. Structure it as: an event list of `add(signal, time, gain)` calls, then the bed (bass + chords), then ducking on the kicks, then the master.

```python
import numpy as np, wave
from scipy.signal import butter, sosfilt
SR, D = 48000, 18; N = SR * D; mix = np.zeros(N); duck = np.ones(N); rng = np.random.default_rng(7)
def add(sig, at, g=1.0):  # safe for any length and for times near the end
    i = int(at * SR)
    if i < N: j = min(N, i + len(sig)); mix[i:j] += g * sig[:j - i]
def env(d, dec): tt = np.arange(int(d * SR)) / SR; return tt, np.exp(-tt / dec)
def kick(g=1, dec=.12): tt, e = env(.5, dec); return g * np.sin(2*np.pi*np.cumsum(45 + 110*np.exp(-tt/.03))/SR) * e
def noise(d, dec, lo, hi): tt, e = env(d, dec); return sosfilt(butter(2, [lo, hi], 'band', fs=SR, output='sos'), rng.standard_normal(len(tt))) * e
def tone(f, d, dec, harm=(1,)): tt, e = env(d, dec); return sum(np.sin(2*np.pi*f*h*tt)/(i+1) for i, h in enumerate(harm)) * e * np.minimum(1, tt/.004)
def sweep(d, lo, hi, g=1):  # whoosh / riser: band-pass noise swept block by block
    n = int(d*SR); r = np.linspace(0, 1, n)**2; s = rng.standard_normal(n); o = np.zeros(n)
    for k in range(0, n, 480):
        fc = lo + (hi-lo)*r[k]; o[k:k+480] = sosfilt(butter(2, [max(40, fc*.7), min(fc*1.4, 20000)], 'band', fs=SR, output='sos'), s[k:k+480])
    return g * o * np.sin(np.pi*np.linspace(0, 1, n))**.5
def ep(freqs, d, g=.1):  # warm electric-piano chord
    tt = np.arange(int(d*SR))/SR; e = np.exp(-tt/1.2)*np.minimum(1, tt/.01)*(1+.15*np.sin(2*np.pi*5*tt))
    return g*e*sum(np.sin(2*np.pi*f*tt)+.25*np.sin(4*np.pi*f*tt) for f in freqs)
# ... tempo map (section 3b), then events on BEATS ...
# ducking: for each kick time b: i=int(b*SR); duck[i:i+int(.15*SR)] *= np.linspace(.4, 1, int(.15*SR)); apply to the music bed only
mix = np.tanh(mix * 1.1); mix /= np.abs(mix).max() / .7
f = int(.5 * SR); mix[-f:] *= np.linspace(1, 0, f)
st = np.stack([mix, np.roll(mix, 14)], 1)  # small Haas widening
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
```

When you add two signals, give them the same duration (numpy cannot broadcast arrays of different lengths). Otherwise, make two `add` calls.

Sound design map:
- Kick: scene cuts and landings. Clap or rim: backbeats. Hats: energy (16ths = urgency).
- Whoosh or sweep: every wipe and big move. Its length is the length of the move, and it peaks at the moment of the cut.
- Riser: the 1–2 s before the big reveal. Impact (kick + sub + noise tail): the reveal and the logo.
- Pitched blips: small pops and staggered letters (rising pentatonic = happy).
- A pitch glide that follows the shape of a drawn mark is a memorable brand sting.
- **Silence is a tool.** Cut to near-silence right after chaos, and put the brand in that gap.
- Chords in major keys feel calm and friendly. Dissonant stabs and a rising drone feel stressful.
- Each tempo section gets its own drum pattern and density: sparse in slow sections, full in fast ones.

Mux, then check:
```bash
ffmpeg -y -loglevel error -i video.mp4 -i audio.wav -c:v copy -af volume=-3dB -c:a aac -b:a 256k -shortest -movflags +faststart /mnt/user-data/outputs/NAME.mp4
ffmpeg -i OUT.mp4 -af volumedetect -f null - 2>&1 | grep -E "max_volume|mean_volume"   # want max ≤ -1 dB, mean about -14 to -18 dB
```
AAC encoding raises the peaks by about 2 dB. That is why the mux lowers the volume by 3 dB.

## 7. Look once, then render

Render about 25 stills spread over the film, including each scene start, mid-point and end, and each transition mid-point. Make a contact sheet:
```bash
python3 -c "
from PIL import Image; import glob
fs=sorted(glob.glob('still_*.png'),key=lambda s:float(s[6:-4])); th=[Image.open(f).resize((480,270)) for f in fs]
g=Image.new('RGB',(2400,270*((len(th)+4)//5)))
[g.paste(t,((i%5)*480,(i//5)*270)) for i,t in enumerate(th)]; g.save('contact.png')"
```
Read it and check for:
- text that is clipped, overlaps, or is too small (body text at 1080p ≥ 30 px; key words ≥ 90 px)
- empty or dead frames
- a scene that disappears before its wipe finishes
- a pop or reveal without anticipation or overshoot
- two heroes that move at the same time

Fix the problems, look at one full-size still of the densest frame, then render. Do not loop on stills after this.

## 8. Motion design principles (apply all of them)

**The 12 animation principles, for graphics**
- *Squash & stretch:* scale along the velocity (stretch ≈ 1 + 0.4·v²) and squash at contact (use `gauss`). Keep the volume constant: sx = 1/sy.
- *Anticipation:* before a big move, move 5–15 % in the opposite direction for 4–10 frames.
- *Staging:* one focal point per moment. Dim, blur or still everything else.
- *Straight ahead vs pose to pose:* keyframe the poses (pose to pose), and use procedural simulation (straight ahead) for particles, falls and crumbles.
- *Follow-through & overlap:* parts stop at different times. Echoes or trailing copies lag 3–6 frames, and inner parts lag the outer ones.
- *Slow in / slow out:* ease out on entrances, ease in on exits, and ease in-out on moves between two rests.
- *Arcs:* natural paths are curved. Add a sine or parabola offset to straight moves.
- *Secondary action:* small supporting moves (orbiters, sparkles, marquee text) at low contrast.
- *Timing:* the number of frames sets the weight. Light objects move fast, heavy ones slowly and with a settle.
- *Exaggeration:* push scale, speed and color changes beyond what is real, on the key beats only.
- *Solid drawing:* keep a consistent perspective and light, and give shapes real volume (shadows, depth).
- *Appeal:* clear silhouettes, simple shapes, confident timing.

**Timing numbers at 60 fps** (at 30 fps, halve the frame counts; in slow or fast tempo sections, use the ranges in section 3b)
- Micro feedback (click, tick): 6–10 f. Pop in: 14–22 f. UI move: 18–30 f. Scene transition: 20–36 f. Big hero move: 30–60 f.
- Stagger between siblings: 2–5 f. Beyond 6 f it reads as separate events.
- Reading hold: at least 0.4 s + 0.3 s per word. End card: at least 2.5 s, with the CTA held for at least 2 s.
- Contrast of pace: follow each fast section with a hold or a slow section. A film that is all fast feels flat.

**Easing vocabulary**
- expo: UI, precise, premium. back: playful pop with overshoot. elastic: rubbery, use rarely. sine: liquid, calm. cubic: neutral.
- Custom bezier `(.83, 0, .17, 1)`: dramatic in-out. `(.2, .8, .2, 1)`: fast out, soft landing.
- Do not mix more than 2 or 3 easing families in one film. The easing is part of the brand's voice.

**Motion-graphics craft**
- *Motivated transitions:* each transition comes out of the content (the ball becomes the wipe, a shape grows to become the next background, a word zooms until its counter fills the frame).
- *Graphic continuity:* keep color, position or shape the same across a cut so the eye stays in the same place.
- *Kinetic type:* mask reveals, per-letter stagger, scale punch 1.3→1 on the beat, weight or width animation, typewriter with a cursor, split and slide, chromatic offset for impact. Keep type in its own clip box.
- *Hierarchy in time:* the headline lands first, the support text 0.2–0.3 s later, the details last.
- *Parallax:* 3+ depth layers that move at different speeds (for example 0.3×, 0.6× and 1×).
- *Camera:* a slow push-in (1.00→1.06 over a scene) adds life to static shots. Use shake only for chaos or impact, and let it decay fast.
- *Spacing charts and onion skin:* use them to check that the easing looks right, and show them when the subject is craft.
- *Rhythm:* place the hits on beats, the secondary actions on off-beats, and the fills on 16ths before the big moments.
- *Color script:* plan the background color of each scene as a sequence. Contrast between neighboring scenes makes the cuts clear.
- *Negative space:* a small hero with a lot of empty space often looks more premium than a full frame.
- *Texture:* grain (a noise canvas at 4–8 % alpha, re-seeded per frame) or halftone gives a crafted feel. Apply it after the blur.
- *Loops:* for social, make the last frame equal to the first frame.
- *Accessibility:* no full-screen strobe faster than 3 flashes per second, and good text contrast.

## 9. Technique library (what has worked; reuse and vary)

- Ball bounce with squash and stretch that stretches into a line, then a full-screen fill (a match cut into the next scene).
- Per-letter elastic drop, a wind-up squash, then a wave jump with color swap on landing.
- Polar morph between polygons: for a vertex list, `r(θ) = ra·rb·sin(b−a) / (ra·sin(θ−a) + rb·sin(b−θ))`, then lerp the radii between shapes.
- Orbiters on tilted ellipses with tapered trails (sample the past positions). Draw them in front of or behind the object according to sin(θ).
- A Truchet tile grid with rotation waves from different origins, then tiles that grow into squares for a full-frame fill.
- A graph editor with a bezier curve, a playhead, a ball on a track, and an onion-skin spacing chart.
- A perspective square tunnel with words punched on each beat and a chromatic offset.
- A glitch recall montage: earlier scenes, inverted slices, and color bars.
- A shaped wave wipe: fill the region behind a sine front and stroke the front with a thick accent band.
- Infinite-scroll chaos: card columns that accelerate, pop-ups on beats, shouted words on plates, rising shake.
- A brand mark that draws itself, and a wordmark revealed left to right as if handwritten.
- Items flying along brand-shaped paths into a list, with the rows shifting (newest first).
- A slot-machine counter that lands on the key number with overshoot.
- A form that breaks into pieces that fall with gravity and random spin.
- A list that scrolls fast and stops softly at an "end" marker.
- An end card with a CTA button that a cursor clicks: the hard shadow closes up when pressed.

Ideas not tried yet (prefer these to vary future films): particles that form words (sample the text pixels to get the targets), liquid metaballs, a 3D card flip (scaleX = cos θ), isometric worlds, a line-drawing (stroke-dash) illustration, a split-flap board, a halftone photo-like look, a mask made from a big word that reveals footage-like gradients, a morphing blob logo, pixel sorting, a paper cut-out with shadows, a clock or radial timeline, a map route line, data bars growing on the beat, a camera fly-through of a long horizontal world, a typographic zoom into a letter's counter.

## 10. Pitfalls already met

- Load all fonts before rendering, or Canvas silently falls back to another font.
- `sed` edits to JS are fragile. Use the Edit tool.
- Flash frames must also cover the frames where the scene returns early.
- Motion-blurred wave edges show soft bands. That is correct; do not "fix" it.
- Label numbers on tight tick marks overlap. Label every 3rd one.
- Keep the flight paths of moving items clear of text labels where you can.
- Both earlier films used 120 BPM. Start the next one from the mood table in section 3b.
- Deliver only the MP4. Do not add markdown readme files.