from pathlib import Path
import datetime
import re
import subprocess
import sys

path = Path("index.html")
html = path.read_text(encoding="utf-8")
original = html

def remove_project_by_name(text, name):
    start = text.find("const PROJECTS = [")
    end = text.find("    ];", start)
    if start == -1 or end == -1:
        return text
    block = text[start:end]
    pos = block.find(f'name: "{name}"')
    if pos == -1:
        return text
    obj_start = block.rfind("      {", 0, pos)
    if obj_start == -1:
        return text
    depth = 0
    obj_end = None
    for i in range(obj_start, len(block)):
        if block[i] == "{":
            depth += 1
        elif block[i] == "}":
            depth -= 1
            if depth == 0:
                obj_end = i + 1
                break
    if obj_end is None:
        return text
    cut_end = obj_end
    while cut_end < len(block) and block[cut_end].isspace():
        cut_end += 1
    if cut_end < len(block) and block[cut_end] == ",":
        cut_end += 1
    while cut_end < len(block) and block[cut_end] in " \n":
        if block[cut_end:cut_end + 7] == "      {":
            break
        cut_end += 1
    new_block = block[:obj_start] + block[cut_end:]
    return text[:start] + new_block + text[end:]

html = remove_project_by_name(html, "SORBET")
html = remove_project_by_name(html, "COBEX")
html = html.replace('name: "OASIS"', 'name: "VIBOLF"', 1)
html = re.sub(r'axis:\s*2,\n\s*name:\s*"SOLAR"', 'axis: 1,\n        name: "SOLAR"', html, count=1)
html = re.sub(r'\n      SORBET: \{\n        status: "closed",\n        questionnaire: "",\n        planning: ""\n      \},', '', html)
html = re.sub(r'\n      COBEX: \{\n        status: "closed",\n        questionnaire: "",\n        planning: ""\n      \},', '', html)
html = html.replace('      OASIS: {\n        status: "closed",', '      VIBOLF: {\n        status: "closed",', 1)

axis_function = '''    function axisTitle(axisNumber) {
      return axisNumber === 1
        ? (currentLanguage === "fr"
          ? "Limites Spatio-temporelles de l'olfaction comparativement et en interaction avec l'audition et la vision"
          : "Spatiotemporal limits of olfaction comparatively and in interaction with audition and vision")
        : (currentLanguage === "fr"
          ? "Influence de l'olfaction sur la perception spatio-temporelle en audition et en vision"
          : "Influence of olfaction on spatiotemporal perception in audition and vision");
    }'''
html = re.sub(r'    function axisTitle\(axisNumber\) \{[\s\S]*?\n    \}', axis_function, html, count=1)

gpn_entry = '''          {
            type: "TP",
            hours: "6 h eq. TD",
            valued: false,
            audience: {
              fr: "Masters",
              en: "Master's students"
            },
            fr: {
              title: "Graduate Programmes Neurosciences - Cardiac and Electrodermal Signatures of Emotions",
              details: "Travaux pratiques consacrés aux signatures cardiaques et électrodermales des émotions."
            },
            en: {
              title: "Graduate Programmes Neurosciences - Cardiac and Electrodermal Signatures of Emotions",
              details: "Practical class on cardiac and electrodermal signatures of emotions."
            }
          }'''
year_pos = html.find('year: "2026-2027"')
sections_pos = html.find('const SECTIONS', year_pos)
if year_pos != -1 and sections_pos != -1:
    block_2026 = html[year_pos:sections_pos]
    if "Graduate Programmes Neurosciences - Cardiac and Electrodermal Signatures of Emotions" not in block_2026:
        insert_pos = html.find("        ]\n      }\n    ];", year_pos)
        if insert_pos != -1:
            html = html[:insert_pos] + ",\n" + gpn_entry + "\n" + html[insert_pos:]

if 'nuitChercheurs: "Nuit des Chercheurs 2026"' not in html:
    html = html.replace(
        '        jddText: "Présentation des travaux de thèse et obtention du prix de l\'originalité pour une approche scientifique audacieuse et créative qui a surpris et inspiré le jury.",\n        contact: "Contact",',
        '        jddText: "Présentation des travaux de thèse et obtention du prix de l\'originalité pour une approche scientifique audacieuse et créative qui a surpris et inspiré le jury.",\n        nuitChercheurs: "Nuit des Chercheurs 2026",\n        nuitChercheursText: "Communication réalisée dans le cadre de la Nuit des Chercheurs 2026, dont le thème général portait sur les émotions. Présentation autour de la visualisation de l\'impact émotionnel des odeurs à partir de mesures physiologiques.",\n        contact: "Contact",',
        1
    )
if 'nuitChercheurs: "Researchers\' Night 2026"' not in html:
    html = html.replace(
        '        jddText: "Presentation of thesis work and recipient of the Originality Award for a bold and creative scientific approach that surprised and inspired the jury.",\n        contact: "Contact",',
        '        jddText: "Presentation of thesis work and recipient of the Originality Award for a bold and creative scientific approach that surprised and inspired the jury.",\n        nuitChercheurs: "Researchers\' Night 2026",\n        nuitChercheursText: "Scientific communication presented during Researchers\' Night 2026, whose general theme focused on emotions. The presentation addressed the visualization of the emotional impact of odors through physiological measures.",\n        contact: "Contact",',
        1
    )

html = html.replace('{ value: "1", label: "Communication" },', '{ value: "2", label: "Communications" },', 1)
html = html.replace('{ value: "1", label: "Communication" },', '{ value: "2", label: "Communications" },', 1)

if "${escapeHtml(data.nuitChercheurs)}" not in html:
    html = html.replace(
        '''                    <li class="filter-item" data-category="communication">
                      <span class="publication-type">Communication</span>
                      <strong>${escapeHtml(data.jdd)}</strong>
                      <p>${escapeHtml(data.jddText)}</p>
                    </li>''',
        '''                    <li class="filter-item" data-category="communication">
                      <span class="publication-type">Communication</span>
                      <strong>${escapeHtml(data.jdd)}</strong>
                      <p>${escapeHtml(data.jddText)}</p>
                    </li>
                    <li class="filter-item" data-category="communication">
                      <span class="publication-type">Communication</span>
                      <strong>${escapeHtml(data.nuitChercheurs)}</strong>
                      <p>${escapeHtml(data.nuitChercheursText)}</p>
                    </li>''',
        1
    )

if html == original:
    print("No content changes to apply.")
    sys.exit(0)

backup_dir = Path("backups")
backup_dir.mkdir(exist_ok=True)
timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
backup_path = backup_dir / f"index_backup_avant_modifs_contenu_{timestamp}.html"
backup_path.write_text(original, encoding="utf-8")
path.write_text(html, encoding="utf-8")

scripts = re.findall(r"<script>([\s\S]*?)</script>", html)
check_file = Path("/tmp/index_script_check.js")
check_file.write_text("\n\n".join(scripts), encoding="utf-8")
subprocess.run(["node", "--check", str(check_file)], check=True)
print(f"Updated index.html and created backup {backup_path}")
