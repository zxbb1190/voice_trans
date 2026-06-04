import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from translator import (
    GOOGLE_TRANSLATE_ENDPOINT,
    GameTranslator,
    TranslationConfig,
    normalize_translation_provider,
)


class FakeResponse:
    status = 200

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def json(self):
        return {
            "data": {
                "translations": [
                    {"translatedText": "敌人 &amp; 队友"},
                ]
            }
        }

    async def text(self):
        return ""


class FakeSession:
    closed = False

    def __init__(self):
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append({"url": url, **kwargs})
        return FakeResponse()


class GoogleTranslationProviderTest(unittest.IsolatedAsyncioTestCase):
    def test_provider_aliases_are_normalized(self):
        self.assertEqual(normalize_translation_provider("google-cloud-translation"), "google")
        self.assertEqual(normalize_translation_provider("openai"), "openai_compatible")

    async def test_missing_google_api_key_returns_user_message(self):
        translator = GameTranslator(TranslationConfig(provider="google", api_key=""))
        result = await translator.translate("Are they pushing B site now?", "en")

        self.assertIn("Google Cloud Translation API Key", result)

    async def test_google_translation_request_and_html_unescape(self):
        translator = GameTranslator(
            TranslationConfig(
                provider="google",
                api_key="TEST_GOOGLE_KEY",
                source_lang="en",
                target_lang="zh",
            )
        )
        fake_session = FakeSession()
        translator._session = fake_session

        result = await translator.translate("Are they pushing B site now?", "en")

        self.assertEqual(result, "敌人 & 队友")
        self.assertEqual(len(fake_session.calls), 1)

        call = fake_session.calls[0]
        self.assertEqual(call["url"], GOOGLE_TRANSLATE_ENDPOINT)
        self.assertEqual(
            call["params"],
            {
                "key": "TEST_GOOGLE_KEY",
                "q": "Are they pushing B site now?",
                "source": "en",
                "target": "zh-CN",
                "format": "text",
            },
        )
        self.assertTrue(call["headers"]["Content-Type"].startswith("application/json"))


if __name__ == "__main__":
    unittest.main()
