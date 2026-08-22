This is the stable estate dashboard (csoai-org.pages.dev).
Standalone hub: index.html (the unified AG-UI home, 10 tabs) + registers-data.json.
It reads /api/* from the csoai-site project (board/models/arena/etc). For full
stability independent of the csoai-site deploy race, the fallback embedded data
in registers-data.json covers the registers tab offline.
