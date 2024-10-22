import json
from json.decoder import JSONDecodeError
import os
import sys

def is_numeric(value):
    return isinstance(value, (int, float))

def standardize_json(data):
    # Standardize the "Properties" field
    if data.get("Properties") is None:
        data["Properties"] = [{"property name": None, "headers": None, "data": None}]
    
    if isinstance(data["Properties"], dict):
        data["Properties"] = [data["Properties"]]
  
    for prop in data["Properties"]:
        
        try:
            headers = prop.get("headers")
        except Exception as e:
            headers = None

        if headers is not None and (len(headers) != 2 or not all(isinstance(h, str) for h in headers)):
            prop["headers"] = None

        try:
            property_name = prop.get("property name")
        except Exception as e:
            property_name = None
        if property_name is not None and not isinstance(property_name, str):
            prop["property name"] = "null"

        try:
            data_list = prop.get("data")
        except Exception as e:
            data_list = None
        if data_list is not None:
            standardized_data = []
            for item in data_list:
                if isinstance(item, (list, tuple)) and len(item) == 2:
                    if all(is_numeric(x) for x in item):
                        standardized_data.append(tuple(item))
                    else:
                        standardized_data = None
                        break
                else:
                    standardized_data = None
                    break
            prop["data"] = standardized_data

    return data




KEYS = ["Matrix Chemical Name", "Matrix Chemical Abbreviation", "Filler Chemical Name", "Filler Chemical Abbreviation", "Filler Composition Mass", "Filler Composition Volume", "Filler Particle Surface Treatment Chemical Name"]

def extract_json_objects(text):
    json_objects = []
    depth = 0
    start_index = 0
    inside_json = False

    for i, char in enumerate(text):
        if char == '{':
            if depth == 0:
                start_index = i
                inside_json = True
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0 and inside_json:
                json_objects.append(text[start_index:i+1])
                inside_json = False

    return json_objects

def parse_json_objects(json_objects):
    parsed_objects = []
    for obj in json_objects:
        try:
            # put null instead of ""
            obj = obj.replace('""', 'null')
            obj = obj.replace("(", '[')
            obj = obj.replace(")", ']')

            # delete everything between // and \n
            obj = obj.split("\n")
            obj = [line.split("//")[0] for line in obj]
            obj = "\n".join(obj)
            

            parsed = json.loads(obj)
            if not all(key in parsed for key in KEYS):
                continue
            parsed_objects.append(parsed)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            
            print("Invalid JSON object:", obj)
    return parsed_objects


def extract_and_standardize_json(folder, name_saved_folder):

    # Read the JSON files in the folder
    
    for jsons_per_article in os.listdir(folder):

        with open(os.path.join(folder, jsons_per_article), "r") as f:
            json_data = f.read()

            # Extract JSON objects from the text
            json_objects = extract_json_objects(json_data)

            # Parse the JSON objects
            parsed_objects = parse_json_objects(json_objects)

            # Standardize the JSON objects
            standardized_objects = [standardize_json(obj) for obj in parsed_objects]

            for i, obj in enumerate(standardized_objects):
                id_folder = jsons_per_article.split(".")[0]
                # if folder doesn't exist create it
                if not os.path.exists(os.path.join(name_saved_folder, id_folder)):
                    os.makedirs(os.path.join(name_saved_folder, id_folder))

                with open(os.path.join(name_saved_folder, id_folder, f"{i}.json"), "w") as f:
                    f.write(json.dumps(obj, indent=4))





if __name__ == "__main__":
    folder = sys.argv[1]
    name_saved_folder = sys.argv[2]
    extract_and_standardize_json(folder, name_saved_folder)              
                    

    
