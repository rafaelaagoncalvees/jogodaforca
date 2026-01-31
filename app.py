from flask import Flask, render_template, request, jsonify
import random
import os

app = Flask(__name__)

# ----------------------------------------
# Lê as palavras do ficheiro palavras.txt
# ----------------------------------------
with open("palavras.txt", "r", encoding="utf-8") as f:
    palavras = [linha.strip() for linha in f if linha.strip()]

# Guarda os jogos ativos em memória
jogos = {}

# ----------------------------------------
# Página principal
# ----------------------------------------
@app.route("/")
def index():
    return render_template("index.html")

# ----------------------------------------
# Criar um novo jogo
# ----------------------------------------
@app.route("/novo_jogo", methods=["POST"])
def novo_jogo():
    # Gera um ID aleatório para o jogo
    jogo_id = str(random.randint(1000, 9999))

    # Escolhe uma palavra aleatória
    palavra = random.choice(palavras)

    # Cria a palavra descoberta (underscore "_" para letras)
    descoberta = [c if c == " " else "_" for c in palavra]

    # Guarda o estado do jogo
    jogos[jogo_id] = {
        "palavra": palavra,
        "descoberta": descoberta,
        "erros": 0,
        "letras_usadas": []
    }

    return jsonify({
        "jogo_id": jogo_id,
        "descoberta": descoberta
    })

# ----------------------------------------
# Jogar uma letra
# ----------------------------------------
@app.route("/jogar", methods=["POST"])
def jogar():
    data = request.json
    jogo_id = data["jogo_id"]
    letra = data["letra"].lower()

    jogo = jogos.get(jogo_id)

    if not jogo:
        return jsonify({"erro": "Jogo não encontrado"}), 400

    # Verifica se a letra é válida e ainda não usada
    if letra.isalpha() and letra not in jogo["letras_usadas"]:
        jogo["letras_usadas"].append(letra)

        # Se a letra existir na palavra
        if letra in jogo["palavra"].lower():
            for i, c in enumerate(jogo["palavra"].lower()):
                if c == letra:
                    jogo["descoberta"][i] = jogo["palavra"][i]
        else:
            jogo["erros"] += 1

    # Se perdeu ou ganhou, revela a palavra
    palavra_final = ""
    if jogo["erros"] >= 6 or "_" not in jogo["descoberta"]:
        palavra_final = jogo["palavra"]

    return jsonify({
        "descoberta": jogo["descoberta"],
        "erros": jogo["erros"],
        "letras_usadas": jogo["letras_usadas"],
        "palavra": palavra_final
    })

# ----------------------------------------
# Inicialização do servidor
# ----------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
