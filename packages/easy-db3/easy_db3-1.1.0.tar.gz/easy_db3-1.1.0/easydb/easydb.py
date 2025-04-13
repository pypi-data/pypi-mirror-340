import os

class Database:
    def __init__(self, file_path):
        self.file_path = file_path
        self._data = {}
        self._use_categories = True

    def storage(self, *args, category=None):
        if category:
            if category not in self._data or not isinstance(self._data.get(category), dict):
                self._data[category] = {}
            for item in args:
                if ": " in item:
                    key, value = item.split(": ", 1)
                    self._data[category][key.strip()] = value.strip()
        else:
            for item in args:
                if ": " in item:
                    key, value = item.split(": ", 1)
                    self._data[key.strip()] = value.strip()
        self._save()

    def _save(self):
        with open(self.file_path, "w") as file:
            for key, value in self._data.items():
                if isinstance(value, dict):
                    file.write(f"[{key}]\n")
                    for subkey, subvalue in value.items():
                        file.write(f"{subkey}: {subvalue}\n")
                else:
                    file.write(f"{key}: {value}\n")

    def load(self):
        if not os.path.exists(self.file_path):
            return

        self._data = {}
        current_category = None

        with open(self.file_path, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("[") and line.endswith("]"):
                    current_category = line[1:-1]
                    self._data[current_category] = {}
                elif ": " in line:
                    key, value = line.split(": ", 1)
                    if current_category:
                        self._data[current_category][key.strip()] = value.strip()
                    else:
                        self._data[key.strip()] = value.strip()

    def get_data(self, key=None, category=None):
        if category and self._use_categories:
            if key:
                return self._data.get(category, {}).get(key)
            return self._data.get(category)
        elif key:
            return self._data.get(key)
        return None

    def del_data(self, key=None, category=None):
        """Delete data by key and optional category."""
        if category and self._use_categories:
            if key:
                if key in self._data.get(category, {}):
                    del self._data[category][key]
                    print(f"Deleted {key} from {category}")
                else:
                    print(f"Key {key} not found in category {category}")
            else:
                if category in self._data:
                    del self._data[category]
                    print(f"Deleted entire category: {category}")
                else:
                    print(f"Category {category} not found")
        elif key:
            if key in self._data:
                del self._data[key]
                print(f"Deleted {key}")
            else:
                print(f"Key {key} not found")
        else:
            print("No key or category provided for deletion")

        self._save()