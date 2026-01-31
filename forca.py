import random

# Lista de palavras para o jogo
palavras = ["python", "programa", "desafio", "jogo", "computador"]

# Escolhe uma palavra aleatória
palavra = random.choice(palavras)
letras_descobertas = ["_"] * len(palavra)
tentativas = 6  # número de chances
letras_usadas = []

print("Bem-vindo ao jogo da Forca!")

# Loop principal do jogo
while tentativas > 0 and "_" in letras_descobertas:
    print("\nPalavra:", " ".join(letras_descobertas))
    print("Tentativas restantes:", tentativas)
    print("Letras usadas:", ", ".join(letras_usadas))
    
    letra = input("Digite uma letra: ").lower()
    
    if letra in letras_usadas:
        print("Você já tentou essa letra!")
        continue

    letras_usadas.append(letra)

    if letra in palavra:
        for i, l in enumerate(palavra):
            if l == letra:
                letras_descobertas[i] = letra
        print("Boa! Você acertou uma letra.")
    else:
        tentativas -= 1
        print("Ops! Letra errada.")

# Resultado do jogo
if "_" not in letras_descobertas:
    print("\nParabéns! Você ganhou! A palavra era:", palavra)
else:
    print("\nVocê perdeu! A palavra era:", palavra)
