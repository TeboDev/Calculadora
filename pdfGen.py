# pdfGen.py

from fpdf import FPDF
from io import BytesIO

def generar_pdf_arbol_bytes(arbol_str: str) -> BytesIO:
    """
    Genera un PDF con el árbol de subredes y lo devuelve como BytesIO.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Árbol de Subredes', ln=True, align='C')
    pdf.set_font('Courier', '', 10)
    pdf.ln(5)

    for linea in arbol_str.splitlines():
        pdf.cell(0, 6, linea, ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

def generar_pdf_resumen_bytes(subredes: list[dict]) -> BytesIO:
    """
    Genera un PDF con el resumen de subredes (tabla) y lo devuelve como BytesIO.
    Cada elemento de `subredes` debe ser un dict con keys:
    'nombre', 'ipRed', 'ipPrimera', 'ipUltima', 'ipBroadcast', 'mascara'
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Resumen de Subredes', ln=True, align='C')
    pdf.ln(5)

    # Encabezados
    headers = ['Nombre','Red','Primera IP','Última IP','Broadcast','Máscara']
    col_w = pdf.w / len(headers) - 10
    pdf.set_font('Arial', 'B', 10)
    for h in headers:
        pdf.cell(col_w, 8, h, border=1, ln=0, align='C')
    pdf.ln()

    # Filas
    pdf.set_font('Arial', '', 10)
    for s in subredes:
        pdf.cell(col_w, 8, s['nombre'], border=1)
        if s.get('ipRed') != 'No asignado':
            pdf.cell(col_w, 8, s['ipRed'], border=1)
            pdf.cell(col_w, 8, s['ipPrimera'], border=1)
            pdf.cell(col_w, 8, s['ipUltima'], border=1)
            pdf.cell(col_w, 8, s['ipBroadcast'], border=1)
            pdf.cell(col_w, 8, '/'+str(s['mascara']), border=1)
        else:
            pdf.cell(col_w*5, 8, 'No asignado', border=1, align='C')
        pdf.ln()

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
