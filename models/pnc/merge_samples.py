import json
import os

import sys

# append /usr/project/xtmp/gk126/nlp-for-materials/bench/modeling/pnc to sys.path
sys.path.append("/usr/project/xtmp/gk126/nlp-for-materials/bench/modeling/pnc")

from standardize_prediction import extract_json_objects, parse_json_objects, standardize_json

def merge_json_files(json_files):
    merged_data = {}

    for json_file in json_files:

        data = json_file
        key = tuple(
            str(data[attr])
            for attr in [
                "Matrix Chemical Name",
                "Matrix Chemical Abbreviation",
                "Filler Chemical Name",
                "Filler Chemical Abbreviation",
                "Filler Composition Mass",
                "Filler Composition Volume",
                "Filler Particle Surface Treatment Chemical Name"
            ]
        )


        if key in merged_data:
            merged_json = merged_data[key]

            for attr in [
                "Matrix Chemical Name",
                "Matrix Chemical Abbreviation",
                "Filler Chemical Name",
                "Filler Chemical Abbreviation",
                "Filler Composition Mass",
                "Filler Composition Volume",
                "Filler Particle Surface Treatment Chemical Name"
            ]:
                if (merged_json[attr] == "null" and data[attr] != "null") or (merged_json[attr] != "null" and data[attr] == "null"):
                    merged_json[attr] = data[attr] if data[attr] != "null" else merged_json[attr]

            for prop in data["Properties"]:
                prop_name = prop.get("property name")
                headers = prop.get("headers")

                for merged_prop in merged_json["Properties"]:
                    if merged_prop.get("property name") == prop_name and merged_prop.get("headers") == headers:
                        if prop["data"] is not None:
                            if merged_prop["data"] is None:
                                merged_prop["data"] = []
                            for data_point in prop["data"]:
                                exists = False
                                for merged_data_point in merged_prop["data"]:
                                    if data_point[0] == merged_data_point[0] and data_point[1] == merged_data_point[1]:
                                        exists = True
                                        break
                                if not exists:
                                    merged_prop["data"].append(data_point)
                        break
                else:
                    merged_json["Properties"].append(prop)
        else:
            merged_data[key] = data

    merged_json_list = list(merged_data.values())
    return merged_json_list


def save_merged_given_prediction(pred_folder_path, merged_path):
    
    pred_jsons = []
    for item_in_folder in os.listdir(pred_folder_path):
        
        # if item_in_folder is a folder
        if os.path.isdir(os.path.join(pred_folder_path, item_in_folder)):
            # go through the folder
            for file in os.listdir(os.path.join(pred_folder_path, item_in_folder)):
                # if the file is a json file
                if file.endswith(".txt"):
                    # load the json file
                    data_pred_path = os.path.join(pred_folder_path, item_in_folder, file)
                    # load data_pred_path
                    with open(data_pred_path) as f:
                        data_pred = f.read()

                        json_objects = extract_json_objects(data_pred)

                        json_objects = parse_json_objects(json_objects)

                        json_objects = [standardize_json(json_object) for json_object in json_objects]

                        pred_jsons.extend(json_objects)
        else:
            if item_in_folder.endswith(".json"):
                data_pred_path = os.path.join(pred_folder_path, item_in_folder)
                with open(data_pred_path) as f:
                    data_pred = f.read()

                    json_objects = extract_json_objects(data_pred)

                    json_objects = parse_json_objects(json_objects)

                    json_objects = [standardize_json(json_object) for json_object in json_objects]
                
                    pred_jsons.extend(json_objects)

            elif item_in_folder.endswith(".txt"):
                data_pred_path = os.path.join(pred_folder_path, item_in_folder)
                with open(data_pred_path) as f:
                    data_pred = f.read()

                    json_objects = extract_json_objects(data_pred)

                    json_objects = parse_json_objects(json_objects)

                    json_objects = [standardize_json(json_object) for json_object in json_objects]

                    pred_jsons.extend(json_objects)

                    

    merged_json_list = merge_json_files(pred_jsons)     
    
    if not os.path.exists(merged_path):
        os.makedirs(merged_path)
        
    for i, merged_json in enumerate(merged_json_list):
        with open(os.path.join(merged_path, f"merged-{i}.json"), "w") as f:
            json.dump(merged_json, f, indent=4)




# # Example usage
# json_files = ["file1.json", "file2.json", "file3.json"]
# merged_json_list = merge_json_files(json_files)

# print(len(merged_json_list))
# print(merged_json_list)

if __name__ == '__main__':
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--pred_folder_path', type=str, default="/usr/project/xtmp/gk126/nlp-for-materials/bench/modeling/pnc/property_extract_from_predictions", help="path to predicted jsons")
    parser.add_argument('--merged_path', type=str, default="/usr/project/xtmp/gk126/nlp-for-materials/bench/modeling/pnc/merged_predicted_jsons", help="path to save the merged jsons")
    args = parser.parse_args()

    save_merged_given_prediction(args.pred_folder_path, args.merged_path)
