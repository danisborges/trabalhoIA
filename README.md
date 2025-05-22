# Detecção de Doenças em folhas do Tomate

## Equipe

Danielli Borges \
Ricardo Alexandre

## Funcionalidades

- **Upload de Imagem**: Os usuários podem fazer upload de uma imagem de uma folha de tomate.
- **Predição de Doença**: A aplicação utiliza o modelo YOLOv8 para detectar e classificar doenças presentes na imagem.
- **Exibição de Resultados**: Os resultados são apresentados com a imagem original anotada com as predições e um gráfico de barras mostrando a confiança de cada predição.

## Pré-requisitos

- Python 3.11
- Flask
- PIL (Python Imaging Library)
- ultralytics (para o modelo YOLOv8)
- Chart.js (para gráficos)

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/Marcossakaguchi5/ai
   cd ai

## Iniciar a aplicação Flask
    
```bash
  python app.py
