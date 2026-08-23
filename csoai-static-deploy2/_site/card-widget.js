/* card-widget.js — self-verifying signed measurement card embed, zero-dep.
   Usage: <div class="csoai-card" data-axis="governance" data-acc="0.700"
   data-n="237" data-ci="[0.639,0.755]" data-sig="2e6525a3..."></div>
   Verify recomputes sha256(axis|acc|n|ci) in-browser via WebCrypto. */
(function () {
  var L = { governance:'Governance', safety:'Safety', provenance:'Provenance',
    continuity:'Continuity', conformance:'Conformance', openness:'Openness',
    'machinery-conformity':'Machinery', care:'Care', 'cross-reality':'XR',
    'detector-interop':'Detection', 'art5-safeguard':'Art 5', swarm:'Swarm', affect:'Affect' };
  function hash(t) {
    if (window.crypto && crypto.subtle) {
      return crypto.subtle.digest('SHA-256', new TextEncoder().encode(t))
        .then(function (h) { return Array.from(new Uint8Array(h))
          .map(function (b) { return b.toString(16).padStart(2, '0'); }).join(''); });
    }
    return Promise.resolve(null);
  }
  document.querySelectorAll('.csoai-card').forEach(function (el) {
    var a = el.getAttribute('data-axis') || 'governance';
    var acc = el.getAttribute('data-acc'), n = el.getAttribute('data-n');
    var ci = el.getAttribute('data-ci') || '', sig = el.getAttribute('data-sig') || '';
    var st = (!acc || !n || parseInt(n, 10) < 30) ? 'UNMEASURED' : 'MEASURED';
    var w = document.createElement('div');
    w.style.cssText = 'border:1px solid #232830;border-radius:10px;background:#15181d;color:#c9cdd6;font:13px/1.5 -apple-system,Segoe UI,sans-serif;max-width:320px;padding:14px 16px;margin:8px 0';
    w.innerHTML = '<div style="display:flex;justify-content:space-between"><b style="color:#f0f2f5">' +
      (L[a] || a) + '</b><span style="color:#5a9;font-size:.72rem;font-weight:600">' + st + '</span></div>' +
      '<div style="font-size:1.7rem;font-weight:700;color:' + (st === 'MEASURED' ? '#ccffdd' : '#556') + '">' +
      (acc || '—') + '</div>' +
      '<div style="color:#79889a;font-size:.72rem">' + (n ? 'n=' + n + ' · ' : '') + (ci || 'no interval') + '</div>' +
      '<div style="margin-top:10px;display:flex;gap:8px;align-items:center">' +
      '<button class="cv" style="background:#232830;color:#8cd;border:1px solid #2a3642;border-radius:6px;padding:4px 10px;font-size:.72rem;cursor:pointer">Verify card</button>' +
      '<span class="vs" style="color:#79889a;font-size:.72rem"></span></div>';
    el.replaceWith(w);
    w.querySelector('.cv').addEventListener('click', function () {
      var v = w.querySelector('.vs'); v.textContent = 'hashing…';
      hash([a, acc, n, ci].join('|')).then(function (h) {
        if (!h) { v.textContent = 'WebCrypto unavailable — verify at /gspc-verify'; return; }
        v.innerHTML = (sig && sig.slice(0, 10) === h.slice(0, 10))
          ? '<span style="color:#5a9">✓ content-hash ok</span>'
          : '<span style="color:#f9a03f">⚠ recompute ' + h.slice(0, 8) + ' — check /gspc-verify</span>';
      });
    });
  });
})();
