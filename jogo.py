from flask import Flask, render_template, request, session, redirect, url_for
import random
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

# Armazenamento temporário dos jogos
jogos = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        palavra = request.form['palavra'].lower()
        jogo_id = str(uuid.uuid4())  # Gera um ID único para o jogo
        jogos[jogo_id] = {
            'palavra': palavra,
            'tentativas': 6,
            'letras_corretas': ['_' for _ in palavra],
            'letras_erradas': []
        }
        return redirect(url_for('compartilhar', jogo_id=jogo_id))
    return render_template('criar.html')

@app.route('/compartilhar/<jogo_id>')
def compartilhar(jogo_id):
    link_jogo = url_for('jogar', jogo_id=jogo_id, _external=True)
    return render_template('compartilhar.html', link_jogo=link_jogo)

@app.route('/jogar/<jogo_id>', methods=['GET', 'POST'])
def jogar(jogo_id):
    jogo = jogos.get(jogo_id)
    if not jogo:
        return "Jogo não encontrado!", 404

    if request.method == 'POST':
        letra = request.form['letra'].lower()
        if letra in jogo['palavra']:
            for index, char in enumerate(jogo['palavra']):
                if char == letra:
                    jogo['letras_corretas'][index] = letra
        else:
            jogo['tentativas'] -= 1
            jogo['letras_erradas'].append(letra)

        if '_' not in jogo['letras_corretas']:
            return redirect(url_for('vitoria', jogo_id=jogo_id))
        elif jogo['tentativas'] == 0:
            return redirect(url_for('derrota', jogo_id=jogo_id))

    return render_template('jogar.html', jogo=jogo, jogo_id=jogo_id)

@app.route('/vitoria/<jogo_id>')
def vitoria(jogo_id):
    jogo = jogos.get(jogo_id)
    if not jogo:
        return "Jogo não encontrado!", 404
    return render_template('vitoria.html', palavra=jogo['palavra'])

@app.route('/derrota/<jogo_id>')
def derrota(jogo_id):
    jogo = jogos.get(jogo_id)
    if not jogo:
        return "Jogo não encontrado!", 404
    return render_template('derrota.html', palavra=jogo['palavra'])

@app.route('/reset/<jogo_id>')
def reset(jogo_id):
    jogos.pop(jogo_id, None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)