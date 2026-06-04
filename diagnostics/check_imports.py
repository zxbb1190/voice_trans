import importlib


MODULES = [
    ("faster_whisper", "faster-whisper"),
    ("PyQt5", "PyQt5"),
    ("pyaudiowpatch", "PyAudioWPatch"),
    ("webrtcvad", "webrtcvad"),
    ("keyboard", "keyboard"),
    ("aiohttp", "aiohttp"),
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
    ("websockets", "websockets"),
    ("soxr", "soxr"),
    ("qrcode", "qrcode"),
    ("PIL", "Pillow"),
    ("loguru", "loguru"),
]


def main() -> int:
    print("Checking Python package imports...")
    failures = []

    for module_name, display_name in MODULES:
        try:
            module = importlib.import_module(module_name)
            version = getattr(module, "__version__", "")
            suffix = f" {version}" if version else ""
            print(f"OK {display_name}{suffix}")
        except Exception as exc:
            failures.append(display_name)
            print(f"FAIL {display_name}: {exc}")

    if failures:
        print(f"\nImport check failed: {', '.join(failures)}")
        return 1

    print("\nAll imports passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
