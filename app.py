from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
import logging
from PIL import Image, ImageDraw
from ultralytics import YOLO

# Initialize the Flask app
app = Flask(__name__)

# Configure upload directory
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the YOLOv8 model
try:
    model = YOLO('tomate.pt')
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    model = None

# Define summaries for each class
class_summaries = {
    'Early Blight': """
<strong>Requeima Precoce (Early Blight)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Manchas concêntricas marrons a negras nas folhas, que eventualmente levam à necrose. As lesões podem se unir, causando desfolha prematura. Em casos graves, manchas escuras aparecem em caules e frutos.
<br><br>
<strong>Danos Econômicos:</strong><br>
Pode reduzir drasticamente a produção e qualidade dos frutos, levando a perdas significativas.
<br><br>
<strong>Causador:</strong><br>
Fungos do gênero <em>Alternaria</em> (principalmente <em>Alternaria solani</em>).
<br><br>
<strong>Prevenção:</strong><br>
Uso de variedades resistentes, prática de rotação de culturas, eliminação de restos de plantas infectadas, espaçamento adequado para melhorar a circulação de ar.
<br><br>
<strong>Controle:</strong><br>
Aplicação de fungicidas como mancozebe, clorotalonil e produtos à base de cobre, remoção de plantas infectadas e melhoria nas práticas de irrigação para evitar molhamento excessivo das folhas.
""",

    'Healthy': """
<strong>Tomate Saudável (Healthy)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Folhas verde-escuras, sem manchas ou deformações, crescimento vigoroso e produção uniforme de frutos.
<br><br>
<strong>Danos Econômicos:</strong><br>
Nenhum.
<br><br>
<strong>Causador:</strong><br>
Boa saúde das plantas resultante de práticas agrícolas adequadas.
<br><br>
<strong>Prevenção:</strong><br>
Manutenção de boas práticas agrícolas, incluindo o uso de sementes certificadas e tratadas, controle de irrigação e fertilização balanceada.
<br><br>
<strong>Controle:</strong><br>
Monitoramento contínuo, manejo integrado de pragas e doenças, e práticas culturais adequadas.
""",

    'Late Blight': """
<strong>Requeima Tardia (Late Blight)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Manchas escuras e encharcadas nas folhas, que se tornam marrons e necróticas. Frutos desenvolvem lesões duras e de cor marrom. Em condições úmidas, pode-se observar uma camada branca de esporos na superfície inferior das folhas.
<br><br>
<strong>Danos Econômicos:</strong><br>
Pode devastar plantações inteiras rapidamente se não controlada, resultando em perdas de 100% em casos severos.
<br><br>
<strong>Causador:</strong><br>
<em>Phytophthora infestans</em>.
<br><br>
<strong>Prevenção:</strong><br>
Plantio de variedades resistentes, escolha de locais bem drenados, rotação de culturas, e eliminação de restos de plantas após a colheita.
<br><br>
<strong>Controle:</strong><br>
Aplicação de fungicidas específicos como metalaxil, cimoxanil, e fosetil-Al, remoção de plantas infectadas e controle rigoroso de irrigação para reduzir a umidade excessiva.
""",

    'Leaf Miner': """
<strong>Minadora (Leaf Miner)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Presença de galerias sinuosas e transparentes nas folhas, causadas pelas larvas que se alimentam do tecido foliar.
<br><br>
<strong>Danos Econômicos:</strong><br>
A redução da área foliar funcional pode comprometer a fotossíntese, diminuindo o vigor da planta e, consequentemente, a produção de frutos.
<br><br>
<strong>Causador:</strong><br>
Larvas de pequenas moscas da família Agromyzidae (gênero <em>Liriomyza</em>).
<br><br>
<strong>Prevenção:</strong><br>
Uso de coberturas vegetais para proteger as plantas jovens, controle biológico com parasitoides como <em>Diglyphus isaea</em>.
<br><br>
<strong>Controle:</strong><br>
Aplicação de inseticidas como abamectina e espinosade, monitoramento e remoção manual das folhas infestadas.
""",

    'Leaf Mold': """
<strong>Mofo das Folhas (Leaf Mold)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Manchas amarelas na superfície superior das folhas, que se tornam marrons com o tempo. Na superfície inferior, desenvolve-se um mofo cinza a roxo.
<br><br>
<strong>Danos Econômicos:</strong><br>
Pode causar desfolha severa, resultando em redução significativa da produção de frutos.
<br><br>
<strong>Causador:</strong><br>
Fungos do gênero <em>Fulvia</em> (<em>Fulvia fulva</em>).
<br><br>
<strong>Prevenção:</strong><br>
Plantio em áreas com boa ventilação, espaçamento adequado entre plantas e redução da umidade relativa no ambiente de cultivo.
<br><br>
<strong>Controle:</strong><br>
Aplicação de fungicidas como clorotalonil e produtos à base de cobre, remoção de folhas afetadas e manutenção de boas práticas de irrigação.
""",

    'Mosaic Virus': """
<strong>Vírus do Mosaico (Mosaic Virus)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Folhas apresentam manchas amareladas e verdes, aspecto mosqueado e distorção do crescimento. Frutos podem ser menores e deformados.
<br><br>
<strong>Danos Econômicos:</strong><br>
Redução significativa do crescimento vegetativo e da produção de frutos, afetando a qualidade e quantidade da colheita.
<br><br>
<strong>Causador:</strong><br>
Diversos vírus, incluindo <em>Tomato mosaic virus (ToMV)</em> e <em>Tobacco mosaic virus (TMV)</em>.
<br><br>
<strong>Prevenção:</strong><br>
Uso de sementes livres de vírus, desinfecção de ferramentas e equipamentos, controle rigoroso de vetores como pulgões.
<br><br>
<strong>Controle:</strong><br>
Remoção e destruição de plantas infectadas, controle de vetores com inseticidas, e uso de barreiras físicas para impedir a disseminação.
""",

    'Septoria': """
<strong>Septoriose (Septoria)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Pequenas manchas circulares marrons com bordas escuras nas folhas inferiores. As manchas aumentam e podem coalescer, causando a queda das folhas.
<br><br>
<strong>Danos Econômicos:</strong><br>
Desfolha intensa pode levar a reduções significativas na produtividade, devido à diminuição da área foliar funcional.
<br><br>
<strong>Causador:</strong><br>
Fungos do gênero <em>Septoria</em> (<em>Septoria lycopersici</em>).
<br><br>
<strong>Prevenção:</strong><br>
Rotação de culturas, uso de variedades resistentes, eliminação de restos de cultura e espaçamento adequado para melhorar a circulação de ar.
<br><br>
<strong>Controle:</strong><br>
Aplicação de fungicidas como mancozebe e clorotalonil, remoção de folhas infectadas e melhoria das práticas de irrigação.
""",

    'Spider Mites': """
<strong>Ácaros-Aranha (Spider Mites)</strong>
<br><br>
<strong>Sintomas:</strong><br>
Pequenos pontos amarelos nas folhas, que eventualmente ficam bronzeadas e secas. Pode haver presença de teias finas na parte inferior das folhas.
<br><br>
<strong>Danos Econômicos:</strong><br>
Redução da saúde da planta e da produção de frutos, especialmente em condições de alta infestação.
<br><br>
<strong>Causador:</strong><br>
Ácaros da família Tetranychidae (principalmente <em>Tetranychus urticae</em>).
<br><br>
<strong>Prevenção:</strong><br>
Manutenção da umidade adequada, monitoramento regular e uso de cultivares resistentes.
<br><br>
<strong>Controle:</strong><br>
Aplicação de acaricidas como abamectina e bifentrina, uso de predadores naturais como <em>Phytoseiulus persimilis</em>, e lavagem das plantas com água para reduzir a população de ácaros.
""",
    'Yellow Leaf Curl Virus': """ 
   <strong> Vírus do Enrolamento Amarelo do Tomateiro </strong>(Yellow Leaf Curl Virus)
    <br><br>
    <strong>Sintomas:</strong><br>
    Folhas jovens apresentam enrolamento, amarelecimento e crescimento atrofiado. Plantas ficam atrofiadas e produzem poucos frutos.
    <br><br>
    <strong>Danos Econômicos:</strong><br>
    Redução significativa na produção de frutos, afetando gravemente a rentabilidade da cultura.
    <br><br>
    <strong>Causador:</strong><br>
    Vírus transmitido por moscas-brancas (<em>Bemisia tabaci</em>).
    <br><br>
    <strong>Prevenção:</strong><br>
    Uso de variedades resistentes, controle das populações de moscas-brancas e instalação de barreiras físicas como telas anti-insetos.
    <br><br>
    <strong>Controle:</strong><br>
    Aplicação de inseticidas como imidacloprido e piriproxifeno, manejo integrado de pragas (MIP) para controle das moscas-brancas, e eliminação de plantas hospedeiras alternativas que possam servir de refúgio para o vírus.
    """
}

# Add the summaries to the context passed to the template
def predict(image_path):
    try:
        img = Image.open(image_path)
        results = model(img)

        predictions = []
        draw = ImageDraw.Draw(img)
        for result in results:
            for detection in result.boxes.data.tolist():
                class_id = int(detection[5])
                prediction = {
                    'class': model.names[class_id],
                    'confidence': detection[4],
                    'box': detection[:4]
                }
                predictions.append(prediction)
                
                # Draw all bounding boxes
                box = detection[:4]
                draw.rectangle([box[0], box[1], box[2], box[3]], outline="red", width=2)
                draw.text((box[0], box[1]), f"{model.names[class_id]}: {detection[4]:.2f}", fill="red")

        # Save the image with bounding boxes
        output_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'classified_' + os.path.basename(image_path))
        img.save(output_image_path)

        if not predictions:
            raise ValueError("No predictions found.")

        # Find the highest confidence prediction for each class
        best_predictions = {}
        for prediction in predictions:
            class_name = prediction['class']
            if class_name not in best_predictions or prediction['confidence'] > best_predictions[class_name]['confidence']:
                best_predictions[class_name] = prediction

        logging.debug(f"Best Predictions: {best_predictions}")
        return best_predictions, output_image_path, class_summaries
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return None, None, None

# Route for image upload
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            best_predictions, output_image_path, summaries = predict(filename)
            if best_predictions:
                return render_template('result.html', best_predictions=best_predictions, image_path=output_image_path, summaries=summaries)
            else:
                return redirect(url_for('error'))

    return render_template('index.html')

# Route to serve the classified image
@app.route('/uploads/<filename>')
def send_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route for handling errors
@app.route('/error')
def error():
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)