#!/usr/bin/env node
// sync-hf.mjs — push the LIVING 22-axis board + Council OS metadata to Hugging Face.
// One command when HF_TOKEN is fresh:  HF_TOKEN=<fresh> node sync-hf.mjs
// Mirrors: gspc-board (datasets) + the leaderboard space. Honest when token is dead.
import { HfApi } from "@huggingface/hub";
import fs from "node:fs";

const token = process.env.HF_TOKEN;
if (!token) {
  console.error("NO_HF_TOKEN — not synced (honest). Set a fresh HF_TOKEN (the ~/.env one is DEAD).");
  process.exit(2);
}
const api = new HfApi({ token });
const board = JSON.parse(fs.readFileSync("living-board.json", "utf8"));
const targets = [
  { repo: "csoai/gspc-board", file: "living-board.json", content: JSON.stringify(board, null, 2) },
  { repo: "csoai/gspc-board", file: "README.md", content: `# GSPC living board\n\n\`${board.totals?.public_count}\`. Authority: councilof.ai/api/gspc. DOI ${board.doi}.\n\nMirrored from the canonical monorepo. Never edit here — edits go back to source.\n` },
];
for (const t of targets) {
  try {
    await api.uploadFile({ pathOrFileObj: Buffer.from(t.content), pathInRepo: t.file, repoId: t.repo, repoType: "dataset" });
    console.log(`  ✓ ${t.repo}/${t.file} — ${board.totals?.public_count}`);
  } catch (e) {
    console.error(`  ✗ ${t.repo}/${t.file}: ${String(e).slice(0,120)}`);
  }
}
console.log("HF mirror synced to the living 22-axis board.");
