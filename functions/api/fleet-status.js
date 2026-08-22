// Cloudflare Pages Function — public, sanitized fleet map
// GET /api/fleet-status
//
// Language lock: public labels only. Internal pod names, endpoints, IPs,
// volume ids and keys are NEVER published here or anywhere on the site.
// The map is a static snapshot of a read-only inventory; it is honest about
// status and about the fact it is a snapshot (as_of).
//
// Policy flags mirror the fleet do-not-touch rules:
//   keep-flying        — running, do not stop
//   billed, light-touch — running and billed, do not hammer
//   owner-gated start  — paused, only the CEO starts it

const FLEET = {
  as_of: '2026-08-21T05:30Z',
  note: 'Public fleet map — sanitized. Internal names, endpoints and keys are never published. Verified 21 Aug: RunPod API edge-blocked (403), mine pod SSH timed out — status below is last-known-truth + owner flags, not a live poll.',
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
      status: 'running',
      policy: 'billed, light touch',
    },
    {
      role: 'merge / weld worker',
      gpu: 'A100',
      status: 'paused',
      policy: 'owner-gated start',
    },
    {
      role: 'mine pod (idle)',
      gpu: 'A100',
      status: 'idle-gpu-0%',
      policy: 'owner-decides-stop-when-idle (still $1.39/hr)',
    },
  ],
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
