# Sogou macOS skin format map

## Contents

- [Package structure](#package-structure)
- [Important plist paths](#important-plist-paths)
- [Common asset sizes](#common-asset-sizes)
- [APNG expectations](#apng-expectations)
- [Installed locations](#installed-locations)

## Package structure

```text
skin-name.mssf                 outer ZIP
└── Skin                      inner ZIP stored as a file with no extension
    ├── skin.plist
    ├── skin.png
    ├── skin@2x.png
    ├── chars_0.png
    ├── chars_0@2x.png
    └── ...
```

The outer archive should contain only `Skin`. The inner archive holds the plist and resources at its root.

## Important plist paths

### Metadata

- `AdditionalInfo.SkinName`: visible name. Change it for every test install.
- `AdditionalInfo.MiniumSupportVersion`: preserve from the working base.
- `AuthorInfo`: author and description metadata.

### Candidate bar

- `SkinInfo.TrunkImageInfo.ImgNode.ImgName`: trunk background.
- `SkinInfo.TrunkImageInfo.ImgNode.StretchCenter`: `x,y,width,height` nine-slice center.
- `SkinInfo.TrunkImageInfo.CurOffset`: background offset relative to logical content.
- `SkinInfo.TrunkImageInfo.Shadow`: runtime shadow.

Nine-slice stretching is the main reason decorative lines deform at different candidate widths. Keep important illustration shapes in fixed caps or explicitly design the center segment to stretch.

### Mascot

- `SkinInfo.Characterization[].Component[].ImgName`: PNG or APNG.
- `Padding`: four-value placement adjustment; preserve a known-working base and change one axis at a time.
- `Level`: layer order. A mascot usually sits above text and trunk.
- `Alignment`: engine alignment code; avoid changing without a reference skin.

### Typography and selection

- `SkinInfo.FontSetting.Style`: normal candidate text.
- `SkinInfo.FontSetting.HotStyle`: selected candidate text.
- `SkinInfo.FontSetting.HotBgColor`: selected background color.
- `SkinInfo.FontSetting.HotBgPadding`: selected pill padding.
- `SkinInfo.FontSetting.Padding`: candidate content insets.

Selected text and selected background are independent. Verify both in the runtime.

### Page controls

- `SkinInfo.PageUpInfo.Component[]`
- `SkinInfo.PageDownInfo.Component[]`

If the user wants no visible page symbols, use transparent assets rather than moving them outside the canvas.

### Chinese/English notification

For the current Sogou default light skin observed on macOS:

- common image: `Skins/_common/humming_def.png` (`24x24`)
- Retina image: `humming_def@2x.png` (`48x48`)
- text: white, `LucidaGrande`, size `14`
- typical `TextPos`: type 0 and most states `5,2`; type 1 `4,2`
- animation: `AnimIn=301`, `AnimOut=302`
- offset: `1,1`

Copy the complete `NotificationInfo.HummingNotif` array from the locally installed official default skin because versions may differ. Copy the common images into the custom package too; do not assume a custom skin can resolve global assets.

## Common asset sizes

The following sizes worked reliably in one modern macOS Sogou build:

| Asset | 1x | 2x |
|---|---:|---:|
| Candidate trunk | 158x40 | 316x80 |
| Character animation | 100x80 | 200x160 |
| Official switch badge | 24x24 | 48x48 |

Treat them as a starting point. Verify the installed Sogou version and reference skin.

## APNG expectations

- PNG signature and `IHDR` remain standard.
- `acTL` declares frame count and loop count.
- Each frame has `fcTL`.
- Frame 0 uses `IDAT`; later frames use `fdAT` with sequence numbers.
- Full-frame animation is easiest to maintain: identical dimensions, zero offsets, and consistent blend/dispose settings.
- A proven timing was `28/100` seconds per frame with infinite loop, but use the user's intended motion.

## Installed locations

Common paths include:

```text
/Library/Input Methods/SogouInput.app
~/Library/Application Support/Sogou/InputMethod/SogouPY.users/<id>/Skins
~/Library/Application Support/Sogou/InputMethod/SogouPY.users/<id>/UserPreferences.plist
```

Read the active path from `keySkinPath`. Do not assume the newest folder is active.
