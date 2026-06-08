import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voxgo.asr.pipeline import merge_speech_segments
from voxgo.audio.capture import SpeechSegment


def _segment(byte_value: int, **overrides):
    values = {
        "audio_data": bytes([byte_value, 0]) * 1600,
        "sample_rate": 16000,
        "duration_seconds": 0.1,
        "voice_duration_seconds": 0.08,
        "block_count": 1,
        "voice_blocks": 1,
        "peak_rms_dbfs": -35.0,
        "energy_threshold_dbfs": -40.0,
        "noise_floor_dbfs": -48.0,
        "reason": f"part-{byte_value}",
    }
    values.update(overrides)
    return SpeechSegment(**values)


class SegmentMergeTest(unittest.TestCase):
    def test_merge_updates_audio_and_metadata(self):
        left = _segment(1, peak_rms_dbfs=-38.0, energy_threshold_dbfs=-42.0)
        right = _segment(2, duration_seconds=0.2, voice_duration_seconds=0.15, peak_rms_dbfs=-31.0)

        merged = merge_speech_segments(left, right, "test_merge")

        self.assertEqual(merged.audio_data, left.audio_data + right.audio_data)
        self.assertAlmostEqual(merged.duration_seconds, 0.3)
        self.assertAlmostEqual(merged.voice_duration_seconds, 0.23)
        self.assertEqual(merged.block_count, 2)
        self.assertEqual(merged.voice_blocks, 2)
        self.assertEqual(merged.peak_rms_dbfs, -31.0)
        self.assertEqual(merged.energy_threshold_dbfs, -40.0)
        self.assertIn("test_merge", merged.reason)


if __name__ == "__main__":
    unittest.main()
