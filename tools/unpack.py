"""Unpack reviewed Chronos source bundle into normal GitHub files."""
import base64, brotli, json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
encoded = (root/"source"/"chronos-source.b64").read_text(encoding="ascii")
files = json.loads(brotli.decompress(base64.b64decode(encoded)).decode("utf-8"))
for name, content in files.items():
    dest = (root/name).resolve()
    if not dest.is_relative_to(root) or dest.name == "chronos.db":
        raise ValueError(f"Unsafe bundle path: {name}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
print(f"Unpacked {len(files)} tracked source files")
