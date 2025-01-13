import os
from dotenv import load_dotenv

load_dotenv()

FEATURE_FLAGS = {
    "RED_LINE": os.getenv("RED_LINE") == "true",
}


def is_feature_enabled(flag_name: str) -> bool:
    return FEATURE_FLAGS.get(flag_name, False)
