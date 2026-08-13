#!/usr/bin/env node
// Thin npm wrapper — shells the CANONICAL Python `csoai` CLI. No reimplementation,
// so the engine has exactly one source of truth (the Python package).
const { spawnSync } = require("child_process");
const args = process.argv.slice(2);
function run(cmd, cmdArgs) { return spawnSync(cmd, cmdArgs, { stdio: "inherit" }); }
let r = run("csoai", args);                                   // csoai on PATH
if (r.error && r.error.code === "ENOENT") r = run("python3", ["-m", "csoai.cli", ...args]);
if (r.error && r.error.code === "ENOENT") {
  console.error("csoai (Python) not found. Install it first:  pip install csoai");
  process.exit(127);
}
process.exit(r.status === null ? 1 : r.status);
