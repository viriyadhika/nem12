from .utils.files import get_generated_mock_file_name, get_upload_path
from .sql_generator import get_sql_from_nim12, generate_nmi_details
import argparse
import uuid

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run task", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("command", help='Either "perf_test", ""')
    argument = vars(parser.parse_args())

    print(f"Running command with {argument}")

    try:
        command = argument["command"]
        if command == "perf_test":
            task_id = str(uuid.uuid4())
            generate_nmi_details(
                10000, get_upload_path(get_generated_mock_file_name(task_id))
            )
            get_sql_from_nim12(task_id)
    except KeyboardInterrupt:
        pass
