import concurrent.futures
import http.client
import tempfile
import threading
import unittest
from pathlib import Path
import server

class CounterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        server.DB = str(Path(self.tmp.name) / 'test.sqlite3')
        server.SECRET = 'a-test-password-with-more-than-20-characters'
        server.initialize()
        self.http = server.ThreadingHTTPServer(('127.0.0.1', 0), server.Handler)
        self.thread = threading.Thread(target=self.http.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.http.shutdown(); self.http.server_close(); self.thread.join()
        self.tmp.cleanup()

    def request(self, method, path, headers=None):
        conn = http.client.HTTPConnection('127.0.0.1', self.http.server_port)
        conn.request(method, path, headers=headers or {})
        response = conn.getresponse(); status = response.status; body = response.read(); conn.close()
        return status, body

    def test_private_stats_and_origin(self):
        self.assertEqual(self.request('GET', '/stats')[0], 401)
        self.assertEqual(self.request('GET', '/stats', {'Authorization': 'Bearer wrong'})[0], 401)
        self.assertEqual(self.request('POST', '/view', {'Origin': 'https://unrelated.example'})[0], 403)
        self.assertEqual(server.stats()['total'], 0)
        self.assertEqual(self.request('POST', '/view', {'Origin': 'https://myopiabridge.org'})[0], 204)
        status, body = self.request('GET', '/stats', {'Authorization': 'Bearer ' + server.SECRET})
        self.assertEqual(status, 200); self.assertIn(b'"total": 1', body)

    def test_concurrent_updates_and_persistence(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
            list(pool.map(lambda _: server.increment(), range(100)))
        server.initialize()  # Restart initialization must not reset saved totals.
        self.assertEqual(server.stats()['total'], 100)

if __name__ == '__main__':
    unittest.main()
