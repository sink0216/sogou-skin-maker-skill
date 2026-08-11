# Runtime QA and failure playbook

## Contents

- [Required runtime matrix](#required-runtime-matrix)
- [Symptom → likely cause → fix](#symptom--likely-cause--fix)
- [Figma calibration loop](#figma-calibration-loop)

## Required runtime matrix

Test all of these after every meaningful build:

1. One short candidate.
2. Five normal candidates.
3. Long candidates that stretch the bar.
4. First and non-first selected candidate.
5. Page controls or their intentionally hidden state.
6. Every animation frame at least twice.
7. Chinese and English switch notifications.
8. Light and dark desktop backgrounds when transparency is used.

## Symptom → likely cause → fix

### The user is asked to provide the same Sogou skin again

- Cause: discovery relied on the current filename instead of prior paths, extracted trees, work notes, and content hashes.
- Fix: search the accessible workspace, conversation paths, Downloads, installed skin folders, base/dist/build folders, and work notes; hash candidates and record aliases. Reconstruct from a clean extracted tree or deterministic build when possible. Ask only if no compatible local source exists and the missing format genuinely blocks progress. Never reuse private files across users.

### A format-only base influences the new visual design

- Cause: package structure and visual reference roles were merged.
- Fix: classify the package as `format/base reference` and inherit only encoding, member layout, config schema, and proven runtime mechanics. Keep its artwork, palette, composition, and subject out of the new reference contract.

### User says the design reference was ignored

- Cause: mascot identity, layout reference, and decorative reference were merged into one vague visual prompt.
- Fix: complete Gate A with separate `must preserve / may adapt / must not introduce` mappings for every reference. In Gate B, show the mapping beside the real-proportion candidate bar.

### Animation moves an unexplained symbol instead of the mascot

- Cause: motion was produced before body-part and anchor approval.
- Fix: specify which eyes, ears, paws, tail, or mouth move. Lock all other pixels. Hearts or action marks may accompany the mascot only when approved; they cannot substitute for character motion.

### A packaged build mixes approved and stale animation

- Cause: approval was tracked at the overall-skin level instead of candidate subject, companion, status subject, ornaments, and controls.
- Fix: maintain a component approval matrix and build every packaged APNG from the exact approved frame folders. If one stale component ships, withdraw the package and reopen Gate C for every affected consumer.

### Paw prints or small icons have a different drawing style

- Cause: generic icons or separately generated assets were mixed with the mascot.
- Fix: derive ornaments from the approved illustration language: matching outline weight, fill texture, palette, and edge softness. Approve them at runtime size, not only enlarged.

### A cleaned or extracted asset no longer matches the chosen reference

- Cause: background removal, crop repair, or transparency cleanup silently became a redraw.
- Fix: classify the source as an `exact asset` before editing. Preserve the original silhouette, internal lines, texture, and color. Limit changes to documented background pixels and show a before/after overlay before packaging.

### A generated “transparent” asset still has a checkerboard or solid background

- Cause: the generator painted a checkerboard into opaque RGB pixels; the preview was trusted without inspecting alpha.
- Fix: inspect alpha extrema, corner alpha, alpha bounding box, and margins. If alpha is fully opaque, perform controlled matting/segmentation or regenerate; never composite the baked checkerboard into the trunk.

### A decorative fragment contains a border line or colored backing

- Cause: the ornament was cropped from a flattened candidate-bar screenshot and carried neighboring pixels with it.
- Fix: use a clean source asset or isolate it with alpha inspection. Reject any crop containing frame colors, stretch lines, or adjacent ornament pixels.

### A clipped object becomes doubled, split, or misshapen after repair

- Cause: an approximate second drawing was layered beneath the clipped original.
- Fix: recover the full original asset or recreate the exact asset as a single approved master. Never patch missing silhouette with a merely similar shape.

### An edge decoration is cropped in preview or runtime

- Cause: its alpha bounding box touches the source canvas, fixed cap, or preview container edge.
- Fix: measure alpha margins at native 2x, add an explicit safe margin, and check both the native asset and the composite. Keep preview dimensions synchronized with the current trunk/subject canvas.

### Top ornaments move downward when the bar grows taller

- Cause: all decorations were shifted by one global canvas-height delta.
- Fix: assign anchor classes before resizing. Keep top-cap items top-relative, bottom-cap items bottom-relative, subject contact points locked, and text-relative elements tied to the capsule/baseline.

### Text or mascot disappears in the switch notification

- Cause: the real HUD is compact and does not expand to editor-preview dimensions.
- Fix: restore the local official asset and full `HummingNotif` configuration. Avoid moving text to large x coordinates.

### Text overlaps a switch icon

- Cause: image details occupy the same center reserved for runtime text.
- Fix: use the official style or leave the center empty; test the real HUD.

### Mascot looks different between frames

- Cause: frames were independently generated or redrawn.
- Fix: derive all frames from one master and move only paw, tongue, tail, or action marks.

### Static line moves with the cat

- Cause: the line was included in APNG frames.
- Fix: move it into the trunk/static layer. Animated frames must contain only animated content.

### Animation is blurry

- Cause: missing or fake 2x assets, upscaled 1x images, or mismatched frame dimensions.
- Fix: render native 2x frames from source and verify exact double dimensions.

### “Clarity improvement” only adds sharpening or outline

- Cause: edge contrast was mistaken for additional image information, or the client resampled a tiny single-density raster.
- Fix: stop unsharp/outline tuning after the premise is rejected. Diagnose final display pixels and client scaling separately. Propose a larger subject or a proven high-density pipeline; do not promise detail that the runtime cannot display.

### A blink leaves black dots, iris fragments, or old lashes

- Cause: the replacement covered only the eye center while original upper/terminal lash pixels remained outside the mask.
- Fix: inspect the open master at high resolution, clear the complete eye cavity and original lash terminals, overlay the approved closed-eye asset, then inspect actual-size and nearest-neighbor crops. Audit every candidate/status consumer derived from the same master.

### Closed-eye lashes become too short at runtime size

- Cause: global face mapping and final downsampling removed terminal pixels even though the enlarged reference looked correct.
- Fix: measure the final-size lash bbox, preserve the exact source shape, and apply only documented runtime-size survival compensation. Recheck left/right asymmetry and residue pixels in every consumer.

### One tongue or marking is white

- Cause: an intermediate frame has an outline but inherited the white body fill.
- Fix: inspect frame crops at nearest-neighbor magnification and standardize fill colors in every frame before rebuilding APNG.

### Selected candidate is not visually selected

- Cause: only normal `Style` changed, or `HotStyle` and `HotBgColor` were confused.
- Fix: set and runtime-test selected text color, background color, and padding independently.

### Large empty space appears on the left

- Cause: `Characterization.Padding`, `TrunkImageInfo.CurOffset`, and trunk cap width no longer agree.
- Fix: return to known-working values; adjust one parameter at a time while preserving the mascot anchor.

### Mascot paw floats above or detaches from the candidate frame

- Cause: characterization anchor, trunk offset, and fixed left cap were adjusted independently.
- Fix: lock a screen-space paw contact line. Change `Characterization.Padding`, `CurOffset`, or canvas placement only with an overlay against that line; verify short and long bars.

### Candidate text enters the green border or is not vertically centered

- Cause: text was judged from the PNG instead of the runtime glyph bounds, or font padding was changed without measuring its total.
- Fix: measure the white-capsule top/bottom and the visible runtime glyph top/bottom. Move text with `top += d` and `bottom -= d` so the vertical padding sum remains unchanged. Re-test selected and unselected candidates because selected-pill padding can alter the optical result.

### “Increase padding by 5 px” becomes “set padding to 5 px”

- Cause: incremental and absolute language were not recorded explicitly.
- Fix: write `old → new` before editing. Treat “increase/move by d” as a delta and “set to d/x = d” as absolute. Reject any revision that changes another padding family.

### Candidate subjects stretch or make the window unexpectedly tall

- Cause: characters were baked into the stretchable background, or a transparent custom canvas still occupied runtime geometry.
- Fix: separate background, left subject, and right subject; then measure custom canvas occupancy independently from visible alpha. Preserve the approved background/padding while changing only the subject layer architecture.

### Two separator lines appear in the candidate window

- Cause: one line is baked into the raster and another is drawn by the runtime.
- Fix: identify both sources and remove only the duplicate. Do not remove runtime spacing or redraw the whole candidate background.

### Increasing the green bands shrinks or squeezes the white capsule

- Cause: the trunk bitmap was made taller without enlarging the Sogou runtime layout, or green was added inside a fixed-height canvas by moving white-capsule edges.
- Fix: keep the approved white-capsule pixel bounds unchanged; enlarge 1x/2x trunk canvases outward; shift existing art on the new canvas; adjust `CurOffset` and vertical `StretchCenter`; increase runtime top/bottom `FontSetting.Padding` by the same 1x delta. Verify the old and new white-region hashes/bounds before installing.

### A requested 2 px change becomes 1 px or 4 px

- Cause: screen points and native Retina pixels were mixed.
- Fix: treat user-visible px as 1x by default. Apply `2 × delta` to @2x assets, then downsample to 1x and report both measurements.

### A page “×” or arrow blocks candidates

- Cause: a page-control asset is still visible or placed inside text space.
- Fix: use transparent page assets or correct their padding. Do not merely push them off-canvas.

### Two page arrows cannot be aligned even when their PNGs are aligned

- Cause: Sogou applies different runtime anchors or baselines to PageUp and PageDown.
- Fix: measure each runtime alpha bound separately. If the controls are keyboard-only, explicitly propose hiding them. If visuals are still required, place a single approved static visual pair in a fixed cap and make native assets transparent, while clearly documenting that the visual pair is non-clickable decoration.

### Page arrows are invisible but the right side still has excessive whitespace

- Cause: fully transparent page assets and their padding still reserve layout width.
- Fix: inspect control canvas dimensions and `PageUpInfo` / `PageDownInfo` padding. Use minimal transparent canvases when compatible, or reduce the font/right padding by the measured runtime occupancy. Never assume alpha transparency removes layout space.

### A fixed paw, dot matrix, or right-cap icon stretches with long candidates

- Cause: visible decoration crossed the nine-slice stretch center.
- Fix: keep all textured or figurative pixels wholly inside fixed caps. The stretch center may contain only flat fill and mechanically stretch-safe lines. Test the same raster at short and very long widths.

### Colors or images do not change after rebuilding

- Cause: renderer or Sogou cache reused a filename/version.
- Fix: rasterize from source bytes, inspect actual output pixels/hashes, change `SkinName` and package filename, then reinstall.

### A rebuild accumulates old arrows or stale decoration

- Cause: each version used the prior generated trunk as its new source and baked another visual layer on top.
- Fix: rebuild from a named, decoration-complete but control-free base. Keep source art separate from generated output. Compare trunk hashes when a revision claims not to touch the raster.

### Deleting an old file makes later revisions drift

- Cause: generated output rather than a named clean master and deterministic script was treated as the source of truth.
- Fix: reconstruct from the registered base hash, extracted tree, approved frames, and build script. Do not redraw from memory or ask for a duplicate upload when equivalent local content remains.

### Reconnected workspace no longer contains early approval assets

- Cause: temporary or scratch approval paths were treated as permanent production sources.
- Fix: preserve editable masters and final approved frames inside the production source folder. If only final production assets remain, reuse them without redrawing the mascot; never silently regenerate identity-critical art.

### A revision fixes one detail but alters unrelated art

- Cause: the whole trunk was re-rendered, or RGBA diff bounds were interpreted from only one channel.
- Fix: declare an allowed change rectangle; compare RGB and alpha differences separately; reject any diff outside it. Preserve unrelated accepted regions byte-for-byte when possible.

### The preview reports clipping that the source asset does not have

- Cause: the preview stage retained an older fixed canvas after the trunk or subject grew.
- Fix: derive preview bounds from current native assets. Inspect the source alpha bbox separately from preview layout and from installed runtime clipping.

### Preview looks correct but runtime is wrong

- Cause: editor preview dimensions or font metrics differ from the Sogou runtime.
- Fix: treat runtime screenshots as ground truth. Overlay them in Figma for measurement.

### Package validates and installs, but the result was not actually runtime-tested

- Cause: package inspection, active `keySkinPath`, or a synthetic safety map was mistaken for Gate D.
- Fix: invoke real Chinese composition and capture the candidate window. If automation cannot switch the IME or the target app changes continuously, ask the user for a fresh runtime screenshot and leave Gate D pending.

### Installed skin differs from the source under review

- Cause: the wrong nested `Skin/` path was hashed, or installation/cache selection was assumed.
- Fix: resolve the active `keySkinPath`, then hash installed and source `Skin/skin.plist`, `skin@2x.png`, page assets, and the primary character APNG. Require byte-for-byte matches before diagnosing renderer behavior.

### Decorative lines look chaotic at long widths

- Cause: nine-slice stretching elongated or repeated illustration details.
- Fix: keep decorative details in fixed left/right caps, use stretch-safe straight segments, or remove them. Test short and long candidate bars.

## Figma calibration loop

1. Create a 1x frame matching the actual trunk and mascot point sizes.
2. Place runtime screenshot beneath the Figma design at 50% opacity.
3. Compare anchors, not the full canvas: box top-left, text baseline, selected pill, mascot paws, and right cap.
4. Correct source measurements.
5. Export both 1x and 2x.
6. Repackage with a new version and repeat.

Do not resize the runtime screenshot non-uniformly to make it fit; that hides real stretch errors.
