from flask import Flask, request, send_file
from rembg import remove
from io import BytesIO
from PIL import Image
from flask import render_template
import os
from flask import Flask, send_from_directory


app = Flask(__name__)

class ObjectImage:
    def __init__(self, image_data):
        self.image_data = image_data
        self.image = self.process_image(image_data)
        self.x = 0
        self.y = 0
        self.width = 500  # Set initial width
        self.height = 500  # Set initial height

    def process_image(self, image_data):
        # Image processing code (e.g., background removal) here
        img = Image.open(BytesIO(image_data))
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] > 220 and item[1] > 220 and item[2] > 220:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        return img

object_images = []

@app.route('/', methods=['GET'])
def home():
    return render_template('1004.html')

@app.route('/removebg', methods=['POST'])
def remove_bg():
    if 'image' not in request.files:
        return 'No image provided', 400

    image = request.files['image'].read()
    no_bg_image = remove(image)

    img = ObjectImage(no_bg_image)  # Create an ObjectImage instance
    object_images.append(img)

    return str(len(object_images))  # Return the index of the added image

@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
