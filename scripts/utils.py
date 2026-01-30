import json

def load_checklist(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        
    return dict(data)