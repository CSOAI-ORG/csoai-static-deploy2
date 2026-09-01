/**
 * P0 OWNER 2026-09-01 — one public website.
 * Pages Functions run ahead of _redirects on csoai-site, so the catch-all
 * in _redirects never fired. This middleware 308s every path to councilof.ai
 * except /.well-known/* (did:web:csoai.org trust root).
 */
export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.pathname === '/.well-known' || url.pathname.startsWith('/.well-known/')) {
    return context.next();
  }
  const dest = `https://councilof.ai${url.pathname}${url.search}`;
  return Response.redirect(dest, 308);
}
