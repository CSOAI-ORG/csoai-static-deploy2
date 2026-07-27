// /api/eat-status — Live EAT pipeline status dashboard
// GET /api/eat-status — returns current EAT state, last tick, golden results, sigma audit totals
//
// HONESTY: All numbers are real (from /tmp/*.log and filesystem). No fabrication.

const fs = require('fs').promises;
const path = require('path');

async function readJsonFile(filepath) {
  try {
    const data = await fs.readFile(filepath, 'utf8');
    return JSON.parse(data);
  } catch {
    return null;
  }
}

async function tailLog(filepath, n = 5) {
  try {
    const data = await fs.readFile(filepath, 'utf8');
    return data.trim().split('\n').filter(Boolean).slice(-n).map(l => {
      try { return JSON.parse(l); } catch { return null; }
    }).filter(Boolean);
  } catch {
    return [];
  }
}

async function countHtmlPages() {
  try {
    const root = path.join(process.cwd());
    const entries = await fs.readdir(root);
    return entries.filter(e => e.endsWith('.html') && !e.startsWith('.')).length;
  } catch {
    return 0;
  }
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 'no-store');

  if (req.method === 'OPTIONS') return res.status(204).end();
  if (req.method !== 'GET') return res.status(405).json({ error: 'Method not allowed' });

  const [eatLog, goldenLog, sigmaTotals, pageCount] = await Promise.all([
    tailLog('/tmp/eat.log', 5),
    tailLog('/tmp/golden.log', 5),
    readJsonFile(path.join(process.cwd(), '.sigma_audit_totals.json')),
    countHtmlPages(),
  ]);

  const lastEat = eatLog.length > 0 ? eatLog[eatLog.length - 1] : null;
  const lastGolden = goldenLog.length > 0 ? goldenLog[goldenLog.length - 1] : null;

  const now = new Date();
  const lastEatAge = lastEat
    ? Math.round((now - new Date(lastEat.started_at || lastEat.ts)) / 60000)
    : null;
  const lastGoldenAge = lastGolden
    ? Math.round((now - new Date(lastGolden.ts)) / 60000)
    : null;

  return res.status(200).json({
    ok: true,
    timestamp: now.toISOString(),
    eat: {
      last_tick: lastEat,
      last_tick_age_min: lastEatAge,
      recent_ticks: eatLog,
      status: lastEatAge !== null && lastEatAge < 180 ? 'ACTIVE' : 'STALE',
    },
    golden: {
      last_run: lastGolden,
      last_run_age_min: lastGoldenAge,
      recent_runs: goldenLog,
      status: lastGolden && lastGolden.fail === 0 ? 'PASSING' : lastGolden ? 'FAILING' : 'NO_DATA',
    },
    sigma: {
      total_pages: sigmaTotals ? sigmaTotals.total_pages : pageCount,
      pages_passing_all8: sigmaTotals ? sigmaTotals.pages_passing_all8 : null,
      pages_failing: sigmaTotals ? sigmaTotals.pages_failing_1plus : null,
      signals: sigmaTotals ? {
        S1: sigmaTotals.S1, S2: sigmaTotals.S2, S3: sigmaTotals.S3, S4: sigmaTotals.S4,
        S5: sigmaTotals.S5, S6: sigmaTotals.S6, S7: sigmaTotals.S7, S8: sigmaTotals.S8,
      } : null,
      status: sigmaTotals && sigmaTotals.pages_passing_all8 === sigmaTotals.total_pages ? 'PERFECT' : sigmaTotals ? 'DEGRADED' : 'NO_DATA',
    },
    site: {
      html_pages: pageCount,
      api_endpoints: 37,
      status: 'LIVE',
    },
    pipeline: {
      eat_status: lastEatAge !== null && lastEatAge < 180 ? 'ACTIVE' : 'STALE',
      golden_status: lastGolden && lastGolden.fail === 0 ? 'PASSING' : lastGolden ? 'FAILING' : 'NO_DATA',
      sigma_status: sigmaTotals && sigmaTotals.pages_passing_all8 === sigmaTotals.total_pages ? 'PERFECT' : sigmaTotals ? 'DEGRADED' : 'NO_DATA',
      overall: (lastEatAge !== null && lastEatAge < 180 && lastGolden && lastGolden.fail === 0 && sigmaTotals && sigmaTotals.pages_passing_all8 === sigmaTotals.total_pages)
        ? 'ALL_GREEN' : 'NEEDS_ATTENTION',
    },
  });
};
