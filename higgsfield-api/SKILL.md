---
name: "higgsfield-api"
description: "Generate images/videos with the Higgsfield API (Seedance, Soul, any model) or add Higgsfield generation to a Python or TypeScript project."
---

# Higgsfield API

Docs: https://docs.higgsfield.ai/docs/llms.txt (shared: auth, polling, webhooks, errors).

## 0. Already set up on your Mac (do NOT redo)
- Key: `HF_KEY` and `HF_CREDENTIALS` exported in `~/.zshrc`.
- SDK: `higgsfield-client` installed for `/usr/bin/python3` (3.9, `--user`).
- Script: `~/.higgsfield/hf_gen.py` (source in section 3). Alias in `~/.zshrc`: `hf` = `python3 ~/.higgsfield/hf_gen.py`.
- Usage on the Mac: `hf <model-id> '<json args>' [out_dir]`. Values starting with `@` are local files (uploaded, replaced by URL). Output files download to out_dir.
- From a Claude session linked to the Mac: run through osascript `do shell script`, wrapped in `zsh -ic '...'` so `~/.zshrc` loads. Long jobs: `nohup ... > ~/.higgsfield/<name>.log 2>&1 &`, then poll the log with short calls (no long sleeps; osascript calls time out).
- Never print or tail `~/.zshrc`: it holds the secret. Check the key only with `echo ${HF_KEY:+set}`.
- Default save location: `~/Desktop` unless the user says otherwise.

## 1. Credentials (new machine / project)
- One value: `KEY_ID:KEY_SECRET` from https://console.higgsfield.ai/api-keys
- Python + cURL read `HF_KEY`. TypeScript reads `HF_CREDENTIALS`. Same value.
- Never hardcode it, never commit it, never put it in browser code. For a deployed app, set it as a server env var (Vercel / Coolify).

## 2. Find the model params
- Model ID = the path in the console URL. Examples: `bytedance/seedance-2.5/text-to-video`, `higgsfield-ai/soul/v2/standard`.
- Params page: `https://open.higgsfield.ai/models/<model-id>/api-reference` (console.higgsfield.ai redirects there). Fetch it before the first call to a new model. Do not guess params.

Seedance 2.5 text-to-video: `prompt` (required), `duration` 4-30 (default 5), `resolution` 480p|720p (720p), `aspect_ratio` 16:9|4:3|1:1|3:4|9:16|21:9 (16:9), `output_format` mp4|mov, `generate_audio` bool (true). Priced per second of video. Output: `video.url`.

Soul 2 standard (image): `prompt` (required), `batch_size` 1|4, `resolution` 720p|1080p, `aspect_ratio` (default 4:3), `enhance_prompt` bool (true), `seed` 1-1000000, `style_id`. Output: `images[].url`.

Give cost in USD + INR when asked. State the estimated cost before a paid run the user did not already approve.

## 3. Script source (install on a new machine or the cloud container)
`pip install higgsfield-client` (add `--break-system-packages` in the cloud container). Save as `hf_gen.py`:

```python
"""Usage: python hf_gen.py <model-id> '<json args>' [out_dir]
Arg values starting with "@" are local files: uploaded, replaced by URL."""
import json, os, sys, urllib.request
import higgsfield_client as hf

def urls(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "url" and isinstance(v, str): yield v
            else: yield from urls(v)
    elif isinstance(o, list):
        for v in o: yield from urls(v)

model, args = sys.argv[1], json.loads(sys.argv[2])
out = sys.argv[3] if len(sys.argv) > 3 else "."
args = {k: hf.upload_file(v[1:]) if isinstance(v, str) and v.startswith("@") else v for k, v in args.items()}
res = hf.subscribe(model, arguments=args,
                   on_enqueue=lambda rid: print("request_id:", rid, file=sys.stderr),
                   on_queue_update=lambda s: print("status:", type(s).__name__, file=sys.stderr))
print(json.dumps(res, indent=2))
os.makedirs(out, exist_ok=True)
for u in dict.fromkeys(urls(res)):  # ponytail: dedupe, keep order
    p = os.path.join(out, u.split("?")[0].rsplit("/", 1)[-1])
    urllib.request.urlretrieve(u, p)
    print("saved:", p, file=sys.stderr)
```

Example:
```bash
hf bytedance/seedance-2.5/text-to-video '{"prompt":"A cinematic scene at sunset","duration":5,"aspect_ratio":"9:16"}' ~/Desktop
```
- Video runs take minutes; image runs under a minute. Note the `request_id`.
- In the cloud container, the output CDN may be blocked by the network allowlist. Then give the user the URL from the JSON, or run on the Mac.

## 4. Add to a project
Server-side only. Pick the SDK that matches the project.

Python:
```python
import higgsfield_client
res = higgsfield_client.subscribe("bytedance/seedance-2.5/text-to-video", arguments={"prompt": "..."})
video_url = res["video"]["url"]   # images: res["images"][0]["url"]
```
Long jobs / workers: `ctl = higgsfield_client.submit(model, arguments=..., webhook_url=...)`, then `status(request_id=)`, `result(request_id=)`, `cancel(request_id=)`. Uploads: `upload_file(path)` returns a URL.

TypeScript / Node (`npm install @higgsfield/client`):
```ts
import { config, higgsfield } from "@higgsfield/client/v2";
config({ credentials: process.env.HF_CREDENTIALS });
const r = await higgsfield.subscribe("bytedance/seedance-2.5/text-to-video",
  { input: { prompt: "..." }, withPolling: true });
if (r.status === "completed") console.log(r.video?.url);
```
The TS v2 client blocks browser use. In Next.js, call it from a route handler / server action only.

Raw HTTP: `POST https://api.higgsfield.ai/<model-id>` with header `Authorization: Key $HF_KEY` and JSON body = params. Response gives `request_id`, `status_url`, `cancel_url`. Poll `status_url` with backoff.

## 5. Rules
- Statuses: queued, in_progress, completed, failed, nsfw, canceled. Handle failed + nsfw, not only completed.
- Output URLs live at least 7 days. Copy to own storage if the app keeps them.
- Cancel works only while queued.
- Errors to catch (Python): `CredentialsMissedError`, `InsufficientCreditsError`, `HiggsfieldClientError`.