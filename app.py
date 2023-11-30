from flask import Flask, render_template, request, jsonify, url_for
import os
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import cv2
import requests

try:
    app = Flask(__name__)
    
    # Load the pre-trained model
    model = load_model('models/model.h5')
    
    UPLOAD_FOLDER = 'static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    def process_image(image_path):
        img = Image.open(image_path)
        img = img.resize((150, 150))
        img_array = np.array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array.astype(np.float32)
    
    @app.route('/')
    def home():
        return render_template('website.html', prediction=None)
    
    @app.route('/predict', methods=['POST'])
    def predict():
        if 'image' not in request.files:
            
            return "No image provided"
    
        image = request.files['image']
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_image.jpg')
        image.save(image_path)
    
        image = cv2.imread(image_path)
        image = cv2.resize(image, (150, 150))
        img1 = image
        image = image.astype('float32') / 255
        image = np.expand_dims(image, axis=0)
    
        predictions = model.predict(image)
        predicted_class = np.argmax(predictions)
    
        class_names = ['stem cracking', 'Stem_bleeding', 'Healthy_Leaf', 'yellow leaf disease', 'healthy_foot', 'Healthy_Trunk', 'Mahali_Koleroga', 'bud borer', 'Healthy_Nut']
        predicted_disease = class_names[predicted_class]
    
        highlighted_disease = f"<strong>{predicted_disease}</strong>"
    
        print("Predicted Disease:", highlighted_disease)
        print("Class Probabilities:", predictions)
    
        # Save the uploaded image to the static/uploads folder
        static_image_path = os.path.join('static', 'uploads', 'input_image.jpg')
        cv2.imwrite(static_image_path, img1)
    
        # Pass the prediction result to the HTML template
        if predicted_disease == 'stem cracking':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP='Stem', prediction=predicted_disease, ME='Improve drainage, Apply potash fertilizers. Spray Borax (0.2 per cent) in the early stage. Protect palms from sun scorch. Cover green portions of the stem with areca leaf sheaths or opaque polythene film. Root feed with Tridemorph 5ml in 100 ml water. thrice a year, Provide shade during summer months')
        elif predicted_disease == 'Stem_bleeding':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP='Stem', prediction=predicted_disease, ME='Improve drainage. Root feeding. Apply neem cake. Apply fungicide and tar. Apply hexaconazole. Apply coal tar')
        elif predicted_disease == 'Healthy_Leaf':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP='Leaf', prediction=predicted_disease, ME='No measures required the leaf is healthy')
        elif predicted_disease == 'healthy_foot':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP = 'Foot', prediction = predicted_disease, ME = 'No measures required the foot is healthy')
        elif predicted_disease == 'Healthy_Trunk':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP = 'Trunk', prediction = predicted_disease, ME = 'No measures required the stem is healthy')
        elif predicted_disease == 'Healthy_Nut':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP = 'Fruit/Nut', prediction = predicted_disease, ME = 'No measures required the fruit/nut is healthy')
        elif predicted_disease == 'yellow leaf disease':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP = 'Leaf', prediction = predicted_disease, ME = 'Remove and burn infected leaves, dried bunches, and inflorescences. Spray mancozeb (3 gil) when female flowers open, and then again after 20–25 days. You can also spray Bordeaux mixture (1%) or Dithane M-45 (3g/liter of water) when female flowers open. Apply 1 kg of superphosphate per palm, alone or with 1 kg of lime. You can also apply 12 kg of compost and green leaf per palm. Treat affected palm basins with 1.5% calixin. You can also apply 1.5–2.0 kg of neem cake per palm.')
        elif predicted_disease == 'Mahali_Koleroga':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'), POP = 'Fruit/Nut', prediction = predicted_disease, ME = 'Spray with Bordeaux mixture: Spray the bunches with a 1% Bordeaux mixture before the monsoon. Spray again after 45 days. If the monsoon lasts longer, spray a third time. Use Metalaxyl MZ: This treatment has been found to be effective. Cleanliness and sanitation: Destroy diseased tree tops and plant parts. ')
        elif predicted_disease == 'bud borer':
            return render_template('website.html',photo=url_for('static', filename='uploads/input_image.jpg'),POP = ' Bud', prediction = predicted_disease, ME = 'Removing infected dried bunches. Spraying mancozeb. Spraying Carbendazim + Mancozeb')
        
        return render_template('website.html', prediction=predicted_disease)
    
    
    @app.route('/get_weather', methods=['POST'])
    def get_weather():
        city = request.form.get('city')
    
        if not city:
            return jsonify({'error': 'City not provided'}), 400
    
        api_key = 'eace5001df19d0b57f6e7eb7634be99d'
        weather_api_url = f'http://api.weatherstack.com/current?access_key={api_key}&query={city}'
    
        try:
            response = requests.get(weather_api_url)
            data = response.json()
    
            if 'current' in data:
                temp = data['current']['temperature']
                humi = data['current']['humidity']
                result = {'location': data['location']['name'], 'temperature': temp, 'humidity': humi}
                return jsonify(result)
    
            return jsonify({'error': 'Data not available for the specified location'}), 404
    
        except Exception as e:
            print('Error:', e)
            return jsonify({'error': 'Error fetching data'}), 500
    
    
    
    if __name__ == '__main__':
        app.run(debug=True)


except Exception as e:
    app.logger.error(f"An error occurred: {str(e)}")
    return "Internal Server Error", 500
