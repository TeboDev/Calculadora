from flask import Flask, render_template, request
from fpdf import FPDF
from calculos import procesar_entrada_vlsm  # función que vas a definir

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        ip = request.form['ip']
        hosts = request.form['hosts']
        resultado = procesar_entrada_vlsm(ip, hosts)
    return render_template('index.html', resultado=resultado)

@app.route('/generar_pdf_arbol', methods=['POST'])
def generar_pdf_arbol():
    # Obtener los datos del árbol (ya calculados)
    arbol_str = request.form.get('arbol')  # Aquí debes extraer el árbol de alguna variable global o sesión

    # Crear el objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Árbol de Subredes", ln=True, align='C')

    # Insertar el contenido del árbol
    pdf.multi_cell(0, 10, arbol_str)

    # Guardar el PDF en memoria
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    # Devolver el PDF como descarga
    return send_file(pdf_output, as_attachment=True, download_name="arbol_subredes.pdf", mimetype="application/pdf")

# Ruta para generar el PDF del resumen
@app.route('/generar_pdf_resumen', methods=['POST'])
def generar_pdf_resumen():
    # Obtener los datos del resumen (ya calculados)
    resumen_str = request.form.get('resumen')  # Similar, extrae el resumen de alguna variable global o sesión

    # Crear el objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Resumen de Subredes", ln=True, align='C')

    # Insertar el contenido del resumen
    pdf.multi_cell(0, 10, resumen_str)

    # Guardar el PDF en memoria
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)

    # Devolver el PDF como descarga
    return send_file(pdf_output, as_attachment=True, download_name="resumen_subredes.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run()

