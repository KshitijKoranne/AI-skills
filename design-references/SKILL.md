---
name: "design-references"
description: "Use when building or redesigning a website, landing page, web app, UI screen or component that must look polished. Picks real design references before coding."
---

# Design references

AI output looks generic when it has not seen good design. Look at real examples first, then build.

## Steps

1. Name the need (page type, section, component, effect).
2. Pick 1-2 sources from the table below.
3. Fetch them (WebFetch or browser). Note concrete patterns: layout, type scale, spacing, color, motion.
4. Check the licence (see Reuse rules). Then either reuse the code or only copy the pattern.
5. Build. Match the project: its colors, fonts and stack.
6. If a source cannot be reached, use the next one. Do not stop.

## Sources by need

| Need | Sources |
|---|---|
| Full-page prompts | scrolltide.co, vibeprompts.dev |
| Design system as text | designmd.ai, styles.refero.design |
| Site inspiration | minimal.gallery, godly.website, awwwards.com, land-book.com, landing.love, hoverstat.es, kage.design |
| Mobile app patterns | mobbin.com |
| Navbar, footer, CTA, hero, pricing | navbar.gallery, footer.design, cta.gallery, supahero.io, pricingpages.design |
| Component patterns | component.gallery |
| React components | ui.shadcn.com, 21st.dev, shadcnblocks.com |
| Animated components | ui.aceternity.com, magicui.design, motion-primitives.com, smoothui.dev, kinetics.colorion.co |
| Micro-interactions, small UI | microkit.co, uiverse.io, glass.samasante.com |
| Animation engine | animejs.com |
| 3D and shaders | threejs.org, shadertoy.com, thebookofshaders.com, threejs-journey.com |
| Illustrations, icons | kitbitz.art, 3dicons.co |

## Reuse rules

- Open-source or free-to-use code (for example MIT or Apache): use it as-is when it fits. No need to rewrite it.
- Change colors only when the project needs it. Use the project's theme tokens or CSS variables. Do not edit the component logic.
- Look at the licence on the component page or its repo before you copy. If you cannot find one, treat it as inspiration only.
- Paid or restricted components: do not copy. Copy the pattern only.
- Galleries and showcase sites (awwwards, godly, land-book and the like) show other people's work. Use them for inspiration only. Never copy their code or assets.
- Keep the licence notice if the licence asks for it.

## Other rules

- Use native CSS and the existing stack first. Add a library only if the user wants that effect.
- Pick references that fit the product. Do not use a 3D or heavy-motion source for a plain tool.
- Do not name these sources in public copy.