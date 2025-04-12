from comparar_imagens import carregar_imagem, comparar_imagens_preto_branco, salvar_imagem
import os

# Caminhos para as imagens
diretorio = os.path.dirname(os.path.abspath(__file__))
caminho_imagem1 = os.path.join(diretorio, "img/img1.jpg")
caminho_imagem2 = os.path.join(diretorio, "img/img2.jpg")
caminho_saida = os.path.join(diretorio, "img/imagem_diferencas.png")

try:
    # Carregar as imagens
    imagem1 = carregar_imagem(caminho_imagem1)
    imagem2 = carregar_imagem(caminho_imagem2)

    # Comparar as imagens e gerar a imagem com as diferenças em preto e branco
    imagem_diferenca = comparar_imagens_preto_branco(imagem1, imagem2)

    # Salvar a imagem com as diferenças
    salvar_imagem(imagem_diferenca, caminho_saida)

    print("Imagem com as diferenças em preto e branco gerada com sucesso!")

except FileNotFoundError as e:
    print(f"Erro: {e}")
except ValueError as e:
    print(f"Erro: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")
