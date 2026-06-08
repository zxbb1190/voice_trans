import sys
import tempfile
import unittest
import wave
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voxgo.asr.pipeline import DebugAudioDumper
from voxgo.audio.capture import SpeechSegment
from voxgo.config.schema import AppConfig, DebugConfig


def _segment():
    return SpeechSegment(
        audio_data=b"\x01\x00" * 1600,
        sample_rate=16000,
        duration_seconds=0.1,
        voice_duration_seconds=0.08,
        block_count=1,
        voice_blocks=1,
        peak_rms_dbfs=-35.0,
        energy_threshold_dbfs=-40.0,
        noise_floor_dbfs=-48.0,
        reason="test",
    )


class DebugAudioDumpTest(unittest.TestCase):
    def test_debug_dump_writes_wav_when_enabled(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config = AppConfig(
                debug=DebugConfig(
                    enabled=True,
                    save_dropped_audio=True,
                    diagnostics_audio_dir=temp_dir,
                )
            )
            dumper = DebugAudioDumper(lambda: config)

            path = dumper.dump_if_enabled(_segment(), "queue full/drop", "save_dropped_audio")

            self.assertIsNotNone(path)
            self.assertTrue(path.exists())
            self.assertIn("peak-350", path.name)
            self.assertIn("gate-400", path.name)
            self.assertIn("voice_duration", path.name)
            self.assertIn("total_duration", path.name)
            with wave.open(str(path), "rb") as wf:
                self.assertEqual(wf.getnchannels(), 1)
                self.assertEqual(wf.getframerate(), 16000)
                self.assertGreater(wf.getnframes(), 0)

    def test_debug_dump_is_default_off(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config = AppConfig(debug=DebugConfig(diagnostics_audio_dir=temp_dir))
            dumper = DebugAudioDumper(lambda: config)

            path = dumper.dump_if_enabled(_segment(), "drop", "save_dropped_audio")

            self.assertIsNone(path)
            self.assertEqual(list(Path(temp_dir).glob("*.wav")), [])

    def test_save_failed_audio_enables_all_failure_dump_reasons(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            config = AppConfig(
                debug=DebugConfig(
                    enabled=True,
                    save_failed_audio=True,
                    diagnostics_audio_dir=temp_dir,
                )
            )
            dumper = DebugAudioDumper(lambda: config)

            path = dumper.dump_if_enabled(_segment(), "empty_asr", "save_empty_asr_audio")

            self.assertIsNotNone(path)
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
