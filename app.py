from flask import Flask, render_template, request, flash, redirect, send_from_directory
from tinydb import TinyDB
import functools
import os

app = Flask(__name__)

db = TinyDB('database.json')
tabela = db.table("investimentos")
app.secret_key = 'some_secret'


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                            'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/investir", methods=("POST",))
def investir():
    dados = {
        'nome': request.form.get("nome"),
        'patrulha': request.form.get("patrulha"),
        'zumbi': request.form.get("zumbi"),
        'olimpiadas': request.form.get("olimpiadas"),
    }
    tabela.insert(dados)
    flash("Obrigado pelo seu investimento!")
    return redirect("/")


@app.route("/investido")
def investidos():
    if tabela.all():
        total_zumbi = functools.reduce(lambda x, y: x+y, [int(x['zumbi']) for x in tabela.all()])
        total_olimpiadas = functools.reduce(lambda x, y: x+y, [int(x['olimpiadas']) for x in tabela.all()])
        return render_template("resultados.html", total_zumbi=total_zumbi,
            total_olimpiadas=total_olimpiadas, votos=tabela.all())
    else:
        return render_template("resultados.html")


@app.route("/limpar_tudo")
def limpar_db():
    tabela.purge()
    db.purge()
    return "Banco limpo!"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
