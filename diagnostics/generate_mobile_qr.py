"""
Generate a QR code PNG for manual mobile scan testing.
"""

import argparse
import socket
from pathlib import Path

import qrcode
from qrcode.constants import ERROR_CORRECT_M

from _helpers import PROJECT_ROOT, load_config


def detect_lan_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def default_mobile_url() -> str:
    try:
        config = load_config()
        port = int(config.get("websocket", {}).get("port", 8765))
    except Exception:
        port = 8765
    return f"http://{detect_lan_ip()}:{port}/mobile"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a mobile test QR code.")
    parser.add_argument("--url", default=default_mobile_url(), help="Mobile page URL.")
    parser.add_argument(
        "--output",
        default=str(PROJECT_ROOT / "mobile_qr_test.png"),
        help="Output PNG path.",
    )
    args = parser.parse_args()

    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_M, box_size=12, border=5)
    qr.add_data(args.url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    output = Path(args.output)
    image.save(output)
    print(f"url {args.url}")
    print(f"ok {output.resolve()}")


if __name__ == "__main__":
    main()
