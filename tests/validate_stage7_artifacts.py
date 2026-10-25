#!/usr/bin/env python3
"""Valida os artefatos documentais produzidos na Etapa 7."""

from pathlib import Path
from zipfile import ZipFile

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
REPORT_1 = ROOT / "docs" / "relatorios" / "CardioIA_Parte_1_Edge_Computing.pdf"
REPORT_2 = ROOT / "docs" / "relatorios" / "CardioIA_Parte_2_MQTT_Dashboard.pdf"
PPTX = ROOT / "docs" / "apresentacao" / "CardioIA_Fase3_Apresentacao_Equipe_Revisao_v2.pptx"
AUDIT_DOC = ROOT / "docs" / "ETAPA_7_AUDITORIA_PRE_APRESENTACAO.md"
AUDIT_EVIDENCE = ROOT / "evidencias" / "etapa-7" / "E7-05-auditoria-pre-apresentacao.txt"
checks = 0


def require(condition: bool, message: str) -> None:
    global checks
    assert condition, message
    checks += 1


def pdf_links(reader: PdfReader) -> set[str]:
    links = set()
    for page in reader.pages:
        for annotation_ref in page.get("/Annots", []):
            annotation = annotation_ref.get_object()
            action = annotation.get("/A")
            if action and action.get("/URI"):
                links.add(str(action["/URI"]))
    return links


for path in [REPORT_1, REPORT_2, PPTX]:
    require(path.exists() and path.stat().st_size > 20_000, f"Artefato ausente ou vazio: {path}")
for path in [AUDIT_DOC, AUDIT_EVIDENCE]:
    require(path.exists() and path.stat().st_size > 500, f"Auditoria ausente ou incompleta: {path}")

reader_1 = PdfReader(str(REPORT_1))
reader_2 = PdfReader(str(REPORT_2))
require(len(reader_1.pages) >= 1, "Relatório da Parte 1 abaixo do mínimo")
require(len(reader_2.pages) >= 2, "Relatório da Parte 2 abaixo do mínimo")
require("ESP32" in "".join(page.extract_text() or "" for page in reader_1.pages), "Parte 1 sem conteúdo técnico")
require("Node-RED" in "".join(page.extract_text() or "" for page in reader_2.pages), "Parte 2 sem conteúdo técnico")
require(len(pdf_links(reader_1)) >= 3, "Parte 1 sem os links públicos esperados")
require(len(pdf_links(reader_2)) >= 5, "Parte 2 sem os links públicos esperados")

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
for url in [
    "https://github.com/FabricioMouzer/CardioIA-Fase3-Monitoramento-IoT",
    "https://wokwi.com/projects/478851580032675841",
    "https://cardioia-fase3-dashboard.onrender.com/dashboard/monitoramento",
    "CardioIA_Parte_1_Edge_Computing.pdf",
    "CardioIA_Parte_2_MQTT_Dashboard.pdf",
]:
    require(url in relationships, f"Hyperlink ausente no PowerPoint: {url}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
require("RELATORIO_EDGE_COMPUTING.md" in readme, "README sem relatório da Parte 1")
require("RELATORIO_MQTT_DASHBOARD.md" in readme, "README sem relatório da Parte 2")
require("CardioIA_Fase3_Apresentacao_Equipe_Revisao_v2.pptx" in readme, "README sem PowerPoint de revisão")

print(f"Etapa 7: {checks} verificações documentais aprovadas; revisão do grupo ainda necessária.")
