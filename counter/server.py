"""MyopiaBridge counter. Python standard library only; run behind HTTPS."""
import hmac
import json
import os
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

DB = os.environ.get('COUNTER_DB', 'counter.sqlite3')
SECRET = os.environ.get('COUNTER_PASSWORD', '')
ORIGINS = set(os.environ.get('COUNTER_ORIGINS', 'https://myopiabridge.org,https://www.myopiabridge.org').split(','))

def initialize():
    with sqlite3.connect(DB, timeout=30) as db:
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('CREATE TABLE IF NOT EXISTS views (day TEXT PRIMARY KEY, total INTEGER NOT NULL)')

def increment():
    day = datetime.now(timezone.utc).date().isoformat()
    with sqlite3.connect(DB, timeout=30) as db:
        db.execute('INSERT INTO views VALUES (?, 1) ON CONFLICT(day) DO UPDATE SET total=total+1', (day,))

def stats():
    with sqlite3.connect(DB, timeout=30) as db:
        rows = db.execute('SELECT day, total FROM views ORDER BY day DESC').fetchall()
    return {'total': sum(n for _, n in rows), 'daily': [{'day': d, 'views': n} for d, n in rows], 'timezone': 'UTC'}

class Handler(BaseHTTPRequestHandler):
    # Avoid storing request headers, IP addresses or passwords in access logs.
    def log_message(self, *args):
        pass

    def respond(self, status, data=None, content_type='application/json'):
        body = b'' if data is None else (json.dumps(data).encode() if content_type == 'application/json' else data)
        self.send_response(status)
        origin = self.headers.get('Origin', '')
        if origin in ORIGINS:
            self.send_header('Access-Control-Allow-Origin', origin)
            self.send_header('Vary', 'Origin')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != '/view':
            return self.respond(404, {'error': 'Not found'})
        if self.headers.get('Origin', '') not in ORIGINS:
            return self.respond(403, {'error': 'Origin not allowed'})
        # The tracking request has no body. Close on unexpected payloads.
        if self.headers.get('Transfer-Encoding') or self.headers.get('Content-Length', '0') != '0':
            self.close_connection = True
            return self.respond(400, {'error': 'Empty request required'})
        try:
            increment()
            self.respond(204)
        except sqlite3.Error:
            self.respond(503, {'error': 'Storage unavailable'})

    def do_GET(self):
        if self.path in ('/', '/admin'):
            return self.respond(200, Path(__file__).with_name('admin.html').read_bytes(), 'text/html; charset=utf-8')
        if self.path == '/stats':
            expected = 'Bearer ' + SECRET
            if not SECRET or not hmac.compare_digest(self.headers.get('Authorization', '').encode(), expected.encode()):
                return self.respond(401, {'error': 'Incorrect password'})
            try:
                return self.respond(200, stats())
            except sqlite3.Error:
                return self.respond(503, {'error': 'Storage unavailable'})
        self.respond(404, {'error': 'Not found'})

if __name__ == '__main__':
    if len(SECRET) < 20:
        raise SystemExit('Set COUNTER_PASSWORD to a unique password of at least 20 characters.')
    initialize()
    ThreadingHTTPServer((os.environ.get('COUNTER_HOST', '127.0.0.1'), int(os.environ.get('PORT', '8080'))), Handler).serve_forever()
