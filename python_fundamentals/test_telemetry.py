import unittest
import tempfile
import json
from pathlib import Path

from solution import process_telemetry


class TestTelemetry(unittest.TestCase):

    def setUp(self):
        # Each test gets its own temporary directory.
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

        self.root = Path(self.tmp.name)
        self.config = self.root / "config.json"
        self.telemetry = self.root / "telemetry.csv"
        self.output = self.root / "summary.json"

        self.config.write_text('{"gpu_threshold": 80}')

        self.telemetry.write_text(
            "agent_id,gpu_utilization\n"
            "agent-a,65.5\n"
            "agent-b,92.0\n"
            "agent-c,invalid\n"
            "agent-d,85.0\n"
            "agent-e,-10\n"
            "agent-f,100.0\n"
        )

    def run_pipeline(self):
        return process_telemetry(
            self.config, self.telemetry, self.output
        )

    # TEST 1: Normal processing
    def test_normal(self):
        result = self.run_pipeline()

        self.assertEqual(result, {
            "total_records": 6,
            "valid_records": 4,
            "invalid_records": 2,
            "high_gpu_agents": ["agent-b", "agent-d", "agent-f"]
        })

        # Also verify the output file.
        self.assertEqual(
            json.loads(self.output.read_text()),
            result
        )

    # TEST 2: Boundary conditions
    def test_threshold_boundary(self):
        self.telemetry.write_text(
            "agent_id,gpu_utilization\n"
            "a,80\n"
            "b,80.01\n"
            "c,0\n"
            "d,100\n"
        )

        result = self.run_pipeline()

        self.assertEqual(result["valid_records"], 4)
        self.assertEqual(
            result["high_gpu_agents"], ["b", "d"]
        )

    # TEST 3: Malformed rows
    def test_malformed_rows(self):
        self.telemetry.write_text(
            "agent_id,gpu_utilization\n"
            "good,90\n"
            ",90\n"
            "a,nan\n"
            "b,inf\n"
            "c,abc\n"
            "d,110\n"
            "e,30\n"
            "bad,row,extra\n"
        )

        result = self.run_pipeline()

        self.assertEqual(result["total_records"], 8)
        self.assertEqual(result["valid_records"], 2)
        self.assertEqual(result["invalid_records"], 6)
        self.assertEqual(result["high_gpu_agents"], ["good"])

    # TEST 4: Invalid configuration values
    def test_invalid_config(self):
        bad_configs = [
            {},
            {"gpu_threshold": None},
            {"gpu_threshold": True},
            {"gpu_threshold": "80"},
            {"gpu_threshold": -1},
            {"gpu_threshold": 101},
            [],
        ]

        for config in bad_configs:
            with self.subTest(config=config):
                self.config.write_text(json.dumps(config))

                with self.assertRaisesRegex(
                    ValueError, "Invalid configuration"
                ):
                    self.run_pipeline()

    # TEST 5: Corrupted JSON
    def test_malformed_json(self):
        self.config.write_text("{invalid json")

        with self.assertRaisesRegex(
            ValueError, "Invalid configuration"
        ):
            self.run_pipeline()

    # TEST 6: Missing configuration file
    def test_missing_config(self):
        self.config.unlink()

        with self.assertRaisesRegex(
            RuntimeError, "Configuration unavailable"
        ):
            self.run_pipeline()

    # TEST 7: Missing telemetry file
    def test_missing_telemetry(self):
        self.telemetry.unlink()

        with self.assertRaisesRegex(
            RuntimeError, "Telemetry unavailable"
        ):
            self.run_pipeline()

    # TEST 8: Empty CSV
    def test_empty_csv(self):
        self.telemetry.write_text("")

        with self.assertRaisesRegex(
            ValueError, "Invalid telemetry schema"
        ):
            self.run_pipeline()

    # TEST 9: Incorrect CSV header
    def test_bad_header(self):
        self.telemetry.write_text(
            "agent_id,gpu_utilizations\n"
            "agent-a,90\n"
        )

        with self.assertRaisesRegex(
            ValueError, "Invalid telemetry schema"
        ):
            self.run_pipeline()

    # TEST 10: Output writing failure
    def test_output_write_failure(self):
        self.output = self.root / "nonexistent" / "summary.json"

        # Must propagate OSError, NOT RuntimeError.
        with self.assertRaises(OSError):
            self.run_pipeline()


if __name__ == "__main__":
    unittest.main()