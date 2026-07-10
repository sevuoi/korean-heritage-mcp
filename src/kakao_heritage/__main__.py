from __future__ import annotations

import argparse

from kakao_heritage.server import main


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="stdio")
    args = parser.parse_args()
    main(transport=args.transport)
