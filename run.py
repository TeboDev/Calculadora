from flask import Flask, render_template, request
from fpdf import FPDF
from io import BytesIO
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
    ip = request.form['ip']
    hosts = request.form['hosts']
    resultado = procesar_entrada_vlsm(ip, hosts)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',14)
    pdf.cell(0,10,'Árbol de Subredes',ln=True,align='C')
    pdf.set_font('Courier','',10)
    pdf.ln(5)
    for linea in resultado['arbol'].splitlines():
        pdf.cell(0,6,linea,ln=True)

    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(
        buf,
        mimetype='application/pdf',
        as_attachment=True,
        attachment_filename='arbol_subredes.pdf',  # ← aquí
        cache_timeout=0
    )

@app.route('/generar_pdf_resumen', methods=['POST'])
def generar_pdf_resumen():
    ip = request.form['ip']
    hosts = request.form['hosts']
    resultado = procesar_entrada_vlsm(ip, hosts)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial','B',14)
    pdf.cell(0,10,'Resumen de Subredes',ln=True,align='C')
    pdf.ln(5)
    # tabla...
    headers = ['Nombre','Red','Primera IP','Última IP','Broadcast','Máscara']
    col_w = pdf.w/len(headers) - 10
    pdf.set_font('Arial','B',10)
    for h in headers:
        pdf.cell(col_w,8,h,1,0,'C')
    pdf.ln()
    pdf.set_font('Arial','',10)
    for s in resultado['subredes']:
        pdf.cell(col_w,8,s['nombre'],1)
        if s.get('ipRed')!='No asignado':
            pdf.cell(col_w,8,s['ipRed'],1)
            pdf.cell(col_w,8,s['ipPrimera'],1)
            pdf.cell(col_w,8,s['ipUltima'],1)
            pdf.cell(col_w,8,s['ipBroadcast'],1)
            pdf.cell(col_w,8,'/'+str(s['mascara']),1)
        else:
            pdf.cell(col_w*5,8,'No asignado',1,0,'C')
        pdf.ln()

    buf = BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return send_file(
        buf,
        mimetype='application/pdf',
        as_attachment=True,
        attachment_filename='resumen_subredes.pdf',  # ← y aquí
        cache_timeout=0
    )

if __name__ == '__main__':
    app.run()

