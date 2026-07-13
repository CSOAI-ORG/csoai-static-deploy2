module.exports = async function handler(req, res) {
res.setHeader('Access-Control-Allow-Origin', '*');
res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS, GET');
res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

if (req.method === 'GET') {
return res.status(200).json({
endpoint: 'debug',
deployed_at: '2026-07-07',
note: 'Inspect deployed signup.js by triggering an OPTIONS request and looking at logs'
});
}

if (req.method === 'OPTIONS') return res.status(204).end();

let body = req.body;
if (typeof body === 'string') {
try { body = JSON.parse(body); } catch (e) { return res.status(400).json({ error: 'Invalid JSON' }); }
}
if (!body || typeof body !== 'object') body = {};

// Echo what we received
return res.status(200).json({
received_keys: Object.keys(body),
email: body.email,
email_type: typeof body.email,
email_stringified: String(body.email || ''),
email_after_trim_lowercase: String(body.email || '').trim().toLowerCase(),
email_includes_at: String(body.email || '').trim().toLowerCase().includes('@'),
});
};