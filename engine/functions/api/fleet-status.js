// Cloudflare Pages Function — public, sanitized fleet map
// GET /api/fleet-status
//
// Language lock: public labels only. Internal pod names, endpoints, IPs,
// volume ids and keys are NEVER published here or anywhere on the site.
// The map is a static snapshot of a read-only inventory; it is honest about
// status and about the fact it is a snapshot (as_of).
//
// Policy flags (1 Sep 2026 lock):
//   keep-flying        — RTX 3090 KEEP only
//   dark / do-not-start — all A100 pods; do not start
// FLEET-B 40 sits UNMEASURED. mill stays dead. Never MEASURED stamp.

const FLEET = {
  as_of: '2026-09-01T02:30Z',
  note: 'Public fleet map — sanitized. Internal names, endpoints and keys are never published. 1 Sep lock: only RTX 3090 KEEP; A100 dark; FLEET-B 40 sits UNMEASURED; mill stays dead. Snapshot + owner flags, not a live RunPod poll.',
  workers: [
    {
      role: 'arena measurement worker',
      gpu: 'RTX 3090',
      status: 'running',
      policy: 'keep-flying',
    },
    {
      role: 'heavy measurement worker',
      gpu: 'A100',
      status: 'dark',
      policy: 'do-not-start',
    },
    {
      role: 'merge / weld worker',
      gpu: 'A100',
      status: 'dark',
      policy: 'do-not-start',
    },
    {
      role: 'mine pod',
      gpu: 'A100',
      status: 'dark',
      policy: 'do-not-start',
    },
  ],
  fleet_b: {
    n_locked: 40,
    status_all: 'UNMEASURED',
    stranger_get: 'https://councilof.ai/fleet/FLEET-B.lock.json',
    sits: true,
    mill: 'dead',
  },
  substrate: ['Cloudflare Pages', 'Oracle always-free micros', 'Kaggle'],
  measurement_language: 'signed · re-attested · independent — never certification',
};

export async function onRequestGet() {
  return Response.json(FLEET, {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=300',
      'Access-Control-Allow-Origin': '*',
    },
  });
}
