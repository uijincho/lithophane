from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from lithophane_generator import generate_lithophane
import os
import tempfile

app = Flask(__name__)
CORS(app)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image = request.files['image']
        params = request.form.to_dict()

        # Save uploaded image to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image.filename)[-1]) as temp_image_file:
            image.save(temp_image_file.name)
            temp_image_path = temp_image_file.name

        # Call your lithophane generator and get STL path
        stl_path = generate_lithophane(temp_image_path, params)

        return send_file(stl_path, as_attachment=True, download_name="lithophane.stl")

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Let Render assign the port (important!)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
