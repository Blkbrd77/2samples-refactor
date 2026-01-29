# 2Samples Migration Context

## Project Overview

Family travel portfolio website migrating from **Flask/Python on AWS Elastic Beanstalk** to **Astro on Cloudflare Pages** to reduce hosting costs.

- **Flask app (current production):** `app/`
- **Astro app (migration target):** `2samples-astro/`
- **Media assets:** AWS S3 bucket `2samples-static-assets-211125453069`, served via CloudFront CDN `https://d1rhrn7ca7di1b.cloudfront.net` (staying on AWS regardless of hosting platform)

## Architecture Decisions

- **Astro with SSR** (`output: 'server'`) using `@astrojs/cloudflare` adapter
- **Cloudflare Pages** as the hosting target
- **Media stays on AWS** — videos and images remain in S3/CloudFront
- **Security headers** configured via `public/_headers` (Cloudflare-native approach)
- **TypeScript strict mode** throughout
- **Testing:** Vitest (unit, 95% coverage threshold) + Playwright (E2E)

## Tech Stack (Astro)

| Layer | Technology |
|-------|-----------|
| Framework | Astro 5.x |
| Adapter | @astrojs/cloudflare 12.x |
| Language | TypeScript 5.x (strict) |
| Unit Tests | Vitest + happy-dom + @testing-library |
| E2E Tests | Playwright (Desktop Chrome + Mobile Chrome) |
| Linting | ESLint + @typescript-eslint + eslint-plugin-astro |
| Formatting | Prettier + prettier-plugin-astro |
| AWS SDK | @aws-sdk/client-s3 (for S3 video fetching) |

## Key Files & Structure

```
2samples-astro/
  src/
    pages/           # 9 pages (index, japan, ireland, uk, greece, bahamas, blog, maps, library)
    components/      # Tile.astro, VideoSection.astro, BookCard.astro
    layouts/         # Base.astro (sticky nav, global styles, favicon)
    lib/
      destinations.ts  # Centralized destination content (titles, sections, descriptions)
      navigation.ts    # Nav link definitions
      storage.ts       # S3 client + video data processing utilities
      library.ts       # Book types + library data loader
      types.ts         # Video/S3 TypeScript interfaces
    tests/           # Vitest unit tests
    styles/          # (empty — styles are in public/styles/)
  e2e/               # Playwright E2E tests
  public/
    styles/global.css  # All CSS
    library_data.json  # Book data from Inventaire API (~300+ books)
    _headers           # Cloudflare security headers (CSP, X-Frame-Options, etc.)
```

## Migration Status

### Fully Migrated

| Page/Feature | Notes |
|-------------|-------|
| Homepage (`index.astro`) | All 6 tiles match Flask version |
| Japan page | 3 video sections, content matches Flask |
| Ireland page | 4 video sections (Days 1-4), content matches Flask |
| Blog page | Placeholder — matches Flask (both minimal) |
| Maps page | 3D globe with globe.gl, family filters, timeline — fully ported |
| Library page | Search, filters, BookCard grid, Inventaire data — fully ported |
| Base layout | Sticky nav, all 9 links, favicon, global CSS |
| CSS/Styling | Ported to public/styles/global.css, matches Flask style.css |
| Navigation | Centralized in navigation.ts |
| Security headers | CSP, X-Frame-Options, etc. in public/_headers |
| Testing infrastructure | Vitest + Playwright configured and passing |

### Partially Migrated (Content Gaps)

| Page | Flask Has | Astro Has | Missing |
|------|----------|----------|---------|
| **UK** | 7 day sections (Days 5-11), 7 videos | 1 section (Day 5 only), 1 video | Days 6-11 content and video entries in `destinations.ts` |
| **Greece** | 6 day sections (Days 1-8), 6 videos | 1 section (generic), 1 video | Day-by-day breakdown and video entries in `destinations.ts` |
| **Bahamas** | 1 section | 1 section | Content matches, but description is brief |

### Not Yet Implemented

| Feature | Details |
|---------|---------|
| **CI/CD for Astro** | `.github/workflows/ci.yml` only covers the Flask app. Need a workflow for the Astro build/test/deploy. |
| **Custom domain / DNS** | No CNAME or DNS configuration for Cloudflare. Current production is on AWS EB. |
| **Decommission AWS EB** | Once Cloudflare is stable and DNS is switched, shut down Elastic Beanstalk to save costs. |

## Video Data Strategy (Decided)

Using **hardcoded CloudFront URLs** — no AWS credentials needed on Cloudflare. Each destination page has a `placeholderVideos` array with direct CloudFront URLs. When adding new videos, update the array in the page file. Most video files use `.mov` extension (verified against S3). The `storage.ts` S3 utilities remain in the codebase but are unused.

```typescript
const placeholderVideos = [
  {
    url: 'https://d1rhrn7ca7di1b.cloudfront.net/videos/VideoName.mov',
    name: 'VideoName',
    still: 'https://d1rhrn7ca7di1b.cloudfront.net/stills/VideoName-still-001.jpg'
  },
];
```

## Cloudflare Pages Deployment (Live)

- **URL:** `https://2samples-refactor-astro-cf.pages.dev/`
- **Project:** Connected to `Blkbrd77/2samples-refactor` repo via Git integration
- **Root directory:** `2samples-astro`
- **Build command:** `npm run build`
- **Deploy command:** `npx wrangler pages deploy dist`
- **Auto-deploys:** On push to `main`
- **Config file:** `wrangler.jsonc` in `2samples-astro/`

### Cloudflare Gotchas Encountered
- Root `.gitignore` had `lib/` (Python pattern) which blocked `src/lib/` — fixed to `/lib/`
- `node:fs` doesn't exist on Cloudflare Workers — library page now uses direct JSON import instead
- Video files in S3 are mostly `.mov`, not `.mp4` — placeholder URLs must match actual extensions

## S3 Bucket Structure

```
s3://2samples-static-assets-211125453069/
  videos/          # .mp4 and .mov video files
  stills/          # Video poster thumbnails (e.g., VideoName-still-001.jpg)
  images/          # Static images (comingSoon.jpg, favicon, etc.)
```

## Key Design Patterns

- **Centralized content:** All destination section data lives in `src/lib/destinations.ts` — add new sections there, pages render them automatically via `.map()`
- **Component reuse:** `VideoSection.astro` renders any video section given a title, videoName, video array, and description
- **Client-side interactivity:** Maps globe and Library search/filter use inline `<script>` tags with vanilla JS (no client framework)
- **Build-time data:** Library loads `library_data.json` via direct JSON import (bundled by Vite, works on Cloudflare Workers)

## Suggested Next Steps (Priority Order)

1. **Add CI/CD workflow** for Astro (test + build on PRs)
2. **Configure custom domain** — DNS CNAME switch from AWS EB to Cloudflare Pages
3. **Decommission AWS EB** once Cloudflare is stable with custom domain

## Useful Commands

```bash
cd 2samples-astro
npm run dev          # Local dev server at localhost:4321
npm run build        # Production build
npm run preview      # Preview production build
npm test             # Run Vitest unit tests
npm run test:e2e     # Run Playwright E2E tests
npm run lint         # ESLint check
npm run typecheck    # TypeScript check
```

## External Services

| Service | Purpose | Reference |
|---------|---------|-----------|
| AWS S3 | Video/image storage | Bucket: `2samples-static-assets-211125453069` |
| AWS CloudFront | CDN for media | `https://d1rhrn7ca7di1b.cloudfront.net` |
| Inventaire.io | Book library data | User: `f9a685e15825d73108b49c3465224b03` |
| Globe.gl | 3D globe visualization | Loaded from `https://unpkg.com/globe.gl` |
| Cloudflare Pages | Astro hosting (live) | `https://2samples-refactor-astro-cf.pages.dev/` |
