from PIL import Image
import os

# Função para recortar imagens mantendo a maior resolução possível
def recortar_imagens(pasta_entrada, pasta_saida, tamanho_minimo=(256, 256)):
    # Verificar se a pasta de saída existe, se não, criar
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Listar arquivos na pasta de entrada
    arquivos = os.listdir(pasta_entrada)

    # Percorrer os arquivos na pasta de entrada
    for arquivo in arquivos:
        # Verificar se é um arquivo de imagem
        if arquivo.endswith('.jpg') or arquivo.endswith('.jpeg') or arquivo.endswith('.png'):
            # Abrir a imagem
            try:
                caminho_completo = os.path.join(pasta_entrada, arquivo)
                imagem = Image.open(caminho_completo)
                largura_original, altura_original = imagem.size
            except Exception as e:
                print(f"Erro ao abrir {arquivo}: {e}")
                continue

            # Calcular proporção de redimensionamento
            proporcao_largura = tamanho_minimo[0] / largura_original
            proporcao_altura = tamanho_minimo[1] / altura_original
            proporcao = max(proporcao_largura, proporcao_altura)

            # Calcular novo tamanho com base na maior resolução possível
            largura_nova = int(largura_original * proporcao)
            altura_nova = int(altura_original * proporcao)

            # Redimensionar a imagem
            imagem_redimensionada = imagem.resize((largura_nova, altura_nova), Image.LANCZOS)

            # Recortar para o tamanho mínimo especificado
            left = (largura_nova - tamanho_minimo[0]) / 2
            top = (altura_nova - tamanho_minimo[1]) / 2
            right = (largura_nova + tamanho_minimo[0]) / 2
            bottom = (altura_nova + tamanho_minimo[1]) / 2

            imagem_recortada = imagem_redimensionada.crop((left, top, right, bottom))

            # Salvar a imagem recortada na pasta de saída
            try:
                caminho_saida = os.path.join(pasta_saida, f"recortada_{arquivo}")
                imagem_recortada.save(caminho_saida)
                print(f"Imagem {arquivo} recortada e salva com sucesso.")
            except Exception as e:
                print(f"Erro ao salvar {arquivo} recortada: {e}")

# Exemplo de uso
if __name__ == "__main__":
     pasta_entrada = "/home/hideki/Documents/fatec/rena/dataset/aplication/static/images/banner"
     pasta_saida = "/home/hideki/Documents/fatec/rena/dataset/aplication/static/images/cort"
     tamanho_minimo_recorte = (256, 256)

     recortar_imagens(pasta_entrada, pasta_saida, tamanho_minimo_recorte)
