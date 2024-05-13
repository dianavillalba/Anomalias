from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

current_date = datetime.now().strftime("%Y/%m/%d")

@app.route('/')
def home():
    return render_template('index.html', current_page='home', current_date=current_date)

@app.route('/perfil')
def perfil():
    return render_template('perfil.html', current_page='perfil', current_date=current_date)

@app.route('/anomalias')
def anomalias():
    return render_template('anomalias.html', current_page='anomalias', current_date=current_date)

@app.route('/ficha')
def ficha():
    return render_template('ficha.html', current_page='ficha', current_date=current_date)

if __name__ == '__main__':
    app.run(debug=True)