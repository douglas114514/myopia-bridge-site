// Set this to the public HTTPS address of your counter server, without a trailing slash.
(() => {
  const counterURL = 'REPLACE_WITH_YOUR_COUNTER_HTTPS_URL';
  if (!counterURL.startsWith('https://')) return;
  if (!['myopiabridge.org', 'www.myopiabridge.org'].includes(location.hostname)) return;
  // One request per document load, including refreshes. Hash navigation isn't a new load.
  fetch(counterURL + '/view', {method: 'POST', credentials: 'omit', keepalive: true}).catch(() => {});
})();
