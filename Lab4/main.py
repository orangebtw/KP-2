from flask import Flask, jsonify, request, render_template
from PIL import Image, UnidentifiedImageError
import io

app = Flask(__name__,
            static_folder="./static/",
            template_folder="./web/templates/")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return jsonify({"author": "158365"})

@app.route("/size2json", methods=["POST"])
def size2json():
    if "image" not in request.files:
        return jsonify({"result": "image file is required"})
    image = request.files["image"]
    try:
        data = io.BytesIO(image.read())
        opened_image = Image.open(data, formats=("PNG",))
    except UnidentifiedImageError as e:
        print(e)
        return jsonify({"result": "invalid filetype"})
    size = opened_image.size
    return jsonify({"width": size[0], "height": size[1]})

if __name__ == "__main__":
    app.run()
