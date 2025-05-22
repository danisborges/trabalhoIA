# Detecção de Doenças em Plantas de Tomate

Este projeto é uma aplicação web desenvolvida com Flask que utiliza o modelo YOLOv8 para detectar doenças em plantas de tomate a partir de imagens. A aplicação permite que os usuários façam upload de imagens de folhas de tomate e retorna previsões sobre possíveis doenças.

## Equipe

David Marques
Gabriel Calil
Luis Ricardo
Marcos Hideki

## Funcionalidades

- **Upload de Imagem**: Os usuários podem fazer upload de uma imagem de uma folha de tomate.
- **Uso de camera**: Os usuários podem usar a camera pegando uma imagem de uma folha de tomate.
- **Predição de Doença**: A aplicação utiliza o modelo YOLOv8 para detectar e classificar doenças presentes na imagem.
- **Exibição de Resultados**: Os resultados são apresentados com a imagem original anotada com as predições e um gráfico de barras mostrando a confiança de cada predição.
- **Manuseio de Erros**: Se nenhuma predição for encontrada, a aplicação redireciona para uma página de erro informando o usuário.

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
