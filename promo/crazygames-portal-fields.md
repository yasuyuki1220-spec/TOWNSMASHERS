# CrazyGames developer portal: required fields (memo)

Learned while submitting. Game name in the portal: "TOWNSMASHERS!" (the name "TOWNSMASHERS" / "TOWN SMASHERS" was already taken by two drafts).

## Flow
1. Upload the zip (`./build.sh` -> `dist/town-smashers.zip`) -> fill game details -> Preview -> **Continue to last step** -> **Submit** (until submitted the game stays DRAFT; nothing is reviewed).
2. Page content is lost if you reload before saving. Save first, use a desktop browser.
3. Basic Launch: ads are not allowed, SDK checklist is informational only.

## Game details
- Name must be unique (duplicates give "Game name is already used").
- Category: Action (+ Multiplayer / Battle / .io / Funny if selectable). Tags: see `crazygames-submission.md`.
- Short + long description, controls text: see `crazygames-submission.md`.
- Tools: HTML5 / JavaScript (three.js + PeerJS, no engine). AI use: code, SFX and music made with AI (Claude).
- Mobile friendly: checked, orientation "Both".
- **Multiplayer: checked -> lobby size is REQUIRED. Min 1 / Max 15** ("Online lobby size with friends"). If Min will not accept input, set Max first, select-all then type, or use the arrow keys.
- Supports CrazyGames mute audio via SDK: checked.
- Google Play / iOS / Steam links, downloads, marketing URL: leave empty.

## Images (all required)
- Landscape 16:9 **1920x1080**: `thumb_1920x1080.png`
- Portrait 2:3 **800x1200**: `cover_800x1200.png`
- Square 1:1 **800x800**: `cover_800x800.png`
- Preview videos: landscape and portrait both needed (15 s, no audio, sizes 1920x1080 / 800x1200 used so far; check the portal's stated limits).
