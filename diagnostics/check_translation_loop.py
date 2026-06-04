"""
Manually check repeated translations on one persistent asyncio loop.
"""

import asyncio
import threading
import time

from _helpers import load_translation_config, require_real_api_key
from translator import GameTranslator


SAMPLES = [
    "Good as the battery technology and honestly what",
    "Are they actually ahead of us?",
]


def main() -> None:
    config = load_translation_config()
    require_real_api_key(config.api_key, config.provider)
    loop = asyncio.new_event_loop()

    def run_loop():
        asyncio.set_event_loop(loop)
        loop.run_forever()

    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()
    while not loop.is_running():
        time.sleep(0.01)

    translator = GameTranslator(config)

    try:
        for text in SAMPLES:
            future = asyncio.run_coroutine_threadsafe(translator.translate(text), loop)
            print(repr(future.result(timeout=45)))

        close_future = asyncio.run_coroutine_threadsafe(translator.close(), loop)
        close_future.result(timeout=3)
    finally:
        loop.call_soon_threadsafe(loop.stop)
        thread.join(timeout=3)
        loop.close()


if __name__ == "__main__":
    main()
