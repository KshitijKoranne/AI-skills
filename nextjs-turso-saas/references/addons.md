# Optional Add-ons Setup Guide

Reference this file when the user asks about auth, email, payments, or other SaaS add-ons.

---

## Clerk (Auth — Recommended for SaaS)

Easiest auth for Next.js. Handles sign-up, sign-in, sessions, and user management UI out of the box.

```bash
npm install @clerk/nextjs
```

`src/middleware.ts`
```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher(["/dashboard(.*)"]);

export default clerkMiddleware((auth, req) => {
  if (isProtectedRoute(req)) auth().protect();
});

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

Add to `.env.local`:
```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

Wrap root layout with `<ClerkProvider>`.

---

## NextAuth v5 (Auth — Self-hosted)

Better for projects where you want full control, no third-party dependency.

```bash
npm install next-auth@beta
```

Create `src/auth.ts` with your providers. See https://authjs.dev/getting-started for full setup.

---

## Resend (Email)

Best transactional email for indie SaaS. Simple API, React email templates.

```bash
npm install resend react-email @react-email/components
```

`src/lib/email.ts`
```typescript
import { Resend } from "resend";

export const resend = new Resend(process.env.RESEND_API_KEY);
```

Usage in a Server Action:
```typescript
await resend.emails.send({
  from: "noreply@yourdomain.com",
  to: user.email,
  subject: "Welcome!",
  react: WelcomeEmail({ name: user.name }),
});
```

---

## Stripe (Payments)

```bash
npm install stripe @stripe/stripe-js
```

Add to `.env.local`:
```env
STRIPE_SECRET_KEY=sk_test_...
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

Create a webhook handler at `src/app/api/webhooks/stripe/route.ts` to handle `checkout.session.completed` and update your DB.

---

## UploadThing (File Uploads)

The simplest file upload solution for Next.js — no S3 setup required.

```bash
npm install uploadthing @uploadthing/react
```

See https://uploadthing.com/docs/getting-started for the route handler + component setup.

---

## Trigger.dev (Background Jobs)

For running long tasks (sending emails in bulk, processing data) outside the request cycle.

```bash
npm install @trigger.dev/sdk @trigger.dev/nextjs
```

---

## Posthog (Analytics)

```bash
npm install posthog-js
```

Wrap your root layout with a `PostHogProvider` client component. Self-host or use their cloud.
