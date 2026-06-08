"""
Manually check both English->Chinese and Chinese->English translation.
"""

import asyncio

from _helpers import load_translation_config, require_real_api_key
from voxgo.translation import GameTranslator


SAMPLES = [
    ("en", "zh", "Are they pushing B site now?"),
    ("zh", "en", "他们是不是已经转点去 B 点了？"),
]


async def translate_once(source_lang: str, target_lang: str, text: str) -> None:
    config = load_translation_config(source_lang=source_lang, target_lang=target_lang)
    require_real_api_key(config.api_key, config.provider)
    translator = GameTranslator(config)
    try:
        result = await translator.translate(text, source_lang)
        print(f"{source_lang}->{target_lang}: {text} -> {result}")
    finally:
        await translator.close()


async def main():
    for source_lang, target_lang, text in SAMPLES:
        await translate_once(source_lang, target_lang, text)


if __name__ == "__main__":
    asyncio.run(main())
