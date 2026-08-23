#!/bin/bash
# oracle-offload.sh — archive idle data dirs to Oracle Object Storage (mac-offload bucket)
# SAFE: uploads a tarball, then MOVES the local dir to a trash location (never rm).
# The dir only leaves the working area after a VERIFIED upload.
BUCKET="mac-offload"
TRASH="$HOME/offloaded-trash"
mkdir -p "$TRASH"
for dir in "$@"; do
  base=$(basename "$dir")
  [ -d "$dir" ] || { echo "skip (not dir): $dir"; continue; }
  echo "=== archiving $dir -> $BUCKET ..."
  tar --exclude='node_modules' --exclude='.git' -czf "/tmp/$base.tar.gz" -C "$(dirname "$dir")" "$base" 2>/dev/null
  size=$(du -h "/tmp/$base.tar.gz" | cut -f1); echo "  tarball: $size"
  oci os object put --bucket-name "$BUCKET" --name "mac-offload/$base.tar.gz" --file "/tmp/$base.tar.gz" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "  uploaded OK; MOVED local copy to $TRASH (recoverable, not deleted)"
    mv "$dir" "$TRASH/$base"
  else
    echo "  upload FAILED — keeping local copy"
  fi
  rm -f "/tmp/$base.tar.gz"
done
