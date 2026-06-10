from flask import Flask, request, jsonify, send_file, render_template_string
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

UPLOAD_FOLDER = "/tmp/images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =======================
# /login
# =======================
@app.route("/login", methods=["GET"])
def login():
    return jsonify({"author": "158365"})


# =======================
# HTML шаблоны
# =======================

MAKEIMAGE_HTML = """
<!DOCTYPE html>
<html>
<body>
<h2>Create Image</h2>
{% if message %}
<p style="color:red;">{{ message }}</p>
{% endif %}
<form method="POST" enctype="application/x-www-form-urlencoded">
  Width: <input type="text" name="width"><br>
  Height: <input type="text" name="height"><br>
  Text: <input type="text" name="text"><br>
  <button type="submit">Create</button>
</form>
</body>
</html>
"""

UPLOAD_HTML = """
<!DOCTYPE html>
<html>
<body>
<h2>Upload Image</h2>
{% if message %}
<p style="color:red;">{{ message }}</p>
{% endif %}
<form method="POST" enctype="multipart/form-data">
  Name: <input type="text" name="name"><br>
  File: <input type="file" name="file"><br>
  <button type="submit">Upload</button>
</form>
</body>
</html>
"""

# =======================
# /makeimage
# =======================

@app.route("/makeimage", methods=["GET", "POST"])
def make_image():
    if request.method == "GET":
        return render_template_string(MAKEIMAGE_HTML)

    width = request.form.get("width")
    height = request.form.get("height")
    text = request.form.get("text", "")

    # Валидация
    try:
        width = int(width)
        height = int(height)

        if width <= 0 or height <= 0 or width > 2000 or height > 2000:
            raise ValueError()

    except:
        return render_template_string(MAKEIMAGE_HTML, message="Invalid image size")

    # Создание изображения
    img = Image.new("RGB", (width, height), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)

    # Простейший текст по центру
    try:
        font = ImageFont.load_default()
    except:
        font = None

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    x = (width - text_width) // 2
    y = (height - text_height) // 2

    draw.text((x, y), text, fill=(0, 0, 0), font=font)

    # Сохранение в память
    img_io = io.BytesIO()
    img.save(img_io, "JPEG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/jpeg")


# =======================
# /load_image
# =======================

@app.route("/load_image", methods=["GET", "POST"])
def load_image():
    if request.method == "GET":
        return render_template_string(UPLOAD_HTML)

    file = request.files.get("file")
    name = request.form.get("name")

    if not file:
        return render_template_string(UPLOAD_HTML, message="No file selected")

    if not name:
        name = file.filename

    filepath = os.path.join(UPLOAD_FOLDER, name)

    if os.path.exists(filepath):
        return render_template_string(UPLOAD_HTML, message="File already exists")

    file.save(filepath)

    return f"Uploaded: {name}"


# =======================
# /images
# =======================

@app.route("/images", methods=["GET"])
def images():
    files = os.listdir(UPLOAD_FOLDER)

    html = "<h2>Images</h2><div style='display:flex;flex-wrap:wrap;'>"

    for f in files:
        path = f"/tmp/images/{f}"
        html += f"""
        <div style="margin:10px;">
            <img src="/get_image/{f}" width="150"><br>
            {f}
        </div>
        """

    html += "</div>"
    return html


# =======================
# отдача файлов
# =======================

@app.route("/get_image/<filename>")
def get_image(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path)


# =======================
# запуск
# =======================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
