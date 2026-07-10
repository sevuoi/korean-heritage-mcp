from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv()

print("Python:", sys.version)
print("Kakao API key set:", bool(os.getenv("KAKAO_REST_API_KEY")))
print("Environment check passed")
