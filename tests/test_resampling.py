import sys
import unittest
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from speech_recognition import SpeechRecognizer, WhisperConfig


class ResamplingTest(unittest.TestCase):
    def test_resample_to_16k_preserves_librosa_default_length_rule(self):
        recognizer = SpeechRecognizer(WhisperConfig())
        rng = np.random.default_rng(123)

        for sample_rate in (22050, 32000, 44100, 48000):
            audio = rng.normal(0, 0.1, sample_rate // 3).astype(np.float32)
            resampled = recognizer._resample_to_16k(audio, sample_rate)
            expected_len = int(np.ceil(len(audio) * 16000 / sample_rate))

            self.assertEqual(len(resampled), expected_len)
            self.assertEqual(resampled.dtype, np.float32)

    def test_16k_audio_is_returned_without_copy_when_possible(self):
        recognizer = SpeechRecognizer(WhisperConfig())
        audio = np.arange(160, dtype=np.float32)

        resampled = recognizer._resample_to_16k(audio, 16000)

        self.assertIs(resampled, audio)


if __name__ == "__main__":
    unittest.main()
