import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from voxgo.i18n import (
    UI_LANGUAGE_EN,
    UI_LANGUAGE_ZH,
    is_english_ui,
    language_label,
    normalize_ui_language,
    ui_text,
)


class I18nTest(unittest.TestCase):
    def test_normalize_ui_language(self):
        self.assertEqual(normalize_ui_language(""), UI_LANGUAGE_ZH)
        self.assertEqual(normalize_ui_language("zh_CN"), UI_LANGUAGE_ZH)
        self.assertEqual(normalize_ui_language("English"), UI_LANGUAGE_EN)
        self.assertEqual(normalize_ui_language("en-US"), UI_LANGUAGE_EN)

    def test_ui_text_and_language_labels_follow_ui_language(self):
        self.assertFalse(is_english_ui(UI_LANGUAGE_ZH))
        self.assertTrue(is_english_ui(UI_LANGUAGE_EN))
        self.assertEqual(ui_text(UI_LANGUAGE_ZH, "中文", "English"), "中文")
        self.assertEqual(ui_text(UI_LANGUAGE_EN, "中文", "English"), "English")
        self.assertEqual(language_label("en", UI_LANGUAGE_ZH), "英语")
        self.assertEqual(language_label("zh", UI_LANGUAGE_EN), "Chinese")


if __name__ == "__main__":
    unittest.main()
