# MyopiaBridge custom page-view counter

This program does not use Google Analytics or an analytics subscription. It needs a Python server with persistent disk storage. GitHub Pages cannot run server.py. Your main website stays on GitHub Pages.

## What it counts

Each successful tracking request adds one view: a page load or refresh, across visitors. Moving between your site's hash sections doesn't count again. This is page views, not unique people. No visitor IDs, IP addresses, cookies, or full URLs are stored by this program. Bots, repeated refreshes, and forged requests can inflate totals; blockers and failed requests can reduce them. Report it as recorded page views, not verified people reached.

## Run locally to try it

Requires Python 3.9 or later; no extra packages.

In a terminal, enter the counter directory, then set a unique password (never commit it to GitHub):

```bash
export COUNTER_PASSWORD='replace-with-a-unique-password-at-least-20-characters'
export COUNTER_ORIGINS='http://localhost:8000,https://myopiabridge.org,https://www.myopiabridge.org'
python3 server.py
```

Open http://localhost:8080/admin and enter the password. In another terminal, create a test view:

```bash
curl -X POST -H 'Origin: http://localhost:8000' http://localhost:8080/view
```

Press Refresh on the admin page. Restarting the server keeps the total as long as its database file remains.

## Connect your live site

1. Run server.py on a Python-capable host with a persistent disk, behind HTTPS. Hosting a server is separate from buying a domain. Configure an HTTPS reverse proxy to forward to 127.0.0.1:8080. If your platform requires binding to all interfaces, set COUNTER_HOST=0.0.0.0 and use its managed HTTPS ingress.
2. Set COUNTER_PASSWORD as a private environment secret with at least 20 characters. Set COUNTER_DB to a writable file on the persistent disk (for example /data/myopiabridge.sqlite3). Do not put either a password or a database into your public repository. Back up the database; replacing a host without retaining it resets the total.
3. Apply rate limits to /view and /stats at your hosting proxy, especially repeated failed authentication. The public counting endpoint isn't proof that a request is human. Origin validation stops ordinary cross-site browser submissions but isn't bot protection.
4. In counter/tracker.js, replace REPLACE_WITH_YOUR_COUNTER_HTTPS_URL with your backend's HTTPS address. The tracker contains no password.
5. Upload the included tracker.js into the counter folder in your GitHub repository. Use the included updated index.html, which loads it once, or add this immediately before </head>:

```html
<script defer src="counter/tracker.js"></script>
```

6. Commit your changes. Visit your live site and then the backend's /admin address. Enter your password and verify the total increases once per refresh. No number appears publicly on your main website. The admin page HTML is public, but its data endpoint requires the password; keep HTTPS enabled.

The program is ready to configure, but this download does not deploy a backend or modify your live GitHub repository. It cannot recover past views. Keep the tracking URL placeholder until you have a working HTTPS backend.
