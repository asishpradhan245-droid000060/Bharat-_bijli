
# BHARAT BIJLI - Kivy Android App (GitHub Build Template)

This repository contains your Kivy app `electric.py` with the tricolor theme and animated Ashoka Chakra.
Use the included `buildozer.spec` and GitHub Actions (or local Buildozer) to build an APK.

## Files
- `electric.py` - Main Kivy app (your code, unchanged).
- `logo.png` - Placeholder icon (replace with your own if desired).
- `buildozer.spec` - Buildozer configuration (ready for Android).
- `requirements.txt` - Python dependencies.
- `.github/workflows/android-build.yml` - (optional) GitHub Actions workflow to automate APK builds.

## Build using GitHub Actions (recommended)
1. Create a new GitHub repository and upload all files from this ZIP.
2. Go to **Actions** → enable workflows → run the `Android Build` workflow.
3. Wait ~20-30 minutes for the build to complete.
4. Download the APK from the workflow artifacts.

## Or build locally (WSL / Ubuntu)
1. `sudo apt update && sudo apt install -y python3-pip git zip unzip openjdk-17-jdk`
2. `pip install buildozer cython kivy`
3. Run `buildozer init` then `buildozer -v android debug`.

