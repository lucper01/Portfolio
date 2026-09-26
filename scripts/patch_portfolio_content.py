from pathlib import Path
import datetime
import re
import subprocess
import sys

path = Path("index.html")
html = path.read_text(encoding="utf-8")
original = html

old_fr_variants = [
    "Communication réalisée dans le cadre de la Nuit des Chercheurs 2026, dont le thème général portait sur les émotions. Présentation autour de la visualisation de l'impact émotionnel des odeurs à partir de mesures physiologiques.",
    "Présentation de la manière dont les mesures physiologiques peuvent rendre visible et aider à interpréter l'impact émotionnel des odeurs.",
]
new_fr = "Présentation de l'effet émotionnel des odeurs et de sa mesure par des indicateurs physiologiques."

old_en_variants = [
    "Scientific communication presented during Researchers' Night 2026, whose general theme focused on emotions. The presentation addressed the visualization of the emotional impact of odors through physiological measures.",
    "Presentation of how physiological measures can make the emotional impact of odors visible and help interpret it.",
]
new_en = "Presentation of the emotional effect of odors and how it can be measured through physiological indicators."

for old in old_fr_variants:
    html = html.replace(f'nuitChercheursText: "{old}",', f'nuitChercheursText: "{new_fr}",')

for old in old_en_variants:
    html = html.replace(f'nuitChercheursText: "{old}",', f'nuitChercheursText: "{new_en}",')

if html == original:
    print("No content changes to apply.")
    sys.exit(0)

backup_dir = Path("backups")
backup_dir.mkdir(exist_ok=True)
timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
backup_path = backup_dir / f"index_backup_avant_modifs_nuit_chercheurs_{timestamp}.html"
backup_path.write_text(original, encoding="utf-8")
path.write_text(html, encoding="utf-8")

scripts = re.findall(r"<script>([\s\S]*?)</script>", html)
check_file = Path("/tmp/index_script_check.js")
check_file.write_text("\n\n".join(scripts), encoding="utf-8")
subprocess.run(["node", "--check", str(check_file)], check=True)
print(f"Updated index.html and created backup {backup_path}")
