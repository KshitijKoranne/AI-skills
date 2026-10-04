---
name: vps-maintenance
description: "Safe VPS maintenance: update panel, proxy, databases, services and OS; back up; remove unused apps and DNS; fix SSL/proxy errors, backup alerts and monitors. Any self-hosted server."
---

# VPS maintenance

Use this skill when the user asks to maintain, update, clean up or fix a self-hosted server (VPS) or its panel (Coolify, Dokploy, CapRover, Portainer, plain Docker, and similar). It is a general procedure, not a guide for one app.

The work has 9 phases. Do them in order. Never skip phase 1 (inventory) or phase 3 (backups). Phase 4 (updates) runs on EVERY maintenance, even when the user asks only for a clean-up: always check for updates and report them.

## Golden rules

1. Read first, change later. Build the full inventory before you touch anything.
2. Never delete on your own judgment. Every delete (app, database, volume, DNS record, monitor, repo, local file) needs a clear "yes" from the user for that item.
3. Back up before every risky step (update, delete, schema change). Verify each backup: status = success, size is realistic, and the off-site copy exists if configured.
4. Never reveal or type secrets. List env var KEYS only. Do not request revealed values (DATABASE_URL, passwords, tokens). Never type a bot token, API key or password into a form. Fill every other field, then ask the user to paste the secret, test and save.
5. Verify after every change: resource list, HTTP status codes, certificate, logs.
6. Update one component at a time. Verify it before you start the next one.
7. Do not publish things for the user (for example, a new public GitHub repo) without explicit permission.
8. Do not delete the user's local files, even when they look old. Report them instead.
9. Do not guess what is "unused". Things that look idle can still be critical. Example: a static privacy-policy page that an App Store listing needs.
10. When the user's answer rests on a wrong belief, correct it with facts. Only act on what they actually chose.
11. Keep replies short and step-wise. Follow the user's saved style preferences.

## Tools: pick the best access path

Check which tools exist before you start. Use the most direct, most structured tool first.

| Need | First choice | Fallback |
|---|---|---|
| Panel data and actions | Panel MCP (for example Coolify MCP: overview, list, get, env_vars keys, storages, deployments, backups, logs, delete, control) | Panel web UI in the browser |
| Panel UI-only actions ("Back up now", "Upgrade", "Docker cleanup", proxy restart) | Claude in Chrome extension | AppleScript Chrome control (`execute_javascript`) on the user's Mac |
| DNS lookups, curl, openssl | Shell on the user's Mac (`osascript do shell script` with dig/curl/openssl) | Cloud sandbox shell. Its proxy often blocks DoH and arbitrary hosts. |
| DNS provider changes | Provider MCP if it has record tools | Provider dashboard in the user's logged-in browser |
| Latest versions and release notes | WebSearch / WebFetch (GitHub releases, Docker Hub tags, vendor changelog) | Ask the user |
| Host OS packages, Docker engine, reboot | Panel host terminal or SSH (ask the user for access) | Tell the user the exact commands to run |
| Git hosting checks | `gh` CLI on the user's Mac (`export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH`) | GitHub web |
| Finding local source code | `mdfind` on the Mac | Ask the user |
| Command inside a container | Panel feature that execs in the container (Coolify: scheduled task `run_once`, container = app uuid) | Panel terminal |

Browser tips (important):
- If the Chrome extension is "not connected", the AppleScript Chrome tools still work (list tabs, open URL, run JS, read text).
- `open_url` with `new_tab:false` changes the ACTIVE tab. That may be the user's tab. Open your own tab with `new_tab:true`, get its id with `get_current_tab`, and always pass `tab_id`.
- Top-level `await` in AppleScript JS returns "missing value". So can `const`/`let` names that were already declared in an earlier call. Use `var`, or wrap the code in a function. For async work, store the result in `window.__x`, then read it in a second call.
- Do not trigger native `alert/confirm` dialogs. In-page modals (Bootstrap, Livewire) are fine. Click the button inside the visible modal (`.modal.show button`).
- Vue/React inputs need the native value setter plus `input` and `change` events, or the form will not see the value.
- Pages built with Livewire may need 1 to 3 seconds before buttons exist. Re-query instead of failing.
- In a logged-in dashboard tab, same-origin `fetch(..., {credentials:'include'})` can call that dashboard's own API (for example Vercel `/api/v4/domains/<d>/records`). Use this only for actions the user approved.
- Close every tab you opened. Put the user's own tabs back where they were.

## Phase 1: Inventory (read-only)

Collect all of this before you ask the user anything:

1. Panel version and "update available" state. Read it from the UI header too, because the API version can be cached.
2. All resources: name, type (app, service or stack, database), status, domains, git repo and branch, description, created date.
3. For each app: env var KEYS (look for DATABASE_URL, REDIS_URL, auth provider keys such as CLERK_*, payment keys), persistent storages and volumes, the last deployments and their commit SHAs, and the build pack or base image.
4. For each database: which apps use it (only apps with a DB URL key can; a database with no public port can only be used by apps on the same server or network), the image and tag, backup schedules, executions and sizes. A 3 KB dump of a "main" database often means only the default DB is backed up.
5. For each multi-container service: the sub-containers, their images and tags, and state. A service that exited weeks ago with a locally built image is usually dead.
6. Version table for Phase 4: panel, panel agents (for example Sentinel, helper image), reverse proxy (Traefik or Caddy), every database image, every service image, Docker engine, host OS. Note if a tag is pinned (`postgres:18.1`), floating (`postgres:18-alpine`) or `latest`.
7. Server health: unhealthy resources, disk use, and Docker cleanup settings (does it delete volumes? networks? retained images?).
8. Backups: the instance (panel) backup schedule, each database schedule, S3/R2 storage links, and failure messages in execution records.
9. DNS for every domain the server uses:
   - Nameservers per apex (`dig +short NS example.com`) tell you the provider. `vercel-dns.com` = Vercel, `dns-parking.com` = Hostinger, `cloudflare.com` = Cloudflare, and so on.
   - The A/AAAA/CNAME for every host. Mark each one: points to the VPS IP, points to another platform (for example Vercel edge IPs 64.29.x.x or 216.198.x.x), or does not resolve.
   - The full record list from the provider. Find records that point to the VPS but match no resource (stale). Find third-party records (auth, email, verification) that belong to apps you may retire.
   - Wildcard records (`*` ALIAS/CNAME). If an explicit record is deleted, the host falls back to the wildcard target.
10. Other platforms that may host the same app (Vercel or Netlify project lists). The same name on two platforms is a common source of confusion. Also note platform warnings you see (for example "Node.js 20 builds fail from <date>").
11. Monitoring: uptime monitors, whether alerts are set up and to where, and dashboards (Homepage) that list services.
12. Source repos: confirm each repo still exists (`gh repo list <owner> --json name`). A missing repo means the app cannot redeploy or restart. On some panels "restart" also runs `git ls-remote`.

Make a short table for yourself: resource → domain(s) → DNS provider → depends on → holds data? → image:tag → status → notes. Use it for the questions and the final report.

## Phase 2: Ask the user (AskUserQuestion)

- Put the explicit requests first: "Confirm: delete A, B, C with their data volumes?" Mention the side effects in the option text (for example "also deletes its database").
- For "anything else I may not need", group candidates into multi-select questions with at most 4 options each. Add short context to each option: domain, status, "also exists on Vercel", "no real domain".
- Tell the user which items you will keep, and why.
- Show the available updates (from Phase 4, step 1) grouped by risk: safe patch/minor, needs care (major, database, proxy), needs host access or downtime (OS, Docker engine, reboot). Ask which to apply now. Recommend the safe group.
- Ask separately about stale DNS records, third-party records linked to removed apps, and data export before a delete.
- If an answer is free text, read it carefully. It may change the plan.

## Phase 3: Pre-flight backups

1. Confirm that no deployment is running.
2. For each database with real data, trigger "Back up now". Check the new execution: status success, size close to earlier runs, `s3_uploaded` true if S3 is on.
3. Trigger the panel's own instance backup and verify it the same way (local and S3 availability).
4. For services that keep data in volumes (for example monitoring or analytics), check they have a DB backup or a volume backup before you update them.
5. Write down the paths and times of these backups, and the current image tags, for rollback.

## Phase 4: Check and apply updates (every run)

### 4.1 Find what is out of date

For each row of the version table, find the latest stable version:
- Panel: its own update screen (Coolify: Settings → Updates, or "Update available" in the header) and its GitHub releases.
- Reverse proxy: panel proxy page (Coolify: Server → Proxy) and Traefik/Caddy releases.
- Service images: GitHub releases or Docker Hub tags of the image (for example `louislam/uptime-kuma`, `umami-software/umami`, `gethomepage/homepage`).
- Database images: official image tags. Separate patch/minor (for example 16.4 → 16.6) from major (16 → 17).
- Docker engine and OS: host terminal (`docker version`, `apt list --upgradable`, `cat /var/run/reboot-required`).
- App base runtimes: end-of-life notices (Node, Python, PHP). Report them. Do not change app code unless the user asks.

For every available update, read the release notes for EVERY version in between. Look for breaking changes, manual steps, config or env renames, minimum versions of other parts, and new mandatory agents. A release from the last day or two has less field testing. Say so.

Classify each update:
- Safe: patch or minor, no breaking notes, stateless or backed up.
- Care: major version, database, reverse proxy, anything with breaking notes.
- Downtime: Docker engine, kernel, OS reboot. These restart every container.

### 4.2 Order of work

Apply only what the user approved, in this order. Verify after each step.
1. Panel (control plane). Coolify updates do not restart user apps.
2. Panel agents and helpers, if the panel does not update them itself.
3. Reverse proxy. A proxy restart drops all sites for a few seconds. Warn the user and do it once.
4. Database minor/patch updates.
5. Service images (monitoring, analytics, dashboards, tools).
6. Database major updates, only as a separate, planned job (see below).
7. OS packages, Docker engine, reboot: last, in a window the user accepts.

### 4.3 How to update each part

Panel:
1. Use the official UI path (Coolify: Settings → Updates → Upgrade now). Read the confirmation modal and confirm the target version before you click.
2. Poll every 60 to 90 seconds. "Reconnecting" during an upgrade is normal. Wait for "up to date".
3. Verify the version in the UI header after a full reload, then check all resources and sites.

Service with a pinned tag:
1. Note the current tag. Back up its data.
2. Change the image tag in the service compose or config to the new version.
3. Redeploy or restart with image pull. Watch the logs until the app reports ready.
4. Check the site and its health. To roll back, set the old tag and redeploy.

Service with `latest` or a floating tag:
1. Restart with "pull latest image" (Coolify MCP: `control` restart with `pull_latest: true` for services).
2. Verify as above. Suggest pinning a version, so updates are deliberate.

Database minor/patch:
1. Fresh verified backup first.
2. Update the tag within the same major (or restart a floating major tag with pull).
3. Check DB logs for a clean start, then check the logs of the apps that use it.

Database major (for example PostgreSQL 16 → 17):
1. Never change the major tag on the existing data volume. The data format is not compatible and the database will not start.
2. Plan: full dump → create a new database resource on the new major → restore the dump → point the app to the new DB (with the user, because this changes a secret) → test → keep the old DB stopped for some days → delete it only with approval.
3. MySQL/MariaDB majors may need `mariadb-upgrade` or `mysql_upgrade`. Read the vendor guide.

OS and Docker engine (needs host access):
1. Ask the user for terminal or SSH access, or give them the exact commands.
2. `apt update && apt list --upgradable`. Show the list. Apply security updates first: `apt upgrade -y`.
3. A Docker engine upgrade restarts all containers. Check `restart: unless-stopped/always` so they come back.
4. If `/var/run/reboot-required` exists, plan the reboot with the user. After the reboot, check the panel, the proxy and every site.

If an update fails: stop, do not try the next component, roll back to the noted tag or backup, and report.

## Phase 5: Remove what the user approved

Order:
1. Apps first, then databases used only by those apps, then dead services and stacks.
2. Delete with volumes (and configurations, networks, cleanup) only for items the user approved as "delete with data". If the user wants to keep data, stop the resource instead.
3. Wait about 40 seconds, then list resources again. Confirm each item is gone and no kept item disappeared.
4. Check the logs of kept apps that use databases, to catch connection errors.
5. Run Docker cleanup with SAFE settings (keep unused volumes, networks and retained images) to remove orphan images and build cache. If a manual run does not show in the history, mention that the nightly cleanup also runs.
6. Delete backup schedules that belong only to deleted databases if the panel did not remove them. Off-site copies can remain in S3/R2.

## Phase 6: DNS clean-up and domain moves

1. Delete only the records the user approved. Delete explicit A/AAAA/CNAME records for removed hosts. If a host had no explicit record (it used a wildcard), there is nothing to delete. Tell the user.
2. Confirm third-party records (Clerk `clerk`/`accounts`/`clkmail`/`clk._domainkey`, Resend or SES mail records, site-verification TXT) one group at a time. Other apps may use them.
3. Do not delete a record just because no panel resource matches it. The service can run outside the panel. Check with curl first, and ask.
4. Vercel DNS through the logged-in dashboard tab:
   - List: `GET /api/v4/domains/<apex>/records?teamId=<team>&limit=100`
   - Delete: `DELETE /api/v2/domains/<apex>/records/<rec_id>?teamId=<team>`
   - Move a host to a Vercel project: `POST /api/v10/projects/<prj_id>/domains?teamId=<team>` with body `{"name":"host.example.com"}`, and delete any explicit A record that points elsewhere. Check `verified:true` in the response.
5. Wait for the TTL (often 60 seconds). Verify at the authoritative nameserver (`dig +short host @ns1.<provider>`), then with curl and `openssl s_client -servername host` (subject, issuer, expiry).

## Phase 7: Monitoring and alerts

1. Delete monitors for removed apps. A "down" monitor for a deleted app hides real alerts.
2. Add monitors for every kept public endpoint that has none. Clone an existing healthy monitor (Uptime Kuma: `/clone/<id>`) so interval, retries and timeouts match. Change only name, URL and description. Save. Confirm the first heartbeat is Up.
3. Alerts must reach the user. If none exist, offer to set them up.
4. Default policy: alert only on problems. Silence means everything is green.
   - Uptime Kuma has no built-in "down only" option (GitHub issue #4744). Workaround for Telegram: turn on "Use custom message template", format Plain Text, template `{% if heartbeatJSON == nil or heartbeatJSON.status == 0 %}{{ msg }}{% endif %}`. UP messages render empty and Telegram rejects them, so they never arrive (Uptime Kuma logs an error for each one). DOWN, certificate-expiry and Test messages still arrive.
   - Turn on "Default enabled" and "Apply on all existing monitors".
   - Do not type the bot token or chat ID. Ask the user to paste them (they can often copy them from the panel's own Telegram notification settings), click Test, then Save. Then open one monitor's edit page and confirm the alert is ticked. Leave without saving.
5. Update or remove dashboard entries (for example Homepage) that point to removed services.

## Phase 8: Troubleshooting playbook

### Certificate shows "TRAEFIK DEFAULT CERT" and the site returns 503 or `000`
Meaning: the proxy has no healthy router for that host. The certificate is not the real problem.
1. Check the container status in the panel. An `unhealthy` container is dropped by Traefik.
2. Read the health check config (path, port, host, expected text).
3. Run a diagnostic inside the container: `sh -c 'which wget curl; wget -qO- http://127.0.0.1:<port><path>; echo rc=$?; head -2 /etc/os-release'`. If `wget`/`curl` are "not found", the HTTP health check can never pass (common with slim or distroless images).
4. Fix options, simplest first: disable the health check and rely on the uptime monitor; use a command health check with a tool the image has; or add curl or wget to the image.
5. Health check changes need a restart or redeploy. If the git repo is gone, the redeploy fails at `git ls-remote` ("could not read Username" or "Repository not found"), and the old container keeps running, still unhealthy.

### App cannot redeploy because its repo is missing
1. `gh repo list <owner>`. The repo may be renamed, replaced or deleted.
2. Find the deployed commit SHA in the deployment history.
3. Find local copies (`mdfind -onlyin ~ 'kMDItemFSName == "Dockerfile"'`, folder names). Check `git remote -v`, `git log`, `git status`, `git diff`.
4. Uncommitted changes can be dangerous (for example a "demo mode" that turns login off). Never deploy them without the user's explicit choice. Default to the deployed commit.
5. Ask the user which repo is canonical. A newer repo with the same product name can be a different app (different stack, data model or platform). Explain the difference before you act.
6. If another platform already runs the canonical version, the simplest fix is to point the domain there and retire the server copy (with approval).

### Repeated "backup succeeded locally but failed to upload to S3 (storage ID: null)" alerts
1. List all backup schedules for that database. Look for duplicates, an every-minute cron (`* * * * *`) created by mistake, and `save_s3` with `s3_storage_id` null.
2. Get the storage UUID from the panel's S3 storage page (link `/storages/<uuid>`).
3. Update the real schedule: `save_s3=true`, `s3_storage_uuid=<uuid>`, S3 retention (for example 14). Estimate bucket use (dump size × retention) against the free tier.
4. Delete the disabled or duplicate schedule (its local dump files go with it).
5. Trigger "Back up now" and confirm `s3_uploaded: true`.

### Backup looks too small
A dump of a few KB for a database that apps use means the schedule backs up only the default DB. Set "all databases" or list the real DB names, then run a backup and compare the size.

### Database will not start after an image update
You probably changed the major version on an old data volume. Set the old tag back at once, start it, and plan a dump-and-restore upgrade (Phase 4.3).

### Domain resolves to another platform instead of the VPS
If no explicit record exists, the host uses a wildcard (for example `*` ALIAS to Vercel). The VPS proxy config for that host does nothing. Decide with the user which platform owns the host.

### Monitor for an auth-protected app
A 307/302 to a login page is normal. Uptime Kuma follows redirects (maxRedirects 10) and the login page returns 200. Do not add credentials to the monitor.

## Phase 9: Report and remember

- Report in short steps: what changed, what you verified, updates applied (old → new version), updates found but not applied and why, what is still open, what needs a decision. Name items by domain or app name, not internal ids.
- List pre-existing problems you found but did not fix, with one-line causes.
- Save durable facts to memory: which apps the user keeps, which were retired, DNS providers, alert channel, and the canonical repo or platform for apps that exist twice.

## Final checklist

- [ ] Inventory and version table done; nothing changed before the user answered.
- [ ] Fresh database and instance backups verified (local and off-site).
- [ ] Updates found for panel, agents, proxy, databases, services, Docker and OS; release notes read.
- [ ] Approved updates applied one at a time in the right order; each one verified; the others reported.
- [ ] Approved resources deleted with the correct volume choice; resource list re-checked.
- [ ] Safe Docker cleanup run.
- [ ] Approved DNS records deleted; stale and third-party records confirmed; results checked with dig, curl and openssl.
- [ ] Monitors match the kept endpoints; down-only alerts work (the user tested them).
- [ ] Backup alert sources fixed and a test backup verified.
- [ ] Tabs you opened closed; the user's tabs restored.
- [ ] Short report sent; durable facts saved to memory.