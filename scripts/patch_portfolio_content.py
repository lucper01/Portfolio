from pathlib import Path
import datetime
import re
import subprocess
import sys

INDEX = Path("index.html")
BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

html = INDEX.read_text(encoding="utf-8")
original = html

favicon_block = """  <link rel="shortcut icon" href="/Portfolio/favicon.ico?v=20261002" />
  <link rel="icon" href="/Portfolio/favicon.ico?v=20261002" sizes="any" />
  <link rel="icon" type="image/png" sizes="256x256" href="/Portfolio/assets/favicon.png?v=20261002" />
  <link rel="apple-touch-icon" href="/Portfolio/assets/favicon.png?v=20261002" />
"""

# Remove previous favicon declarations only, then reinsert a cache-busted block.
html = re.sub(
    r"\n\s*<link\s+rel=\"(?:shortcut icon|icon|apple-touch-icon)\"[^>]*(?:favicon|apple-touch-icon)[^>]*>\s*",
    "\n",
    html,
)

needle = '  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
if needle not in html:
    print("Viewport meta tag not found. Favicon block was not inserted.", file=sys.stderr)
    sys.exit(1)

html = html.replace(needle, needle + "\n" + favicon_block, 1)

if html == original:
    print("No favicon changes to apply.")
    sys.exit(0)

timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
backup_path = BACKUP_DIR / f"index_backup_avant_favicon_cachebust_{timestamp}.html"
backup_path.write_text(original, encoding="utf-8")
INDEX.write_text(html, encoding="utf-8")

scripts = re.findall(r"<script>([\s\S]*?)</script>", html)
check_file = Path("/tmp/index_script_check.js")
check_file.write_text("\n\n".join(scripts), encoding="utf-8")
subprocess.run(["node", "--check", str(check_file)], check=True)

print(f"Updated favicon links and created backup {backup_path}")
