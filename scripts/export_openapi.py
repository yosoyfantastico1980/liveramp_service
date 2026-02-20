import json
import sys
from pathlib import Path

# Add repo root to sys.path so `import main` works reliably
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from main import app  # noqa: E402

if __name__ == "__main__":
    with open(ROOT / "openapi.json", "w") as f:
        json.dump(app.openapi(), f, indent=2)
    print("Wrote openapi.json")
