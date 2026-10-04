# AI Skills — by KJR Labs

A collection of reusable AI-agent skills for developers, builders, and pharma professionals.

## Skills

### `nextjs-turso-saas`
Step-by-step scaffold guide for spinning up a production-ready SaaS web app using Next.js 14+ (App Router), Turso, Drizzle ORM, Tailwind CSS, shadcn/ui, and TypeScript strict mode.

**Stack:** Next.js · Turso · Drizzle ORM · Tailwind CSS · shadcn/ui · TypeScript · Vercel

---

### `gamp5-risk-assessment`
Generates a professional, GMP-compliant FMEA-based Quality Risk Assessment document as a formatted Word (.docx) file. Fully aligned with ISPE GAMP 5 Second Edition (2022), ICH Q9, and EU Annex 11.

Covers all GAMP software categories (Cat 1, 3, 4, 5) and system types including LIMS, ERP, SCADA, MES, lab instruments, and custom in-house software. Includes a pre-built function library with typical failure modes and a complete regulatory reference set.

**Scope:** GMP · GLP · GCP · 21 CFR Part 11 · EU Annex 11 · ICH Q9

---

### `clean-mac`
Audits macOS storage and creates a confirmation-first cleanup plan. Finds rebuildable caches, app leftovers, AI/editor artifacts, Xcode/developer junk, screenshot locations, and personal-review folders before deleting anything.

**Scope:** macOS cleanup · app leftovers · developer caches · AI tool artifacts · screenshots

---

### `f5-opus`
Makes Opus models (4.8+) operate as an extension of Claude Fable 5 — same judgment, design taste, audit rigor, recommendation style, and memory discipline. Routes trivially simple questions down to Sonnet to save cost.

**Scope:** persona/decision-policy transfer · design anti-slop rules · code/doc auditing · Opus↔Sonnet routing

---

### `design-references`
Before building a site, landing page or UI, picks real design references (galleries, component libraries, animation and 3D sources) from a curated list by need. Reuse rules: open-source code can be used as-is with colors tweaked to the project; galleries are inspiration only.

**Scope:** web design · UI components · animation · licence-aware reuse

---

### `mac-app-store-release`
Ships a Tauri (or other non-Xcode) macOS app to the Mac App Store, and as a signed, notarized DMG for website download. Fill in your own Team ID, notarization key and contact details before use.

**Scope:** Mac App Store · signing · notarization · App Store Connect metadata

---

### `higgsfield-api`
Generates images and video with the Higgsfield API (Seedance, Soul and other models), or adds Higgsfield generation to a Python or TypeScript project. Includes a reusable CLI script.

**Scope:** Higgsfield · image and video generation · Python · TypeScript

---

### `motion-film`
Makes short motion-graphics videos (app ads, promos, launch teasers, explainer clips) as MP4 with synced sound, rendered from code.

**Scope:** motion graphics · video rendering · sound sync

---

### `store-screenshots`
Makes App Store, Mac App Store and Play Store marketing screenshots (framed, captioned, exact store sizes), plus optional app preview videos.

**Scope:** App Store · Play Store · marketing screenshots · preview videos

---

### `vps-maintenance`
Safe maintenance for a self-hosted VPS: update the panel, proxy, databases, services and OS; back up; remove unused apps and DNS; fix SSL and proxy errors, backup alerts and monitors.

**Scope:** VPS · Coolify-style panels · backups · SSL · monitoring

---

## Installation

### Claude.ai (Web/Desktop)
Download the `.skill` file from the [Releases](../../releases) page and upload it via Claude settings.

### Claude Code (CLI)
```bash
git clone https://github.com/KshitijKoranne/AI-skills
cp -r AI-skills/<skill-name> ~/.claude/skills/
```

---

Built by [KJR Labs](https://kjrlabs.in)
