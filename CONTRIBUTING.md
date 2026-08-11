# Contributing

Contributions are welcome when they improve format inspection, packaging safety, runtime calibration, or documentation without adding proprietary/user assets.

Before submitting a change:

1. Keep the Skill package self-contained under `skill/sogou-macos-skin-maker/`.
2. Do not commit `.ssf`, `.mssf`, generated skins, screenshots containing personal data, or third-party artwork.
3. Preserve the separation between macOS `.mssf`, Windows classic `.ssf`, and unsupported modern/H5 formats.
4. Run `python3 -m unittest discover -s tests -v`.
5. Describe which runtime or package structure was actually tested; do not present synthetic previews as runtime verification.
