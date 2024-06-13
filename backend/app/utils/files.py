import os
from werkzeug.utils import secure_filename

app_directory = "app"
file_directory = "files"


def get_upload_path(file_name: str):
    return os.path.join(app_directory, file_directory, file_name)


def get_result_file_name(task_id: str):
    return secure_filename(f"{task_id}-result.txt")


def get_input_file_name(task_id: str):
    return secure_filename(f"{task_id}.csv")


def get_generated_mock_file_name(task_id: str):
    return secure_filename(f"{task_id}.csv")
