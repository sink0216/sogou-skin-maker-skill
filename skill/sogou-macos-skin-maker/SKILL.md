---
name: sogou-macos-skin-maker
description: Design, study references for, preview, approve, build, modify, repair, validate, package, and runtime-test Sogou Pinyin skins for macOS (.mssf) and classic Windows (.ssf). Supports exact character/IP artwork, static or APNG animation, candidate geometry, status controls, notifications, transparent layers, file/base deduplication, deterministic packaging, and runtime calibration. Use whenever creating or revising a Sogou skin, especially when supplied artwork, an existing skin file, animation, stretch-safe layout, padding, controls, clarity, or runtime placement must be preserved and verified.
---

# Sogou Skin Maker (macOS + Windows)

Build against the selected Sogou runtime, not a static mockup. Route macOS and Windows formats separately, separate design approval from production, and treat the installed client as the final renderer.

## Non-negotiable rules

- Before asking for a skin file, exhaust local discovery and deduplication. Search the current workspace, paths already mentioned in the conversation, Downloads, project base folders, installed Sogou skin folders, prior build notes, and known hashes. Never ask a user to upload or resend a Sogou skin already present or previously supplied in the accessible local environment.
- Never ask users for a generic classic Windows `.ssf` merely to learn its format; use the bundled Windows reference and proven local tooling. Request a file only when the task is to modify a specific unavailable skin or an exact proprietary base is technically indispensable.
- Do not solicit H5/modern skin packages from unrelated users as format research. Use official tooling/schema or a package the current user voluntarily supplies and is authorized to use; otherwise report the unsupported format instead of repeatedly requesting samples.
- Reuse files only within the current user's accessible environment and authorization scope. Never claim access to, request, or reuse another user's private files.
- Maintain a base registry in work notes containing path, platform, SHA-256, structure, and prior use. Content identity is determined by hash and inspection, not filename.
- Start from a known-working local `.mssf`, `.ssf`, or installed skin whenever possible. Ask for a new base only after local discovery proves that no compatible working base or equivalent content exists and the missing format genuinely blocks progress.
- Detect the platform before editing. Do not apply macOS plist/Retina/package rules to Windows `skin.ini`/flat-SSF packages, or vice versa.
- Preserve unrelated user skins. Work in a copy and use a unique visible version for every install.
- Do not package or install a new design before the required approval gates pass.
- Do not infer approval from silence, general enthusiasm, or approval of a different stage.
- Use user references according to an explicit `must preserve / may adapt / must not introduce` contract.
- If a user says an existing skin is format-only, inherit its container mechanics only. Do not let its artwork, layout, palette, or prior design leak into the new design.
- Keep every approved subject, logo, object, or character consistent across all states and frames.
- Treat an explicitly chosen asset as locked artwork. Background removal, alpha cleanup, cropping, or scaling does not authorize redrawing or replacing it with a similar asset.
- If the user asks for subject animation, animate the named subject or parts. Do not substitute hearts, dots, punctuation, sparkles, or other symbols unless explicitly approved.
- Keep static decoration out of subject APNG frames.
- Produce native 1x and 2x PNGs. Make 2x dimensions exactly double 1x.
- Inspect every animation frame at native 2x size, including fills, seams, transparent edges, and anchors.
- Inspect animation at actual runtime size and speed as well as magnified frame crops. A magnified contact sheet cannot prove runtime legibility, and a real-speed preview can hide one-frame residue.
- Use solid colors by default. Add gradients only when explicitly approved.
- If the user requests the official Chinese/English notification, copy the official assets and complete local `HummingNotif` configuration; do not approximate it.
- Never trust a preview alone. After approval and packaging, install, invoke real candidates, and compare a runtime screenshot.
- Never package a mixture of newly approved motion and stale motion from another component. Track candidate subject, companion, status subject, ornaments, and controls in a component-level approval matrix.
- Treat bitmap geometry, Sogou runtime layout, and invisible control occupancy as three separate systems. A taller trunk PNG does not by itself create a taller candidate window.
- Before every revision, write a change contract with `must change`, `must remain pixel-identical`, and whether requested pixels mean 1x screen points or native-2x pixels.
- Change one geometry family at a time. Verify invariants with hashes and pixel bounds before installing.

## Approval state

Track these gates in the work notes:

```text
A reference contract: pending | approved
B static design:      pending | approved
C animation:          pending | approved | not-applicable
D runtime:            pending | approved
```

Only the user can approve A, B, or C. Revisions invalidate the affected gate and every downstream gate. For example, changing the primary subject or candidate-bar composition after C returns B and C to `pending`.

Read [references/design-approval-playbook.md](references/design-approval-playbook.md) before creating a new visual design or changing motion. When the user requests inspiration or the direction is underspecified, read [references/official-gallery-study.md](references/official-gallery-study.md) and study current official cases before proposing a design.

Route by platform before inspecting or building:

- For macOS `.mssf`, read [references/format-map.md](references/format-map.md).
- For classic Windows `.ssf`, read [references/windows-classic-ssf.md](references/windows-classic-ssf.md).
- If a package claims to be H5 or another modern Windows format, require an authentic locally runnable sample or published schema. Do not fabricate a container from marketing claims.

## Workflow

### 1. Discover and deduplicate the real base

1. Search accessible local sources before contacting the user: current project, prior project paths, conversation-provided paths, Downloads, Sogou installed/allskin/skin folders, and prior work notes. Use `rg --files` first.
2. Hash plausible `.mssf` and `.ssf` files. Treat matching hashes as the same content even when filenames differ; record aliases instead of asking for another copy.
3. Prefer an already proven working base. If the requested file was deleted but its extracted tree, deterministic build script, or hash-verified equivalent remains, reconstruct from those sources instead of asking for re-upload.
4. Inspect the base before editing. Use `inspect_mssf.py` for macOS; for Windows, inspect ZIP members, `skin.ini` encoding, image dimensions, APNG chunks/frames, and referenced assets.

   ```bash
   python3 scripts/inspect_mssf.py path/to/skin.mssf
   ```

5. Record platform, SHA-256, structure, config encoding, image dimensions, APNG timing, padding/margins, offsets, controls, and prior use in the base registry.
6. Save a reversible working copy. Never use the installed folder as the primary source.
7. Ask the user for a file only when all compatible local sources are absent, reconstruction is impossible, and the exact missing user-specific sample is necessary. Do not ask for a generic classic SSF sample. State what was searched and why existing format knowledge is insufficient. Ask once, not repeatedly.

### 2. Study cases and build the reference contract — Gate A

Before drawing, classify the theme as one or more of: `character/animal`, `object`, `brand/IP`, `scene`, `pattern/decorative`, or `minimal/material`. This classification changes the visual hierarchy, not the engineering rules.

Decompose every supplied reference by role. Do not collapse layout, subject identity, ornament, material, and motion references into one vague instruction. If the user supplies a specific image or says “use this exact one,” mark it `exact asset`; preserve its silhouette, internal linework, texture, and color unless a listed technical adaptation is approved.

Also classify supplied skin packages as `format/base reference`, `visual reference`, or both. A format/base reference authorizes structural study, not visual inheritance.

When official-case study is useful, sample diverse Sogou gallery categories and extract composition principles. Do not copy or redistribute third-party/IP artwork. Translate the principle to macOS `.mssf` runtime constraints and the user's own authorized assets.

Present a concise contract containing:

- `must preserve`: exact assets, subject identity, logo geometry, markings, silhouette, pose requirements, palette, layout motifs, required controls, and requested motion;
- `may adapt`: details that must change for 40 pt runtime constraints;
- `must not introduce`: unrequested symbols, mismatched illustration styles, gradients, controls, poses, or decorations;
- `runtime constraints`: canvas sizes, stretch zones, text space, and unavoidable engine limitations;
- `open decisions`: only choices that materially change the result.

Show how each important element from each reference maps to the skin. Ask the user to approve or correct the contract. Stop before drawing until Gate A is explicitly approved.

### 3. Create the static design board — Gate B

After Gate A, create a static approval board at real proportions. It must show:

- short, normal, and long candidate bars;
- normal and selected candidates, including a non-first selected item;
- subject anchor and overlap with text space;
- previous/next controls in every visible state, or an explicit proposal to hide them;
- light and dark desktop backgrounds when transparency is present;
- labeled palette and 1x measurements;
- side-by-side reference mapping so the user can see which design ideas were adopted.

Use final-style artwork for visible components. Do not use placeholder icons that could accidentally ship. Check nine-slice fixed caps and stretch center before presenting.

Ask the user to approve the static board. Stop before final asset production, APNG assembly, plist edits, packaging, or installation until Gate B is explicitly approved.

### 4. Create the motion specification and preview — Gate C

Skip only when the user requests a completely static skin.

Define the animation before producing the final APNG. Motion may belong to a character, object, ornament, material effect, or state transition, but it must match the user's named intent:

- motion intent in one sentence;
- exact body parts that move and parts that stay locked;
- anchor point and maximum displacement in pixels at 2x;
- frame count, timing, loop behavior, and resting duration;
- transition order and whether the motion is state-driven or a continuous loop;
- method used to preserve identity across frames.

Then produce both:

1. a labeled native-2x contact sheet with every frame;
2. a playable preview at intended speed on the candidate bar.

The preview must show the actual approved motion, not proxy symbols. Inspect identity-critical details, fills, seams, transparent edges, and anchors. Also show the first and last frame overlaid or flickered to reveal drift.

When one master or eye/mouth/limb transformation is reused in multiple components, preview and audit every consumer together. A candidate-window approval does not implicitly approve a status-bar frame built by another method.

Ask the user to approve the motion, speed, and amplitude. Stop before final APNG assembly, packaging, or installation until Gate C is explicitly approved.

### 5. Build production assets deterministically

Derive candidate bars and animation frames from the approved sources, not independently generated frames or stale filename caches. Store approved masters in the project source folder; never depend on a clipboard or temporary path for production.

For every imported or generated raster:

1. Inspect the actual alpha channel; a visible checkerboard may be baked opaque pixels.
2. Record the alpha bounding box and safe margins at native size.
3. Separate `content extraction` from `redesign`. Remove background contamination without changing the object.
4. Reject fragments containing old frame lines, colored backing, or neighboring decorations.
5. Never repair a clipped object by placing an approximate second shape underneath it. Recover the full original or request/regenerate the exact asset.
6. Preserve user-approved identity from one master. For character motion, move or replace only the named pixels; do not regenerate the full subject per frame.
7. Treat clarity as an information problem. Do not describe unsharp masking, contrast, or thicker outlines as increased resolution. If runtime pixels are insufficient, propose a larger display size or a proven high-density pipeline.

Typical proven dimensions:

- candidate trunk: `158x40` and `316x80`;
- animated subject: `100x80` and `200x160`;
- compact official notification: `24x24` and `48x48`.

These are baselines. If a canvas changes, adjust `CurOffset`, `Padding`, and `StretchCenter` together.

Use this three-layer geometry model:

1. **Raster layer** — trunk canvas, white capsule, green bands, fixed-cap ornaments, and 1x/2x pixel bounds.
2. **Runtime layout layer** — `FontSetting.Padding` determines much of the real candidate-window height and text inset; `CurOffset`, characterization padding, and stretch center place the raster and optional subject inside it.
3. **Control occupancy layer** — page-control images may remain in layout even when every pixel is transparent. Their canvas size and `PageUpInfo` / `PageDownInfo` padding can create blank space or overlap candidates.

Classify each visible raster element by anchor before resizing:

- `top-cap`: stays at a fixed distance from the candidate-bar top;
- `bottom-cap`: stays at a fixed distance from the bottom;
- `subject-contact`: locks to a measured contact line or attachment point;
- `text-relative`: follows the white capsule or text baseline;
- `stretch-center`: contains only flat or mechanically repeatable pixels.

Do not shift every decoration by one global delta when canvas height changes.

Never exchange one layer for another. In particular:

- To grow outer green bands without shrinking the white capsule, enlarge the trunk canvas, move existing art on the new canvas, adjust `CurOffset` and vertical `StretchCenter`, **and increase the runtime top/bottom padding by the same 1x amount**.
- To move text vertically without resizing the window, add `d` to one vertical font inset and subtract `d` from the other; keep their sum unchanged, then verify in a real candidate window.
- Interpret user-facing `px` as 1x screen points unless they explicitly say native/Retina pixels. Apply twice that delta to `@2x` raster bounds.
- When a region must remain unchanged, compare its source and produced pixel bounds or hashes. Do not rely on visual memory.

For APNG:

1. Render identical full-size canvases.
2. Keep the approved anchor fixed.
3. Export native 2x first; derive or render the matching 1x according to the approved source workflow.
4. Assemble and inspect:

   ```bash
   python3 scripts/apng_tool.py assemble frame0.png frame1.png frame2.png -o chars_0.png
   python3 scripts/apng_tool.py inspect chars_0.png
   ```

Reject production frames that differ from the approved contact sheet except for documented technical corrections.

### 6. Configure the platform-specific skin file

For macOS, configure `skin.plist` and validate with `plutil` as described below.

Edit only necessary nodes and preserve unknown keys from the working base:

- `SkinInfo.TrunkImageInfo`: trunk, nine-slice center, offset, and shadow;
- `SkinInfo.Characterization`: optional subject/APNG, level, alignment, and padding;
- `SkinInfo.FontSetting`: normal and selected text/background states;
- `PageUpInfo` / `PageDownInfo`: approved page-control assets and padding;
- `NotificationInfo.HummingNotif`: official Chinese/English notification.

Validate after every structural edit:

```bash
plutil -lint skin.plist
```

Before packaging, record at least:

- trunk 1x/2x dimensions and `CurOffset`;
- white-capsule pixel bounds at 2x;
- `FontSetting.Padding` and its vertical sum;
- page-control canvas sizes, alpha visibility, and page-control padding;
- subject anchor and candidate-text left/right safe areas;
- each visible decoration's anchor class, alpha bounding box, and edge-safe margin.

If page controls are intentionally hidden, prefer minimal transparent canvases and test whether Sogou still reserves their layout width. Compensate the real occupied width, not merely the visible pixels.

For classic Windows, preserve the working base's `skin.ini` encoding and unknown keys. Treat background raster geometry, pinyin/candidate margins, custom-layer canvases, runtime separators, and control occupancy as independent. Never bake a separator that the runtime already draws. Keep language and menu normal/hover/pressed assets separate from animated base art.

### 7. Package and validate

For macOS, the outer `.mssf` must contain exactly one file named `Skin`; that inner ZIP contains `skin.plist` and assets.

```bash
python3 scripts/pack_mssf.py path/to/inner-folder output.mssf
python3 scripts/inspect_mssf.py output.mssf --json
```

Reject the build when:

- any approval gate required for the build is pending;
- the plist is invalid or a referenced asset is missing;
- a 2x asset is not exactly double its 1x counterpart;
- APNG canvas, frame count, timing, or anchor differs unexpectedly;
- a visible asset was absent from the approved static or motion preview;
- the outer member is not exactly `Skin`.

For classic Windows, reproduce the proven base's archive layout and compression exactly. Common classic bases are flat ZIPs with UTF-16LE+BOM `skin.ini` and PNG/BMP/APNG members, but inspect rather than assume. Validate CRC, config encoding, referenced assets, member order/count when required, APNG frame RGBA/timing, changed-member allowlist, package-size limits, and a second deterministic build hash.

### 8. Install and runtime-test — Gate D

1. Change both package filename and `SkinName` to defeat caching.
2. Install through Sogou and confirm `keySkinPath` points to the new version.
3. Hash the installed `skin.plist`, trunk, page assets, and primary animation against the source. Installation is not verified until they match.
4. Invoke the full runtime matrix:
   - one short candidate;
   - five normal and long candidates;
   - first and non-first selection;
   - page controls or their intentionally hidden state;
   - every animation frame at least twice;
   - Chinese/English switching;
   - light and dark backgrounds when transparency is used.
5. Compare runtime screenshots to the approved board using a semi-transparent overlay. Measure the white-region center, visible glyph bounds, left/right whitespace, subject contact points, and control alpha bounds numerically.
6. If automation cannot invoke candidates, stop and ask the user for runtime screenshots. Installation success, package inspection, and a synthetic preview are not runtime approval; do not claim the result was self-checked in runtime.
7. Fix the source, increment the version, and repeat. Never patch only the installed copy.

On Windows, change both `skin_name` and `skin_version` when the base supports them, then test real pinyin/candidate geometry, first and non-first selection, page controls, Chinese/English display, menu normal/hover/pressed/click, candidate APNG, status APNG, and light/dark backgrounds. Do not treat package validation as Windows runtime approval.

Read [references/qa-playbook.md](references/qa-playbook.md) when diagnosing mismatches.

## Visual consistency checks

- Set a deliberate hierarchy for the selected theme. Candidate text must remain readable; the subject may be primary visually, while ornaments remain subordinate.
- Match all visible components to the approved art system: line weight, fill treatment, texture, edge softness, lighting, and palette.
- Do not mix crisp geometric icons with watercolor, pencil, collage, pixel, or hand-painted artwork unless the contrast was approved.
- Place important art only in fixed nine-slice caps; keep the stretch zone mechanically safe.
- Treat “restore” feedback as removal of the rejected visual while retaining independent technical fixes.

## Revision discipline

For every user correction:

1. Quote the requested delta in 1x pixels.
2. State which raster bounds and plist fields will change.
3. State which artifacts must remain identical.
4. Rebuild from a named clean master with approved decoration and no rejected controls; never repeatedly bake new visuals onto the prior generated trunk.
5. Compare RGB and alpha differences separately against the prior accepted version. Verify the changed bounding box stays inside the declared change region.
6. Never reinterpret “increase green area” as “shrink white area” unless the user explicitly asks to trade one for the other.
7. Rebuild the preview canvas from current native asset dimensions. A clipped preview is not evidence that the source raster is clipped, and a roomy preview is not evidence that runtime is safe.
8. Distinguish incremental language (`increase by 5 px`, `move left 10 px`) from absolute language (`set to 5 px`, `x = 10`). Record both old and new values.
9. If an accepted file disappears, reconstruct from the named clean master, build script, approved frames, and hashes. Never improvise a replacement from memory.
10. When a user reports one shared-frame defect, audit every component derived from the same source before declaring it fixed.

Read [references/qa-playbook.md](references/qa-playbook.md) for failure patterns discovered during iterative runtime calibration.

## Handoff

Provide:

- the approved design board and motion preview;
- the final `.mssf` or `.ssf` and editable source folder;
- a list of retained, changed, and intentionally hidden behaviors;
- validation results for platform-specific package structure, dimensions/density, APNG frames, active version, changed-member allowlist, and runtime matrix;
- any runtime states still awaiting user evidence.
