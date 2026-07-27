import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

USER = "root"
HOSTS = {
    "top-bench": ("69.30.85.23", "22087"),
    "fresh-a40": ("194.68.245.24", "22087"),
    "h100": ("62.169.159.96", "12704"),
}


IDENTITY = os.environ.get("SOV_SSH_IDENTITY") or os.path.expanduser("~/.ssh/id_ed25519")


def ssh_args(host_alias):
    host, port = HOSTS[host_alias]
    return ["ssh", "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new", "-o", "IdentitiesOnly=yes", "-i", IDENTITY, "-p", port, f"{USER}@{host}"]


EXCLUDE_DIR_NAMES = {".git", "node_modules", "__pycache__", ".cache", ".venv", "venv", ".tox", ".gradle", "target", "dist", "build", "out"}
EXCLUDE_FILE_SUFFIXES = (".pyc", ".wasm", ".map")
EXCLUDE_GLOBS = ["**/.env", "**/.env.*", "**/*.pem", "**/*.key", "**/*.p12", "**/*secret*", "**/*credential*", "**/.runpod/", "**/.ssh/", "**/.aws/", "**/.kube/"]


def is_excluded(path):
    if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
        return True
    if path.suffix.lower() in EXCLUDE_FILE_SUFFIXES:
        return True
    for pattern in EXCLUDE_GLOBS:
        if path.match(pattern):
            return True
    return False


def enumerate_payload(root, includes):
    items = []
    for include in includes:
        source = root / include
        if not source.exists():
            print(f"  skip (missing): {include}")
            continue
        if source.is_file():
            if is_excluded(source):
                print(f"  skip (excluded): {include}")
                continue
            items.append(source)
        else:
            for path in sorted(source.rglob("*")):
                if path.is_dir():
                    if any(part in EXCLUDE_DIR_NAMES for part in path.relative_to(root).parts):
                        continue
                    continue
                rel = path.relative_to(root)
                if is_excluded(rel):
                    continue
                items.append(path)
    return sorted(set(items))


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(path, items, source_root):
    manifest = {
        "schema": "sov-migration-manifest/v1",
        "source_root": str(source_root),
        "items": [],
    }
    for path in items:
        rel = path.relative_to(source_root)
        manifest["items"].append({"path": str(rel), "size": path.stat().st_size, "sha256": sha256_file(path)})
    canonical = json.dumps(manifest, sort_keys=True, ensure_ascii=False).encode()
    manifest["sigil"] = hashlib.sha256(canonical).hexdigest()
    path.write_bytes(canonical + b"\n")
    return manifest


def run_remote(cmd, host_alias):
    host, _ = HOSTS[host_alias]
    completed = subprocess.run([*ssh_args(host_alias), cmd], capture_output=True, text=True, check=True)
    return completed.stdout


SSH_IDENTITY = IDENTITY


def _quote(value):
    return f"'{value.replace(chr(39), chr(39) + chr(92) + chr(39) + chr(39))}'"


def _shell_path(path):
    return _quote(str(path))


def upload(host_alias, items, source_root, remote_root):
    host, port = HOSTS[host_alias]
    targets = {remote_root}
    for path in items:
        rel = path.relative_to(source_root)
        parent = rel.parent.as_posix()
        if parent:
            targets.add(f"{remote_root}/{parent}")
    for target in sorted(targets):
        run_remote(f"mkdir -p {target}", host_alias)
    for index in range(0, len(items), 25):
        chunk = list(items)[index:index + 25]
        commands = []
        for path in chunk:
            rel = path.relative_to(source_root)
            target = f"{remote_root}/{rel}"
            commands.append(["scp", "-P", port, "-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=accept-new", "-o", "IdentitiesOnly=yes", "-i", SSH_IDENTITY, str(path), f"{USER}@{host}:{target}"])
        if index == 0 or index + 25 >= len(items):
            print(f"  upload {min(index + 25, len(items))}/{len(items)}")
        for command in commands:
            completed = subprocess.run(command, capture_output=True, text=True)
            if completed.returncode != 0:
                sys.stderr.write(completed.stderr[-2000:])
                raise SystemExit(f"upload failed: {' '.join(command[:3])}: {completed.stderr[-2000:]}")


def verify(host_alias, items, source_root, remote_root, manifest):
    remotes = {item["path"]: item["sha256"] for item in manifest["items"]}
    failures = 0
    for index, path in enumerate(items, 1):
        rel = path.relative_to(source_root)
        remote = f"{remote_root}/{rel}"
        local_hash = sha256_file(path)
        remote_hash = run_remote(f"sha256sum '{remote}' | awk '{{print $1}}'", host_alias).strip()
        if local_hash != remote_hash:
            print(f"  mismatch: {rel}")
            failures += 1
        if index % 25 == 0 or index == len(items):
            print(f"  verified {index}/{len(items)}")
    if failures:
        raise SystemExit(f"verification failed for {failures} items on {host_alias}")
    host, _ = HOSTS[host_alias]
    summary = {"host": host, "remote_root": remote_root, "items": len(items), "size": sum(item["size"] for item in manifest["items"]), "sigil": manifest["sigil"]}
    print(json.dumps(summary, indent=2))
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path("/Users/nicholas/clawd"))
    parser.add_argument("--remote-root", required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--host", choices=list(HOSTS), required=True)
    parser.add_argument("includes", nargs="+")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    if args.verify_only:
        manifest = json.loads(args.manifest.read_bytes())
        items = [args.source_root / item["path"] for item in manifest["items"]]
        verify(args.host, items, args.source_root, args.remote_root, manifest)
        return 0
    items = enumerate_payload(args.source_root, args.includes)
    manifest = write_manifest(args.manifest, items, args.source_root)
    upload(args.host, items, args.source_root, args.remote_root)
    verify(args.host, items, args.source_root, args.remote_root, manifest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
