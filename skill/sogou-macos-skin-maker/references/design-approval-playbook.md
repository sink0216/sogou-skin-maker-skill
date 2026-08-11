# Design and animation approval playbook

Use this playbook for new skins and any revision that changes subject identity, exact supplied artwork, composition, controls, or motion.

## Contents

- [Gate A — reference contract](#gate-a--reference-contract)
- [Gate B — static design board](#gate-b--static-design-board)
- [Gate C — animation preview](#gate-c--animation-preview)
- [Revision rules](#revision-rules)

## Gate A — reference contract

Present one table:

| Reference | Role | Must preserve | May adapt | Must not introduce |
|---|---|---|---|---|
| Layout reference | Structure/style | Candidate structure, hierarchy, palette, control metaphors | Measurements required by runtime | Unrequested components |
| Subject reference | Identity | Exact asset status, silhouette, markings/logo, line/fill treatment | Approved scale, crop, or pose changes | Replacement subject or different art style |
| Ornament reference | Detail system | Shape language, texture, palette, density | Runtime-size simplification | Generic mismatched icons |
| Motion reference | Behavior | Named moving part, timing, amplitude | Frame count required by runtime | Proxy motion unrelated to the request |
| Existing skin package | Format/base or visual reference | Declared role only; structure when format-only | Technical measurements required by runtime | Silent inheritance of artwork, palette, layout, or old design |

Label each supplied raster as `exact asset`, `identity reference`, `style reference`, or `layout reference`. “Remove the background” on an exact asset means preserve its internal pixels and silhouette while cleaning only the background.

Label each supplied skin package as `format/base reference`, `visual reference`, or both. A format-only package authorizes structural inspection but no visual inheritance.

Also state engine constraints and open decisions. Use precise visual language. “Inspired by” is not a sufficient mapping.

Approval prompt: `请确认这份参考图映射；确认后我才制作静态设计板。`

## Gate B — static design board

Deliver a single board with labeled panels:

1. short candidate;
2. normal five-candidate state;
3. long stretched state;
4. first candidate selected;
5. non-first candidate selected;
6. previous/next controls, including hover/pressed/disabled if visible;
7. light/dark transparency check;
8. measurements and palette;
9. reference-to-output callouts.

Review before presenting:

- subject does not cover text;
- selected state is unmistakable;
- fixed-cap art does not cross the stretch center;
- all controls and ornaments share the approved art treatment;
- no placeholder or unapproved decoration is visible.

Approval prompt: `请确认布局、色彩、角色位置和翻页控件；确认后我才制作动画。`

## Gate C — animation preview

First present a motion table:

| Property | Required answer |
|---|---|
| Intent | What the subject or visual state is doing |
| Moving parts | Specific body parts |
| Locked parts | Face, markings, feet, anchor, etc. |
| 2x displacement | Maximum x/y movement in pixels |
| Frames | Count and labeled sequence |
| Timing | Per-frame or phase duration |
| Loop | Continuous, intermittent, or state-driven |

Then deliver:

- a native-2x contact sheet with frame numbers;
- a playable preview at intended runtime speed;
- first/last-frame difference or overlay;
- a candidate-bar composite, not an isolated subject only.

Also deliver a component approval matrix when motion appears in more than one asset:

| Component | Source/master | Motion | Timing | Approval |
|---|---|---|---|---|
| Candidate primary subject | | | | pending/approved |
| Candidate companion | | | | pending/approved |
| Status primary subject | | | | pending/approved |
| Status ornaments/stars | | | | pending/approved |
| Language/menu controls | | | | unchanged/approved |

Show actual runtime-size playback and magnified identity-critical crops. Inspect every consumer of a shared eye, mouth, limb, or transformation together.

Reject the preview if:

- the user asked for subject motion but only proxy symbols move;
- unapproved hearts, dots, punctuation, sparkles, or action lines appear;
- identity, logo geometry, markings, silhouette, or art style changes between frames;
- seams, transparent holes, clipping, or anchor drift are visible;
- the motion is imperceptible at actual candidate-bar size;
- static candidate-bar decoration moves with the subject.
- an original eye/marking remains as an isolated dot or ghost beside the animated replacement;
- a lash, ear tip, paw, or marking disappears only after final-size rasterization;
- one component uses stale motion that was never included in the current approval preview.

Approval prompt: `请确认动作内容、幅度和速度；确认后我才组装最终 APNG 和皮肤包。`

## Revision rules

- A reference, exact asset, or primary-subject change invalidates A, B, and C.
- A layout, color, or control change invalidates B and any affected composite in C.
- A motion, timing, or anchor change invalidates C.
- A technical correction that does not alter approved appearance may retain approval, but document it.
- Approval is component-specific. Approval of a candidate animation does not approve a separately built status animation.
- Never treat a package inspection result as visual approval.
