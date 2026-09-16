import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "text_stats.py"
SAMPLE = ROOT / "sample.txt"


class TextStatsTests(unittest.TestCase):
    def test_count_text_stats_function(self):
        from src.text_stats import count_text_stats

        text = "alpha beta\ngamma\n"
        self.assertEqual(
            count_text_stats(text),
            {"lines": 2, "words": 3, "characters": 17},
        )

    def test_cli_outputs_json_for_sample_file(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(SAMPLE)],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(ROOT),
        )

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            payload,
            {"lines": 5, "words": 55, "characters": 281},
        )

    def test_cli_requires_file_argument(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(ROOT),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage:", result.stderr)


if __name__ == "__main__":
    unittest.main()
