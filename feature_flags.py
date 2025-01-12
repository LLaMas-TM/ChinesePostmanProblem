from dotenv import load_dotenv
import os


FEATURE_FLAGS = {
    "RED_LINE": os.getenv("RED_LINE") == "true",
}

def is_feature_enabled(flag_name: str) -> bool:
    return FEATURE_FLAGS.get(flag_name, False)