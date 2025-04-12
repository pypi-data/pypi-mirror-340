from PIL import Image, ImageChops

def carregar_imagem(caminho_imagem):
    """
    Carrega uma imagem a partir do caminho fornecido.
    """
    try:
        return Image.open(caminho_imagem)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_imagem}")

def comparar_imagens_preto_branco(imagem1, imagem2):
    """
    Compara duas imagens e retorna uma nova imagem em preto e branco destacando as diferenças.
    """
    if imagem1.size != imagem2.size:
        raise ValueError("As imagens devem ter o mesmo tamanho para serem comparadas.")

    # Gerando a imagem com as diferenças
    imagem_diferenca = ImageChops.difference(imagem1, imagem2)

    # Convertendo para escala de cinza (preto e branco)
    imagem_preto_branco = imagem_diferenca.convert("L")

    return imagem_preto_branco

def salvar_imagem(imagem, caminho_saida):
    """
    Salva a imagem resultante em um arquivo.
    """
    imagem.save(caminho_saida)
    print(f"Imagem com as diferenças salva em: {caminho_saida}")