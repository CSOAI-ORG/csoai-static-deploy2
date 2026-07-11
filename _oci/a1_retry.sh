#!/usr/bin/env bash
VP="/private/tmp/claude-501/-Users-nicholas/aab64416-7b82-4017-a53b-cd1305864906/scratchpad/ocienv/bin/python"
OUT=$("$VP" ~/clawd/_oci/launch_free_vm.py 2>&1)
echo "$(date) $OUT" >> ~/clawd/_oci/a1_retry.log
if echo "$OUT" | grep -qE 'LAUNCHED|ALREADY-EXISTS'; then
  crontab -l 2>/dev/null | grep -v a1_retry.sh | crontab -   # got it -> stop retrying
  echo "$(date) A1 SECURED, cron removed" >> ~/clawd/_oci/a1_retry.log
fi
