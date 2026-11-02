#!/usr/bin/env python3
"""Valida os artefatos documentais produzidos na Etapa 7."""

import re
import zlib
from pathlib import Path
from zipfile import ZipFile

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    PdfReader = None


ROOT = Path(__file__).resolve().parents[1]
REPORT_1 = ROOT / "docs" / "relatorios" / "CardioIA_Parte_1_Edge_Computing.pdf"
REPORT_2 = ROOT / "docs" / "relatorios" / "CardioIA_Parte_2_MQTT_Dashboard.pdf"
PPTX = ROOT / "docs" / "apresentacao" / "CardioIA_Fase3_Apresentacao_Equipe_Revisao_v5_links_corrigidos.pptx"
AUDIT_DOC = ROOT / "docs" / "ETAPA_7_AUDITORIA_PRE_APRESENTACAO.md"
AUDIT_EVIDENCE = ROOT / "evidencias" / "etapa-7" / "E7-05-auditoria-pre-apresentacao.txt"
checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    assert condition, message
    checks += 1


def inspect_pdf(path: Path, markdown_fallback: Path) -> tuple[int, str, set[str]]:
    if PdfReader is not None:
        reader = PdfReader(str(path))
        links: set[str] = set()
        for page in reader.pages:
            for annotation_ref in page.get("/Annots", []):
                annotation = annotation_ref.get_object()
                action = annotation.get("/A")
                if action and action.get("/URI"):
                    links.add(str(action["/URI"]))
        text = "".join(page.extract_text() or "" for page in reader.pages)
        return len(reader.pages), text, links

    raw_latin = path.read_bytes().decode("latin-1", errors="ignore")
    page_count = len(re.findall(r"/Type\s*/Page\b", raw_latin))
    links = set(re.findall(r"/URI\s*\((https?://[^)]+)\)", raw_latin))
    text = markdown_fallback.read_text(encoding="utf-8")
    return page_count, text, links


for path in [REPORT_1, REPORT_2, PPTX]:
    require(path.exists() and path.stat().st_size > 20_000, f"Artefato ausente ou vazio: {path}")
for path in [AUDIT_DOC, AUDIT_EVIDENCE]:
    require(path.exists() and path.stat().st_size > 500, f"Auditoria ausente ou incompleta: {path}")

pages_1, text_1, links_1 = inspect_pdf(REPORT_1, ROOT / "docs" / "RELATORIO_EDGE_COMPUTING.md")
pages_2, text_2, links_2 = inspect_pdf(REPORT_2, ROOT / "docs" / "RELATORIO_MQTT_DASHBOARD.md")
require(pages_1 >= 1, "Relatório da Parte 1 abaixo do mínimo")
require(pages_2 >= 2, "Relatório da Parte 2 abaixo do mínimo")
require("ESP32" in text_1, "Parte 1 sem conteúdo técnico")
require("Node-RED" in text_2, "Parte 2 sem conteúdo técnico")
require(len(links_1) >= 3, "Parte 1 sem os links públicos esperados")
require(len(links_2) >= 5, "Parte 2 sem os links públicos esperados")

with ZipFile(PPTX) as archive:
    names = archive.namelist()
    slides = [name for name in names if name.startswith("ppt/slides/slide") and name.endswith(".xml")]
    images = [name for name in names if name.startswith("ppt/media/")]
    relationships = "\n".join(
        archive.read(name).decode("utf-8", errors="ignore")
        for name in names
        if name.startswith("ppt/slides/_rels/") and name.endswith(".rels")
    )
require(len(slides) == 14, "A apresentação de revisão deve conter 14 slides")
require(len(images) >= 8, "As capturas de evidência não foram incorporadas")
for url_options in [
    ("https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT",),
    ("https://wokwi.com/projects/478851580032675841",),
    ("https://cardioia-fase3-dashboard.onrender.com/dashboard/monitoramento",),
    ("CardioIA_Parte_1_Edge_Computing.pdf", "RELATORIO_EDGE_COMPUTING.md"),
    ("CardioIA_Parte_2_MQTT_Dashboard.pdf", "RELATORIO_MQTT_DASHBOARD.md"),
]:
    require(
        any(opt in relationships for opt in url_options),
        f"Hyperlink ausente no PowerPoint: {url_options}",
    )

readme = (ROOT / "README.md").read_text(encoding="utf-8")
require("RELATORIO_EDGE_COMPUTING.md" in readme, "README sem relatório da Parte 1")
require("RELATORIO_MQTT_DASHBOARD.md" in readme, "README sem relatório da Parte 2")
require(
    "CardioIA_Fase3_Apresentacao_Equipe_Revisao_v5_links_corrigidos.pptx" in readme,
    "README sem PowerPoint de revisão",
)

print(f"Etapa 7: {checks} verificações documentais aprovadas; revisão do grupo ainda necessária.")
