from .watcher import start_watching
from .config import get_api_key

def main():
  try:
    api_key = get_api_key()
    start_watching(api_key)
  except Exception as e:
    print(f"[ERROR] {e}")