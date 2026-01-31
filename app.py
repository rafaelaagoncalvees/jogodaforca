from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Lê palavras do ficheiro
with open("palavras.txt", "r", encoding="utf-8") as f:
    palavras = [linha.strip() for linha in f if linha.strip()]

jogos = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/novo_jogo", methods=["POST"])
def novo_jogo():
    jogo_id = str(random.randint(1000, 9999))
    palavra = random.choice(palavras)
    # cria lista de descoberta, mantendo espaços
    descoberta = [c if c == " " else "_" for c in palavra]
    jogos[jogo_id] = {
        "palavra": palavra,
        "descoberta": descoberta,
        "erros": 0,
        "letras_usadas": []
    }
    return jsonify({"jogo_id": jogo_id, "descoberta": descoberta})

@app.route("/jogar", methods=["POST"])
def jogar():
    data = request.json
    jogo_id = data["jogo_id"]
    letra = data["letra"].lower()
    jogo = jogos[jogo_id]

    if letra not in jogo["letras_usadas"] and letra.isalpha():
        jogo["letras_usadas"].append(letra)
        if letra in jogo["palavra"].lower():
            for i, c in enumerate(jogo["palavra"].lower()):
                if c == letra:
                    jogo["descoberta"][i] = jogo["palavra"][i]
        else:
            jogo["erros"] += 1

    resultado = {
        "descoberta": jogo["descoberta"],
        "erros": jogo["erros"],
        "letras_usadas": jogo["letras_usadas"],
        "palavra": jogo["palavra"] if jogo["erros"] >= 6 or "_" not in jogo["descoberta"] else ""
    }
    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)
