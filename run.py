from flask import Flask, render_template, request, send_file
from calculos import procesar_entrada_vlsm
from pdfGen import generar_pdf_arbol_bytes, generar_pdf_resumen_bytes

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
    # Recalcula para obtener los datos
    ip = request.form['ip']
    hosts = request.form['hosts']
    resultado = procesar_entrada_vlsm(ip, hosts)

    # Genera el PDF en memoria
    buffer = generar_pdf_arbol_bytes(resultado['arbol'])
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='arbol_subredes.pdf'
            )

@app.route('/generar_pdf_resumen', methods=['POST'])
def generar_pdf_resumen():
    # Recalcula para obtener los datos
    ip = request.form['ip']
    hosts = request.form['hosts']
    resultado = procesar_entrada_vlsm(ip, hosts)

    # Genera el PDF en memoria
    buffer = generar_pdf_resumen_bytes(resultado['subredes'])
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='resumen_subredes.pdf'
    )

if __name__ == '__main__':
    app.run()
