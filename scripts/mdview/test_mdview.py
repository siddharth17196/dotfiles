"""Run with: python3 -m unittest discover -s scripts/mdview -v"""

import json
import os
from pathlib import Path
import subprocess
import sys
import socket
import tempfile
import threading
import time
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import mdview


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        (self.root / ".git").mkdir()
        (self.root / "docs").mkdir()
        self.plan = self.root / "docs" / "PLAN #1.md"
        self.plan.write_text("# Plan\n\n[Review](../REVIEW.md#review)\n\n![Image](../image.svg)\n", encoding="utf-8")
        self.review = self.root / "REVIEW.md"
        self.review.write_text("# Review\n", encoding="utf-8")
        (self.root / "image.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        self.server = mdview.Server(0)
        self.port = self.server.server_port
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def call(self, route, data=None, headers=None):
        req = Request(f"http://127.0.0.1:{self.port}{route}",
                      data=json.dumps(data).encode() if data is not None else None,
                      headers=headers or ({"Content-Type": "application/json"} if data is not None else {}))
        try:
            return urlopen(req, timeout=3)
        except HTTPError as error:
            error.close()
            raise

    def open_plan(self):
        with self.call("/api/open", {"paths": [str(self.plan)]}) as response:
            return json.load(response)["files"][0]["url"]

    def test_cross_session_registration_and_deduplication(self):
        for path in (self.plan, self.review, self.plan):
            result = subprocess.run([sys.executable, str(mdview.HERE / "mdview.py"),
                                     "--port", str(self.port), "--no-browser", str(path)],
                                    capture_output=True, text=True, timeout=5)
            self.assertEqual(result.returncode, 0, result.stderr)
        with self.call("/api/state") as response:
            state = json.load(response)
        self.assertEqual(state["app"], mdview.APP)
        self.assertEqual(len(state["files"]), 2)
        self.assertIn("PLAN%20%231.md", state["files"][0]["url"])

    def test_relative_markdown_and_images(self):
        url = self.open_plan()
        with self.call(url + "?render=1") as response:
            rendered = json.load(response)["html"]
        self.assertIn('href="../REVIEW.md#review"', rendered)
        self.assertIn('src="../image.svg"', rendered)
        mount = url.split("/")[2]
        with self.call("/api/open-link", {"url": f"/files/{mount}/REVIEW.md#review"}) as response:
            result = json.load(response)
        self.assertEqual(len(result["files"]), 2)
        self.assertTrue(result["url"].endswith("/REVIEW.md"))
        with self.call(f"/files/{mount}/image.svg") as response:
            self.assertIn("sandbox", response.headers["Content-Security-Policy"])
            self.assertIn(b"<svg", response.read())

    def test_changed_file_atomic_save_and_delete_recovery(self):
        url = self.open_plan()
        with self.call(url + "?render=1") as response:
            before = json.load(response)
        with self.call(url + "?render=1&revision=" + before["revision"]) as response:
            self.assertEqual(json.load(response), {"revision": before["revision"]})
        original_time = self.plan.stat().st_mtime_ns
        replacement = self.plan.with_suffix(".tmp")
        replacement.write_text("# Changed\n", encoding="utf-8")
        os.utime(replacement, ns=(original_time, original_time))
        replacement.replace(self.plan)
        with self.call(url + "?render=1") as response:
            after = json.load(response)
        self.assertNotEqual(before["revision"], after["revision"])
        self.assertIn("Changed", after["html"])
        self.plan.unlink()
        with self.assertRaises(HTTPError) as error:
            self.call(url + "?render=1")
        self.assertEqual(error.exception.code, 404)
        self.plan.write_text("# Restored\n")
        with self.call(url + "?render=1") as response:
            self.assertIn("Restored", json.load(response)["html"])

    def test_multiple_roots_and_explicit_root(self):
        other = Path(self.temp.name) / "standalone"
        other.mkdir()
        note = other / "notes.markdown"
        note.write_text("Hello")
        self.open_plan()
        with self.call("/api/open", {"paths": [str(note)], "root": self.temp.name}) as response:
            files = json.load(response)["files"]
        self.assertEqual(len(files), 2)
        self.assertNotEqual(files[0]["url"].split("/")[2], files[1]["url"].split("/")[2])
        self.assertIn("/standalone/notes.markdown", files[1]["url"])

    def test_traversal_symlinks_and_non_assets_are_rejected(self):
        url = self.open_plan()
        mount = url.split("/")[2]
        secret = Path(self.temp.name) / "secret.md"
        secret.write_text("outside")
        (self.root / "escape.md").symlink_to(secret)
        (self.root / ".env").write_text("private")
        for route, code in ((f"/files/{mount}/%2e%2e/secret.md", 404),
                            (f"/files/{mount}/escape.md", 404),
                            (f"/files/{mount}/.env", 403)):
            with self.assertRaises(HTTPError) as error:
                self.call(route)
            self.assertEqual(error.exception.code, code)

    def test_origin_host_and_malformed_requests(self):
        for headers in ({"Content-Type": "application/json", "Origin": "https://example.com"},
                        {"Content-Type": "application/json", "Host": "evil.example"},
                        {"Content-Type": "text/plain"}):
            with self.assertRaises(HTTPError) as error:
                self.call("/api/open", {"paths": [str(self.plan)]}, headers)
            self.assertEqual(error.exception.code, 403)
        for route, data in (("/api/open-link", {"url": 10}), ("/api/open", {"paths": "bad"}),
                            ("/api/open", {"paths": [str(self.plan)], "root": str(self.plan)})):
            with self.assertRaises(HTTPError) as error:
                self.call(route, data)
            self.assertEqual(error.exception.code, 400)

    def test_close_and_batch_validation(self):
        url = self.open_plan()
        with self.assertRaises(HTTPError):
            self.call("/api/open", {"paths": [str(self.review), str(self.root / "missing.md")]})
        with self.call("/api/state") as response:
            self.assertEqual(len(json.load(response)["files"]), 1)
        with self.call("/api/close", {"url": url}) as response:
            self.assertTrue(json.load(response)["ok"])
        with self.call("/api/state") as response:
            self.assertEqual(json.load(response)["files"], [])

    def test_formatting_and_disabled_raw_html(self):
        text = "# Hello\n\n# Hello\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n~~gone~~\n\n- [x] Done\n- [ ] Todo\n\n```python\nprint(1)\n```\n\n<script>alert(1)</script>\n\n[Bad](javascript:alert(1))\n"
        output = mdview.render_markdown(self.server.workspace.parser, text)
        for part in ('id="hello"', 'id="hello-1"', "<table>", "<s>gone</s>",
                     'type="checkbox" disabled checked', 'class="language-python"'):
            self.assertIn(part, output)
        self.assertNotIn("<script>", output)
        self.assertNotIn('href="javascript:', output)

    def test_background_start_reuse_and_stop(self):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        command = [sys.executable, str(mdview.HERE / "mdview.py"), "--port", str(port)]
        environment = dict(os.environ, TMPDIR=self.temp.name)
        try:
            for path in (self.plan, self.review):
                result = subprocess.run(command + ["--no-browser", str(path)], env=environment,
                                        capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(mdview.request(port, "/api/state")["files"]), 2)
        finally:
            subprocess.run(command + ["--stop"], env=environment, capture_output=True, timeout=5)
        for _ in range(40):
            try:
                mdview.request(port, "/api/state")
            except OSError:
                break
            time.sleep(0.05)
        else:
            self.fail("Background server did not stop")


class FrontMatterTests(unittest.TestCase):
    def setUp(self):
        self.parser = mdview.Workspace().parser

    def render(self, text):
        return mdview.render_markdown(self.parser, text)

    def test_skill_metadata_is_a_table_followed_by_the_document(self):
        output = self.render('---\nname: handoff\ndescription: Compact the current conversation.\ndisable-model-invocation: true\nargument-hint: "What will the next session be used for?"\n---\n\n# Handoff\n\nNormal document.\n')
        self.assertIn('<table class="front-matter"', output)
        self.assertIn('<th scope="row">name</th><td>handoff</td>', output)
        self.assertIn('<td>What will the next session be used for?</td>', output)
        self.assertIn('<h1 id="handoff">Handoff</h1>', output)
        self.assertNotIn("<hr", output)
        self.assertNotIn("<h2", output)

    def test_quoted_values_and_html_are_escaped(self):
        output = self.render('---\nname: "<script>alert(1)</script>"\nlabel: \'It\'\'s a label\'\nurl: https://example.com/a:b\nempty:\n---\n')
        self.assertNotIn('<script>', output)
        self.assertIn('&lt;script&gt;', output)
        self.assertIn('It&#x27;s a label', output)
        self.assertIn('https://example.com/a:b', output)
        self.assertIn('<th scope="row">empty</th><td></td>', output)

    def test_complex_metadata_is_preserved_as_text(self):
        for metadata in ('name: handoff\ntags:\n  - work\n',
                         'description: |\n  Multiple lines\n',
                         'name: [one, two]\n',
                         'name: "unterminated\n',
                         'name: first\nname: second\n'):
            with self.subTest(metadata=metadata):
                output = self.render('---\n' + metadata + '---\n\n# Body\n')
                self.assertIn('<pre class="front-matter"><code>---', output)
                self.assertNotIn('<table', output)
                self.assertIn('<h1 id="body">Body</h1>', output)

    def test_normal_separators_and_unclosed_blocks_stay_markdown(self):
        for text in ('# Document\n\n---\nname: handoff\n---\n',
                     '---\nOrdinary heading\n---\n',
                     '---\nname: handoff\n',
                     '\n---\nname: handoff\n---\n',
                     '```yaml\n---\nname: handoff\n---\n```\n'):
            with self.subTest(text=text):
                self.assertNotIn('class="front-matter"', self.render(text))


if __name__ == "__main__":
    unittest.main()
