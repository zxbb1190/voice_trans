"""
Manually check the configured OpenAI-compatible Chat Completions endpoint.
"""

import asyncio

import aiohttp

from _helpers import (
    endpoint_requires_api_key,
    is_placeholder_api_key,
    load_translation_config,
    normalized_chat_endpoint,
)
from voxgo.translation import GameTranslator


def main() -> None:
    asyncio.run(run_check())


async def run_check() -> None:
    config = load_translation_config()
    if config.provider != "openai_compatible":
        raise SystemExit("Set translation.provider to openai_compatible in config.json first.")

    endpoint = normalized_chat_endpoint(config.endpoint)
    if is_placeholder_api_key(config.api_key) and endpoint_requires_api_key(endpoint):
        raise SystemExit("Missing real OpenAI-compatible API key in config.json.")

    headers = {"Content-Type": "application/json"}
    if not is_placeholder_api_key(config.api_key):
        headers["Authorization"] = f"Bearer {config.api_key}"

    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": "你是翻译助手。只把英文翻译成中文，不要解释。"},
            {"role": "user", "content": "Translate to Chinese: Are they actually ahead of us?"},
        ],
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
        "stream": False,
    }

    print(f"endpoint={endpoint}")
    print(f"model={config.model}")
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(endpoint, headers=headers, json=payload) as response:
            body = await response.text()
            print(f"status={response.status}")
            print(f"trace={response.headers.get('x-siliconcloud-trace-id', '')}")
            print(body[:1000])
            response.raise_for_status()
            data = await response.json()

    message = data["choices"][0]["message"]
    print("finish_reason=", data["choices"][0].get("finish_reason"))
    print("content_repr=", repr(message.get("content", "")))
    print("reasoning_repr=", repr(message.get("reasoning_content", "")))

    print("\nTesting GameTranslator.translate()")
    config.endpoint = endpoint

    async def run_translator_test():
        translator = GameTranslator(config)
        try:
            result = await translator.translate("Are they actually ahead of us?")
            print("translator_result_repr=", repr(result))
        finally:
            await translator.close()

    await run_translator_test()


if __name__ == "__main__":
    main()
