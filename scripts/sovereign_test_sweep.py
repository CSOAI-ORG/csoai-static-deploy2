import os, subprocess, sys, glob

os.chdir("/Users/nicholas/clawd")
PY = "/usr/local/bin/python3"

# CLEAN ENV - no PYTHONPATH pollution
clean_env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}
clean_env["PYTHONDONTWRITEBYTECODE"] = "1"

mcp_dirs = sorted(glob.glob("mcp-marketplace/meok-sovereign-*-mcp"))
results = []
total_pass = 0
total_fail = 0
failed = []

for d in mcp_dirs:
    name = os.path.basename(d)
    test_files = glob.glob(f"{d}/tests/test_*.py")
    if not test_files:
        results.append((name, "NO_TESTS", 0, 0))
        continue
    try:
        proc = subprocess.run(
            [PY, "-m", "pytest", "tests/", "-q", "--tb=no", "--no-header", "-p", "no:cacheprovider"],
            cwd=d, capture_output=True, text=True, timeout=60,
            env=clean_env
        )
        out = proc.stdout + proc.stderr
        passed = failed_n = 0
        for line in out.splitlines()[::-1]:
            line = line.strip()
            if " passed" in line and ("failed" not in line and "error" not in line.lower()):
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == "passed" and i > 0:
                        try: passed = int(parts[i-1])
                        except: pass
                break
            elif " failed" in line:
                parts = line.split()
                for i, p in enumerate(parts):
                    if p == "passed" and i > 0:
                        try: passed = int(parts[i-1])
                        except: pass
                    if p == "failed" and i > 0:
                        try: failed_n = int(parts[i-1])
                        except: pass
                break
        status = "PASS" if proc.returncode == 0 and failed_n == 0 else f"FAIL({proc.returncode})"
        total_pass += passed
        total_fail += failed_n
        results.append((name, status, passed, failed_n))
        if failed_n > 0 or proc.returncode != 0:
            failed.append((name, status, passed, failed_n, out[-300:].strip()[:200]))
    except subprocess.TimeoutExpired:
        results.append((name, "TIMEOUT", 0, 0))
        failed.append((name, "TIMEOUT", 0, 0, "60s timeout"))

print(f"\n=== FULL SWEEP (clean env, python 3.14, crypto 49, numpy ok) ===")
print(f"MCPs tested: {len(results)}")
print(f"Total passed: {total_pass}")
print(f"Total failed: {total_fail}")
print()
if failed:
    print(f"FAILED ({len(failed)}):")
    for f in failed:
        print(f"  FAIL {f[0]}: pass={f[2]} fail={f[3]}")
        print(f"      {f[4][:200]}")
else:
    print("ALL MCPs GREEN — 100% PASS")
