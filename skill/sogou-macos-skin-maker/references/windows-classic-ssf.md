# Classic Windows SSF workflow

Use this reference only for classic Windows Sogou `.ssf` packages. Inspect the chosen working base before assuming that every `.ssf` shares the same structure.

## Contents

- [1. Discover and register the base](#1-discover-and-register-the-base)
- [2. Separate reference roles](#2-separate-reference-roles)
- [3. Inspect the package](#3-inspect-the-package)
- [4. Model runtime geometry correctly](#4-model-runtime-geometry-correctly)
- [5. Preserve exact subjects](#5-preserve-exact-subjects)
- [6. Treat clarity honestly](#6-treat-clarity-honestly)
- [7. Build APNG deterministically](#7-build-apng-deterministically)
- [8. Package and validate](#8-package-and-validate)
- [9. Runtime Gate D](#9-runtime-gate-d)

## 1. Discover and register the base

Do not ask a user for a generic classic `.ssf` merely to study the format. Use this reference and the skill's proven inspection/build workflow. Before requesting an exact user-specific package:

1. Search the current workspace, all paths already mentioned in the conversation, Downloads, project `base`/`dist`/`build` folders, installed Sogou `allskin`/`skin` folders, and work notes.
2. Hash every plausible `.ssf`; record aliases for identical content.
3. Inspect extracted trees and deterministic build scripts. A deleted original package may be reproducible without another upload.
4. Record a base registry entry:

   ```text
   platform: Windows classic SSF
   paths/aliases:
   sha256:
   member count/order:
   compression:
   skin.ini encoding/BOM:
   image/APNG inventory:
   prior project/use:
   working runtime evidence:
   ```

5. Ask only if the task requires modifying a specific unavailable skin, no compatible local or reconstructable equivalent exists, and that exact user-specific content blocks the task. Explain the search and the missing capability. Never request a duplicate copy merely because its filename changed.

Keep discovery within the current user's accessible files. Do not transfer or reuse private packages between users. Do not solicit modern/H5 packages from unrelated users; accept only an authorized package voluntarily supplied in the current task or use official tooling/schema.

## 2. Separate reference roles

Classify every supplied item independently:

- `format/base reference`: inspect structure and runtime mechanics only;
- `visual reference`: use only the approved layout, palette, subject, or ornament role;
- `exact asset`: preserve its internal pixels and identity;
- `motion reference`: inherit movement, not a regenerated face or body.

If the user says a skin is format-only, do not inherit its artwork, composition, palette, or subject styling.

## 3. Inspect the package

Check at minimum:

- ZIP validity, compression type, member order/count, and flat/nested structure;
- `skin.ini` encoding, BOM, sections, unknown keys, visible name, and version;
- every referenced PNG/BMP and missing reference;
- raster dimensions, alpha extrema/bboxes, and transparent margins;
- APNG `acTL`/`fcTL`/`fdAT`, frame canvases, duration, disposal, blend, and loop;
- candidate background, pinyin/candidate margins, custom layers, page controls, separators, status base, language states, and menu states.

Preserve the working base's encoding, structure, unknown fields, and compression unless a verified format rule requires a change.

## 4. Model runtime geometry correctly

Treat these as separate systems:

1. **Background raster** — visible capsule/border, transparent canvas, baked separators, and stretch-safe regions.
2. **Text layout** — pinyin and candidate margins/padding controlled by `skin.ini`.
3. **Custom-layer occupancy** — transparent character canvases may still change window height or horizontal space.
4. **Control occupancy** — page assets and status controls may reserve space even when transparent.
5. **Runtime decoration** — Sogou may draw a separator or selected state in addition to the bitmap.

Do not bake candidate characters into a stretchable background. Keep left subject, right subject, candidate background, status base, language controls, and menu controls in independent assets when the base supports them.

When adjusting text:

- distinguish `increase by d` from `set to d`;
- record old and new values;
- change only one margin family at a time;
- measure visible glyph bounds, not font-box assumptions;
- test pinyin and candidates separately;
- ensure selected highlighting hugs the requested glyphs/number, or remove it completely when the user requests text-only emphasis.

If two horizontal lines appear, inspect both the bitmap and runtime separator configuration. Remove only the duplicate source.

## 5. Preserve exact subjects

Use one approved high-resolution master for each subject. Do not independently regenerate animation frames.

- Keep identity-critical face, nose, mouth, hat, hair, outfit, markings, palette, and silhouette locked.
- For a run/bob, move only approved body/foot pixels and audit the head/face under the declared translation.
- For a blink, remove the complete original open-eye cavity, iris, upper lash, and terminal lash pixels before overlaying the closed eye.
- At small sizes, inspect for isolated residue pixels and disappearing lash terminals. Use a documented scale/survival compensation only after comparing actual-size and magnified previews.
- If a transformation is shared by candidate and status assets, audit every consumer together.

## 6. Treat clarity honestly

Classic single-density SSF cannot create information that is absent at the final display size.

- Do not call unsharp masking, increased contrast, or thicker outlines “higher resolution.”
- Do not repeatedly tune sharpening after the user rejects the visual premise.
- Test client scaling flags as isolated diagnostics, not as promised fixes.
- If the client resamples a 50–100 px subject, propose a larger rendered subject or a proven high-density/modern pipeline.
- Require an authentic runnable H5/modern base or published schema before migrating. Do not fabricate H5 from a classic `.ssf`.

## 7. Build APNG deterministically

- Assemble APNG directly from approved production frames.
- Keep full canvases, anchors, frame order, durations, loop, disposal, and blend stable.
- Keep independent motions in independent assets when the runtime supports them.
- Compare packaged frame RGBA bytes to approved frame files.
- Produce an actual-speed composite and a magnified contact sheet for every animated consumer.
- Maintain a component approval matrix for candidate subject, companion, status subject, stars/ornaments, language controls, and menu controls.

## 8. Package and validate

Start from the clean working base. Allowlist changed members; reject any other difference.

Validate:

- ZIP CRC and proven structure/compression;
- `skin.ini` encoding/BOM and only intended metadata/layout changes;
- every referenced asset;
- APNG canvas, frame count, RGBA bytes, duration, loop, and alpha bbox;
- locked resources byte-identical to the base;
- unique visible name and version to defeat cache;
- package-size constraints from the selected distribution channel;
- two consecutive deterministic builds with the same SHA-256;
- no dependency on clipboard, temporary, or deleted paths.

Withdraw a packaged build immediately if a visible component is discovered to contain an unapproved or stale frame. Reopen Gate C for every affected consumer.

## 9. Runtime Gate D

On Windows, test:

1. one short candidate;
2. five normal candidates;
3. long stretched candidates;
4. first and non-first selection;
5. paging and controls;
6. pinyin/candidate vertical spacing and left/right padding;
7. every candidate animation loop at least twice;
8. every status animation loop at least twice;
9. Chinese and English labels;
10. language/menu normal, hover, pressed, and click behavior;
11. transparent art on light and dark backgrounds.

Treat screenshots/video from the installed Windows client as ground truth. Leave Gate D pending when real runtime evidence is unavailable.
