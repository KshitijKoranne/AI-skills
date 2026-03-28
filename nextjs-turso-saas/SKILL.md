---
name: nextjs-turso-saas
description: >
  Step-by-step scaffold guide for bootstrapping a production-ready SaaS or internal web app
  using Next.js 14+ (App Router), Turso (SQLite edge DB), Drizzle ORM, Tailwind CSS,
  shadcn/ui, and TypeScript strict mode. Use this skill whenever the user wants to start a
  new Next.js project, bootstrap a SaaS, set up Turso or Drizzle, scaffold a web app from
  scratch, or asks about project structure for a Next.js + Turso + Tailwind stack. Trigger
  even if the user just says "new project", "start an app", "fresh Next.js setup", or
  "help me scaffold" — don't wait for them to spell out every tool name.
---

# Next.js + Turso SaaS Scaffold Guide

A opinionated, step-by-step guide for spinning up a production-ready SaaS web app.

## Stack

| Layer | Tool | Why |
|---|---|---|
| Framework | Next.js 14+ (App Router) | File-based routing, RSC, server actions |
| Database | Turso (libSQL edge SQLite) | Serverless, edge-compatible, generous free tier |
| ORM | Drizzle ORM | Type-safe, lightweight, great with Turso |
| Styling | Tailwind CSS | Utility-first, fast to prototype |
| Components | shadcn/ui | Accessible, unstyled-ish, copy-paste components |
| Language | TypeScript (strict) | Catch errors early, better DX |
| Deployment | Vercel | Zero-config for Next.js |

---

## Phase 1 — Project Init

### 1.1 Create the Next.js app

```bash
npx create-next-app@latest my-app \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
cd my-app
```

**Flags explained:**
- `--app` → App Router (not Pages Router)
- `--src-dir` → puts all code under `src/` for clean separation
- `--import-alias "@/*"` → clean imports like `@/lib/db` instead of `../../lib/db`

### 1.2 Verify `tsconfig.json` is strict

Check that `tsconfig.json` includes:
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```
Add `"noUncheckedIndexedAccess": true` manually if it's missing — `create-next-app` doesn't add it by default but it catches a whole class of array/object bugs.

---

## Phase 2 — Database Setup (Turso + Drizzle)

### 2.1 Install Turso CLI and create a database

```bash
# Install Turso CLI — macOS (recommended)
brew install tursodatabase/tap/turso

# Install Turso CLI — Linux (or macOS without Homebrew)
curl -sSfL https://get.tur.so/install.sh | bash

# Login
turso auth login

# Create a database
turso db create my-app-db

# Get the connection URL
turso db show my-app-db --url

# Create an auth token
turso db tokens create my-app-db
```

Save these as environment variables (see Phase 3).

### 2.2 Install Drizzle + Turso driver

```bash
npm install drizzle-orm @libsql/client
npm install -D drizzle-kit
```

### 2.3 Create the DB client

`src/lib/db.ts`
```typescript
import { drizzle } from "drizzle-orm/libsql";

export const db = drizzle({
  connection: {
    url: process.env.TURSO_DATABASE_URL!,
    authToken: process.env.TURSO_AUTH_TOKEN!,
  },
});
```

> **Note:** This is the modern Drizzle API (v0.30+). The older pattern using `createClient` from `@libsql/client` separately also still works but this is cleaner and the current recommended style.

### 2.4 Create your first schema

`src/lib/schema.ts`
```typescript
import { text, integer, sqliteTable } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name"),
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
});
```

### 2.5 Configure Drizzle Kit

`drizzle.config.ts` (at root)
```typescript
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  schema: "./src/lib/schema.ts",
  out: "./drizzle",
  dialect: "turso",
  dbCredentials: {
    url: process.env.TURSO_DATABASE_URL!,
    authToken: process.env.TURSO_AUTH_TOKEN!,
  },
});
```

### 2.6 Push schema to Turso

```bash
npx drizzle-kit push
```

Use `push` for development (direct sync). Use `generate` + `migrate` for production migrations.

---

## Phase 3 — Environment Variables

`.env.local`
```env
TURSO_DATABASE_URL=libsql://your-db-name-your-org.turso.io
TURSO_AUTH_TOKEN=your-token-here
```

`.env.example` (commit this, not `.env.local`)
```env
TURSO_DATABASE_URL=
TURSO_AUTH_TOKEN=
```

Make sure `.env.local` is in `.gitignore` — `create-next-app` handles this automatically.

---

## Phase 4 — shadcn/ui Setup

```bash
npx shadcn@latest init
```

> ⚠️ **Next.js 15 + React 19 peer dep issue:** `create-next-app` now defaults to React 19, which causes a peer dependency conflict during `shadcn init`. If you see an `ERESOLVE` error, run with the legacy flag instead:
> ```bash
> npx shadcn@latest init --legacy-peer-deps
> ```
> Also use the same flag when adding individual components if they error: `npx shadcn@latest add button --legacy-peer-deps`

CLI will ask:
- Base color → `Neutral` or `Slate` (both work well for SaaS; Neutral is the new default)
- CSS variables → `Yes`

Then add components as needed:
```bash
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add card
npx shadcn@latest add table
npx shadcn@latest add dialog
```

Components land in `src/components/ui/` — they're yours to edit.

---

## Phase 5 — Folder Structure

After all setup, your `src/` should look like this:

```
src/
├── app/
│   ├── layout.tsx          # Root layout (fonts, providers)
│   ├── page.tsx            # Landing / home
│   ├── globals.css         # Tailwind base styles
│   └── (dashboard)/        # Route group for auth-protected pages
│       ├── layout.tsx
│       └── dashboard/
│           └── page.tsx
├── components/
│   ├── ui/                 # shadcn components (auto-generated)
│   └── [your components]
├── lib/
│   ├── db.ts               # Drizzle client
│   ├── schema.ts           # Drizzle schema
│   └── utils.ts            # shadcn utils (cn helper, etc.)
└── types/
    └── index.ts            # Shared TypeScript types
```

**Key conventions:**
- Route groups `(name)/` — group pages without affecting URL paths
- `lib/` — all non-UI logic (db, helpers, API clients)
- `components/ui/` — shadcn only; your components go in `components/` root

---

## Phase 6 — Server Actions Pattern

Prefer **Server Actions** over API routes for form mutations and DB writes in SaaS apps.

`src/app/(dashboard)/dashboard/actions.ts`
```typescript
"use server";

import { db } from "@/lib/db";
import { users } from "@/lib/schema";
import { revalidatePath } from "next/cache";

export async function createUser(formData: FormData) {
  const email = formData.get("email") as string;

  await db.insert(users).values({
    id: crypto.randomUUID(),
    email,
  });

  revalidatePath("/dashboard");
}
```

Use `revalidatePath` to refresh data after mutations — no manual state management needed.

---

## Phase 7 — Vercel Deployment

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

Add environment variables in Vercel dashboard:
- `TURSO_DATABASE_URL`
- `TURSO_AUTH_TOKEN`

Or via CLI:
```bash
vercel env add TURSO_DATABASE_URL
vercel env add TURSO_AUTH_TOKEN
```

**Important:** Turso works perfectly on Vercel's serverless/edge runtime — no connection pool issues unlike traditional Postgres.

---

## Optional Add-ons

Suggest these to the user depending on their needs. Read `references/addons.md` for setup details on each.

| Need | Tool | Command |
|---|---|---|
| Auth | Clerk | `npm install @clerk/nextjs` |
| Auth (self-hosted) | NextAuth v5 | `npm install next-auth@beta` |
| Email | Resend | `npm install resend` |
| Payments | Stripe | `npm install stripe` |
| File uploads | UploadThing | `npm install uploadthing` |
| Background jobs | Trigger.dev | `npm install @trigger.dev/sdk` |
| Analytics | Posthog | `npm install posthog-js` |

---

## Common Mistakes to Avoid

- **Don't use `turso db push` in production** — use `drizzle-kit generate` + `migrate` for tracked migrations
- **Don't import `db` in Client Components** — Drizzle only runs server-side; use Server Actions or Route Handlers
- **Don't skip `.env.example`** — future you (and collaborators) will thank you
- **Don't add shadcn components to `git` selectively** — commit the whole `src/components/ui/` folder
- **Don't use the Pages Router** — App Router is the standard now; mixing them causes confusion

---

## Quick Reference Checklist

- [ ] `create-next-app` with `--app --src-dir --typescript --tailwind`
- [ ] `noUncheckedIndexedAccess` added to `tsconfig.json`
- [ ] Turso DB created, URL + token saved to `.env.local`
- [ ] Drizzle installed, `src/lib/db.ts` and `src/lib/schema.ts` created
- [ ] `drizzle.config.ts` at root
- [ ] `npx drizzle-kit push` run successfully
- [ ] `shadcn init` done, base components added
- [ ] `.env.example` committed (without values)
- [ ] Deployed to Vercel with env vars set
