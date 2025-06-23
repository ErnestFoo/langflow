import json
import os
from pathlib import Path


class JSONFileReader:
    def __init__(self):
        self._file_path = ""
        self._is_file_path_set = False
        self._set_file_path("/workspace/src/frontend/public/example.json")  # Default file path


    def safe_read(self):
        if not Path(self.file_path).exists():
            print(f"Error: File '{self.file_path}' does not exist.")
            return None
        if not self._is_file_path_set:
            print("Error: File path is not set.")
            return None
        try:
            with Path.open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
            
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        
        except Exception as e:
            print(f"Unexpected error while reading file: {e}")
        return None
    
    def _set_file_path(self, new_path):
        if not isinstance(new_path, str):
            raise ValueError("File path must be a string.")
        self.file_path = new_path
        self._is_file_path_set = True

    def _is_file_path_set(self):
        return self._is_file_path_set

if __name__ == "__main__":
    path = Path("/workspace/src/backend/base/langflow/")  # or any specific path like Path("/home/user/documents")

    # List all files (not directories)
    files = [f for f in path.iterdir() if f.is_file()]

    # Print file names
    for file in files:
        print(file.name)

    print("Current working directory (os):", os.getcwd())
    print("Current working directory (Path):", Path.cwd())
    # Example usage
    reader = JSONFileReader()

    data = reader.safe_read()
    if data is not None:
        print("JSON data:", data)
    else:
        print("Failed to read JSON data.")