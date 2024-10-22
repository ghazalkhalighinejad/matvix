
import json
from json.decoder import JSONDecodeError
import os
import sys

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
            obj = obj.replace('""', 'null')
            obj = obj.replace("(", '[')
            obj = obj.replace(")", ']')

            obj = obj.split("\n")
            obj = [line.split("//")[0] for line in obj]
            obj = "\n".join(obj)
            

            parsed = json.loads(obj)
            parsed_objects.append(parsed)
        except json.JSONDecodeError as e:
            print("JSONDecodeError:", e)
            
            print("Invalid JSON object:", obj)
    return parsed_objects







                    
                    

    
