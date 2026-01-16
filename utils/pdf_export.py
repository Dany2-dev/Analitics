from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import plotly.io as pio
import tempfile
import os


def export_dashboard_pdf(filename, title, kpis, figures):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    story = []

    # =========================
    # TÍTULO
    # =========================
    story.append(Paragraph(f"<b>{title}</b>", styles["Title"]))
    story.append(Spacer(1, 14))

    # =========================
    # KPIs
    # =========================
    for label, value in kpis.items():
        story.append(
            Paragraph(f"<b>{label}:</b> {value}", styles["Normal"])
        )

    story.append(Spacer(1, 18))

    # =========================
    # GRÁFICAS (EXPORTADAS A PNG)
    # =========================
    temp_files = []

    for fig in figures:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        tmp.close()  # IMPORTANTE EN WINDOWS

        pio.write_image(
            fig,
            tmp.name,
            width=900,
            height=500,
            scale=2
        )

        story.append(
            Image(tmp.name, width=17 * cm, height=9 * cm)
        )
        story.append(Spacer(1, 16))

        temp_files.append(tmp.name)

    # =========================
    # CONSTRUIR PDF
    # =========================
    doc.build(story)

    # =========================
    # LIMPIEZA DE TEMPORALES
    # =========================
    for f in temp_files:
        try:
            os.remove(f)
        except PermissionError:
            pass
