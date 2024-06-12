from flask import Flask, request, session
from werkzeug.utils import secure_filename
import os
from .utils.env import SECRET_KEY
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_mapping(SECRET_KEY=SECRET_KEY)


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        # upload file flask
        f = request.files.get("file")

        # Extracting uploaded file name
        data_filename = secure_filename(f.filename)

        f.save("app/files/flask.csv")

        session["uploaded_data_file_path"] = os.path.join("app/files/flask.csv")
        return {"result": "success"}
