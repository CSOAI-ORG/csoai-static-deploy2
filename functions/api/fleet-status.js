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
  as_of: '2026-08-21T06:20Z',
  // Public status transparency (report item e): a trust vendor must publish a
  // stated availability SLO + honest status. The SLO is a commitment; the live
  // availability is the MEASURED number (from /api/health probes) — never a claim.
  status: 'operational',
  slo: '99.9% monthly availability (verification public-good surface + signed-card issuance)',
  availability_measured: 'via /api/health (live probes, 5 min) — recomputed, never asserted',
  availability_url: 'https://csoai-gspc.pages.dev/api/health',
  note: 'Public fleet map — sanitized. Internal names, endpoints and keys are never published. Verified 21 Aug via runpodctl: 3 RUNNING pods (~$40/day). Mine-pod A100 is IDLE (GPU 0%) and still billed $1.39/hr — owner-decides stop-when-idle.',
  workers: [
    {
      role: 'arena measurement worker',
      gpu: 'RTX 3090',
      status: 'running',
      policy: 'keep-flying',
    },
    {
      role: 'heavy measurement worker (idle)',
      gpu: 'A100',
      status: 'idle-gpu-0%',
      policy: 'owner-decides-stop-when-idle ($1.39/hr)',
    },
    {
      role: 'repull worker',
      gpu: 'RTX 3090',
      status: 'running',
      policy: 'keep-flying',
    },
    {
      role: 'cpu sink',
      gpu: 'cpu',
      status: 'running',
      policy: 'keep-flying (cheap)',
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
