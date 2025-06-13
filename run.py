from flask import Flask, render_template, request
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

if __name__ == '__main__':
    app.run()

