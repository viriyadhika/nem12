from flask import Flask, request, send_from_directory

from app.sql_generator import get_sql_from_nim12, generate_nmi_details
from app.db import execute_sql
from .initialize import run

from app.utils.files import (
    get_generated_mock_file_name,
    get_input_file_name,
    get_result_file_name,
    get_upload_path,
    file_directory,
)
from .utils.env import SECRET_KEY
from flask_cors import CORS
from uuid import uuid4

app = Flask(__name__)
CORS(app)
app.config.from_mapping(SECRET_KEY=SECRET_KEY)

run()


@app.route("/generate-file", methods=["POST"])
def generate_file():
    json = request.get_json()
    size = json.get("size")
    task_id = uuid4()
    generate_nmi_details(size, get_upload_path(get_generated_mock_file_name(task_id)))

    return {"task_id": task_id}


@app.route("/get-mock-result/<path:task_id>", methods=["GET"])
def get_mock_result(task_id: str):
    if request.method == "GET":
        file_name = get_generated_mock_file_name(task_id)

        return send_from_directory(file_directory, file_name)


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        # upload file flask
        f = request.files.get("file")

        task_id = uuid4()
        file_name = get_input_file_name(task_id)
        f.save(get_upload_path(file_name))

        get_sql_from_nim12(task_id)

        return {"result": "success", "task_id": task_id}


@app.route("/get-result/<path:task_id>", methods=["GET"])
def get_result(task_id: str):
    if request.method == "GET":
        file_name = get_result_file_name(task_id)

        return send_from_directory(file_directory, file_name)


@app.route("/execute-sql", methods=["POST"])
def execute():
    json = request.get_json()
    task_id = json.get("task_id")
    if request.method == "POST":
        with open(get_upload_path(get_result_file_name(task_id))) as file:
            f = file.read()
            execute_sql.run(f.split("\n"))
            return {"result": "success"}
