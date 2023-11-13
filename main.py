import io
import sys
import flake8.main.application
import os
from rich import print
from dotenv import load_dotenv

class FakeFile(io.StringIO):
    def __init__(self):
        super().__init__()
        self.buffer = self

    def write(self, s):
        if isinstance(s, bytes):
            # Decode bytes to a string and write
            s = s.decode('utf-8')
        super().write(s)

    def getvalue(self):
        return super().getvalue()




def flake8_to_dict(path_to_code):
    base_dir = os.path.commonpath([path_to_code])
    
    # Temporary redirect stdout to the custom FakeFile
    original_stdout = sys.stdout
    sys.stdout = FakeFile()

    # Initialize and run flake8
    app = flake8.main.application.Application()
    app.initialize([
        '--exclude=venv,.venv,your_project/external_packages,*/site-packages/*',
        path_to_code
    ])
    app.run_checks()
    app.report()

    # Capture and restore stdout
    flake8_output = sys.stdout.getvalue()
    sys.stdout = original_stdout

    # Parse the flake8 output
    results = {}
    for line in flake8_output.strip().split('\n'):
        if line:  # Ensure the line is not empty
            file, line_no, col_no, msg = line.split(':', 3)
            # Remove base directory from file path
            relative_path = os.path.relpath(file, base_dir)
            error_code = msg.strip().split(' ')[0]
            results.setdefault(relative_path, []).append({
                'line': int(line_no),
                'column': int(col_no),
                'error_code': error_code,
                'message': msg.strip()
            })

    return results


# Example usage
load_dotenv()
report = flake8_to_dict(os.getenv("DIR"))
print(report)
