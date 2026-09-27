from pathlib import Path
import datetime
import re
import subprocess

SOURCE_BACKUP = Path("backups/index_backup_avant_ancrage_mobile_20260927_1105.html")
INDEX = Path("index.html")
BACKUP_DIR = Path("backups")
BACKUP_DIR.mkdir(exist_ok=True)

if not SOURCE_BACKUP.exists():
    raise FileNotFoundError(f"Source backup not found: {SOURCE_BACKUP}")

current = INDEX.read_text(encoding="utf-8") if INDEX.exists() else ""
html = SOURCE_BACKUP.read_text(encoding="utf-8")

# Sauvegarde de l'etat courant avant restauration propre.
timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
(BACKUP_DIR / f"index_backup_avant_v66_{timestamp}.html").write_text(current, encoding="utf-8")

# Description Nuit des Chercheurs.
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

# Descriptions des axes.
axis1_old_variants = [
    "Cet axe vise à déterminer les limites spatio-temporelles de l'olfaction, en les comparant à celles de l'audition et de la vision, et en étudiant leurs interactions. Il porte notamment sur les fenêtres d'intégration temporelle et sur les conditions dans lesquelles les odeurs peuvent être intégrées ou recalibrées avec les sons et les images.",
    "Cet axe explore la manière dont l'olfaction se situe dans l'espace et dans le temps, en comparaison et en interaction avec la vision et l'audition.",
]
axis1_new = "Cet axe vise à caractériser les limites spatiales et temporelles de l'olfaction en les comparant à celles de l'audition et de la vision, et en étudiant leurs interactions."
axis2_old_variants = [
    "Cet axe vise à caractériser la manière dont les odeurs peuvent moduler la perception visuelle de l'espace, orienter l'attention spatiale et modifier la représentation de scènes ou d'événements.",
    "Cet axe examine comment les odeurs peuvent modifier la perception de l'espace, du temps et des événements dans les autres modalités sensorielles.",
]
axis2_new = "Cet axe vise à caractériser la manière dont les odeurs peuvent moduler la perception spatiale et temporelle de l'audition et de la vision."
for old in axis1_old_variants:
    html = html.replace(old, axis1_new)
for old in axis2_old_variants:
    html = html.replace(old, axis2_new)

# Correctifs mobiles et confort de navigation.
mobile_css = r'''

    /* v66 - confort mobile, retour haut, ancrage horizontal */
    @media (max-width: 760px) {
      html,
      body {
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        overscroll-behavior-x: none;
      }

      body { position: relative; }

      main,
      section,
      header,
      .hero,
      .container,
      .section-card,
      .content-card,
      .nav-inner {
        max-width: 100vw !important;
        overflow-x: hidden !important;
      }

      img,
      video,
      canvas,
      svg {
        max-width: 100% !important;
        height: auto;
      }

      .nav-toggle {
        position: fixed !important;
        left: 14px !important;
        bottom: 18px !important;
        z-index: 1600 !important;
        box-shadow: 0 12px 30px rgba(11, 47, 35, 0.24) !important;
      }

      .back-to-top,
      .to-top,
      [data-back-to-top] {
        position: fixed !important;
        right: 14px !important;
        bottom: 18px !important;
        z-index: 1600 !important;
        width: 48px !important;
        height: 48px !important;
        border-radius: 999px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 12px 30px rgba(11, 47, 35, 0.24) !important;
      }
    }
'''
if "v66 - confort mobile" not in html:
    html = html.replace("</style>", mobile_css + "\n  </style>", 1)

mobile_js = r'''
<script>
  (function portfolioMobileEnhancementsV66() {
    const sectionIcons = {
      about: "👤",
      team: "👥",
      thesis: "🧠",
      side: "🧪",
      training: "🎓",
      publications: "📚",
      recruitment: "📝",
      contact: "✉️"
    };

    function iconizeSections() {
      document.querySelectorAll("main section[id]").forEach((section) => {
        const icon = sectionIcons[section.id];
        const title = section.querySelector("h2");
        if (!icon || !title) return;
        const clean = title.textContent.replace(/^[^A-Za-zÀ-ÿ0-9]+\s*/u, "").trim();
        title.textContent = `${icon} ${clean}`;
      });
    }

    function stabilizeMobileMenu() {
      const nav = document.querySelector("nav.site-nav");
      const toggle = document.querySelector(".nav-toggle");
      document.querySelectorAll("nav.site-nav a[href^='#']").forEach((link) => {
        link.addEventListener("click", () => {
          document.body.classList.remove("nav-open", "menu-open", "mobile-nav-open");
          nav?.classList.remove("open", "active", "expanded");
          toggle?.setAttribute("aria-expanded", "false");
        });
      });
    }

    document.addEventListener("DOMContentLoaded", () => {
      iconizeSections();
      stabilizeMobileMenu();
      const observer = new MutationObserver(() => iconizeSections());
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
    });
  })();
</script>
'''
if "portfolioMobileEnhancementsV66" not in html:
    html = html.replace("</body>", mobile_js + "\n</body>", 1)

INDEX.write_text(html, encoding="utf-8")
(BACKUP_DIR / "index_v66_descriptions_axes_20260927_1350.html").write_text(html, encoding="utf-8")

scripts = re.findall(r"<script>([\s\S]*?)</script>", html)
check_file = Path("/tmp/index_script_check.js")
check_file.write_text("\n\n".join(scripts), encoding="utf-8")
subprocess.run(["node", "--check", str(check_file)], check=True)
print("v66 restored, patched and saved")
