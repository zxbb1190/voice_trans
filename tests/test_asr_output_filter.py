import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voxgo.asr.whisper_engine import TranscriptionResult, should_drop_transcription_result


def _result(text, avg_logprob=-0.2, no_speech_prob=0.2):
    return TranscriptionResult(
        text,
        "en",
        0.95,
        avg_logprob=avg_logprob,
        no_speech_prob=no_speech_prob,
        compression_ratio=1.0,
        segment_count=1,
    )


class ASROutputFilterTest(unittest.TestCase):
    def test_high_no_speech_short_phrase_is_filtered(self):
        reason = should_drop_transcription_result(_result("Thank you.", avg_logprob=-0.89, no_speech_prob=0.80))

        self.assertIn("global_asr_no_speech_short", reason)

    def test_low_logprob_short_noise_is_filtered(self):
        reason = should_drop_transcription_result(_result("Got it.", avg_logprob=-1.27, no_speech_prob=0.20))

        self.assertIn("global_asr_low_logprob_short", reason)

    def test_yoy_noise_token_is_filtered(self):
        reason = should_drop_transcription_result(_result("Yoy.", avg_logprob=-1.27, no_speech_prob=0.40))

        self.assertIn("global_asr_noise_token", reason)

    def test_short_noise_token_is_filtered(self):
        reason = should_drop_transcription_result(_result("BAM", avg_logprob=-0.97, no_speech_prob=0.36))

        self.assertIn("global_asr_noise_token", reason)

    def test_repeated_noise_word_is_filtered(self):
        reason = should_drop_transcription_result(_result("Shoooooo", avg_logprob=-0.09, no_speech_prob=0.52))

        self.assertIn("global_asr_repeated_noise", reason)

    def test_real_short_sentence_is_kept(self):
        reason = should_drop_transcription_result(_result("I don't know.", avg_logprob=-0.47, no_speech_prob=0.14))

        self.assertEqual(reason, "")

    def test_game_command_is_not_filtered_just_for_being_short(self):
        reason = should_drop_transcription_result(_result("push", avg_logprob=-0.2, no_speech_prob=0.2))

        self.assertEqual(reason, "")


if __name__ == "__main__":
    unittest.main()
