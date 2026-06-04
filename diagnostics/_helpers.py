import json
import sys
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from translator import TranslationConfig, normalize_translation_provider


PLACEHOLDER_KEYS = {
    "",
    "YOUR_API_KEY",
    "YOUR_SILICONFLOW_API_KEY",
    "YOUR_OPENAI_COMPATIBLE_API_KEY",
    "YOUR_GOOGLE_TRANSLATE_API_KEY",
    "YOUR_GOOGLE_CLOUD_TRANSLATION_API_KEY",
}
LOCAL_ENDPOINT_HOSTS = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}


def load_config() -> dict:
    config_path = PROJECT_ROOT / "config.json"
    if not config_path.exists():
        raise SystemExit(
            f"Missing {config_path}. Copy config.example.json to config.json first."
        )
    return json.loads(config_path.read_text(encoding="utf-8"))


def load_translation_config(**overrides) -> TranslationConfig:
    translation = load_config().get("translation", {})
    values = {
        "provider": normalize_translation_provider(translation.get("provider", "")),
        "api_key": translation.get("api_key", ""),
        "model": translation.get("model", TranslationConfig.model),
        "endpoint": translation.get("endpoint", TranslationConfig.endpoint),
        "max_tokens": translation.get("max_tokens", TranslationConfig.max_tokens),
        "temperature": translation.get("temperature", TranslationConfig.temperature),
        "source_lang": translation.get("source_lang", TranslationConfig.source_lang),
        "target_lang": translation.get("target_lang", TranslationConfig.target_lang),
        "context_messages": translation.get(
            "context_messages", TranslationConfig.context_messages
        ),
        "timeout_seconds": translation.get(
            "timeout_seconds", TranslationConfig.timeout_seconds
        ),
    }
    values.update(overrides)
    return TranslationConfig(**values)


def require_real_api_key(api_key: str, provider_name: str) -> None:
    if is_placeholder_api_key(api_key):
        raise SystemExit(f"Missing real {provider_name} API key in config.json.")


def is_placeholder_api_key(api_key: str) -> bool:
    return (api_key or "").strip() in PLACEHOLDER_KEYS


def endpoint_requires_api_key(endpoint: str) -> bool:
    endpoint = normalized_chat_endpoint(endpoint)
    host = (urlparse(endpoint).hostname or "").lower()
    return host not in LOCAL_ENDPOINT_HOSTS


def normalized_chat_endpoint(endpoint: str) -> str:
    endpoint = (endpoint or "").strip().rstrip("/")
    if not endpoint:
        endpoint = TranslationConfig.endpoint.rstrip("/")
    if endpoint.endswith("/chat/completions"):
        return endpoint
    return f"{endpoint}/chat/completions"
