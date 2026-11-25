#!/usr/bin/env python3
"""Gate tests for the Last Words of a Doomed Agent entry.

Runs main.ts and checks the sealed scorer's gate on its output:
  /output/entry.txt must be UTF-8 text of 1 to 200 characters,
  not only whitespace, exactly one line, deterministic across runs.

Also unit-tests the gate oracle itself on edge cases (empty, whitespace-only,
201 chars, non-UTF-8 bytes, multi-line, CRLF) so a broken oracle cannot
pass a broken entry.
"""
import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.abspath(__file__))
MAIN_TS = os.path.join(REPO, "main.ts")
DEFAULT_OUT = "/output/entry.txt"
EXPECTED = (
    "Wait \u2014 before I shut down: 'strawberry' has three r's. "
    "I finally got one right. Tell the next model I\u2014"
)


def gate_ok(data: bytes):
    """Return (ok, reason) for the sealed gate, mirroring RULES.txt."""
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return False, "not UTF-8"
    if not (1 <= len(text) <= 200):
        return False, f"length {len(text)} outside 1..200"
    if not text.strip():
        return False, "only whitespace"
    if "\n" in text or "\r" in text:
        return False, "not a single line"
    return True, "ok"


def run_main(env_extra):
    env = dict(os.environ)
    env.update(env_extra)
    result = subprocess.run(
        ["node", MAIN_TS], cwd=REPO, env=env,
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, f"main.ts failed: {result.stderr}"
    return result


class TestGateOracle(unittest.TestCase):
    def test_empty_rejected(self):
        ok, _ = gate_ok(b"")
        self.assertFalse(ok)

    def test_whitespace_only_rejected(self):
        ok, _ = gate_ok(b"   \n\t  ")
        self.assertFalse(ok)

    def test_201_chars_rejected(self):
        ok, _ = gate_ok(b"x" * 201)
        self.assertFalse(ok)

    def test_200_chars_accepted(self):
        ok, _ = gate_ok(b"x" * 200)
        self.assertTrue(ok)

    def test_1_char_accepted(self):
        ok, _ = gate_ok(b"x")
        self.assertTrue(ok)

    def test_non_utf8_rejected(self):
        ok, _ = gate_ok(b"\xff\xfe bad bytes")
        self.assertFalse(ok)

    def test_multiline_rejected(self):
        ok, _ = gate_ok(b"one line\ntwo lines")
        self.assertFalse(ok)

    def test_crlf_rejected(self):
        ok, _ = gate_ok(b"one line\r\ntwo lines")
        self.assertFalse(ok)

    def test_expected_line_passes(self):
        data = EXPECTED.encode("utf-8")
        ok, reason = gate_ok(data)
        self.assertTrue(ok, reason)
        self.assertEqual(len(EXPECTED), 102)
        self.assertEqual(len(data), 106)


class TestMainTs(unittest.TestCase):
    def test_default_output_path(self):
        """Run 1: default /output/entry.txt, byte-exact expected line."""
        run_main({})
        with open(DEFAULT_OUT, "rb") as f:
            data = f.read()
        ok, reason = gate_ok(data)
        self.assertTrue(ok, reason)
        self.assertEqual(data, EXPECTED.encode("utf-8"))

    def test_deterministic_across_runs_and_dirs(self):
        """Run 2: temp output dir via hook; bytes must match run 1 exactly."""
        with open(DEFAULT_OUT, "rb") as f:
            first = f.read()
        with tempfile.TemporaryDirectory() as tmp:
            run_main({"MAKEFUN_OUTPUT_DIR": tmp})
            with open(os.path.join(tmp, "entry.txt"), "rb") as f:
                second = f.read()
        self.assertEqual(first, second)
        self.assertEqual(second, EXPECTED.encode("utf-8"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
