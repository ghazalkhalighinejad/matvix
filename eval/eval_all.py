from parse_samples import extract_json_objects, parse_json_objects
from eval_composition import eval_composition
from eval_property import eval_properties
import argparse
import os
import json
from standardize import standardize_property


def evaluate(true_folder_path, pred_folder_path):

    pred_jsons = []

    merged_pred_folder_path = os.path.join(pred_folder_path, "merged")
    for file in os.listdir(merged_pred_folder_path):
        if file.endswith((".txt", ".json")):
            data_pred_path = os.path.join(merged_pred_folder_path, file)
            with open(data_pred_path) as f:
                data_pred = f.read()

            json_objects = extract_json_objects(data_pred)
            json_objects = parse_json_objects(json_objects)

            pred_jsons.extend(json_objects)

    true_jsons = []
    for true_json in os.listdir(true_folder_path):
        # load true_json 
        with open(os.path.join(true_folder_path, true_json)) as f:
            data_true = f.read()
            data_true = json.loads(data_true)
            data_true = standardize_property(data_true)
            true_jsons.append(data_true)


    matches = eval_composition(pred_jsons, true_jsons)

    matched_comps = matches["matched_compositions"]

    property_scores_f1 = []
    num_unmatched_properties = 0

    all_human_eval_matches = []

    for match in matched_comps:
        corrects, false_positives, false_negatives = match[2][0], match[2][1], match[2][2]
        
        if corrects + false_positives == 0:
            precision = 0
        else:
            precision = corrects / (corrects + false_positives)
        if corrects + false_negatives == 0:
            recall = 0
        else:
            recall = corrects / (corrects + false_negatives)
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        property_score, num_unmatched_properties, human_eval_matches = eval_properties(match[1], match[0])
        
        property_scores_f1.append({"f1": f1, "precision": precision, "recall": recall, "property_scores": property_score})
        
        all_human_eval_matches.extend(human_eval_matches)

    return property_scores_f1, num_unmatched_properties, all_human_eval_matches

def main(true_folder_path, pred_folder_path):
    property_scores_f1 = []


    for article in os.listdir(true_folder_path):

        article_path_true = os.path.join(true_folder_path, article)
        article_id = article[:4]

        try:
            # find the article in the pred_folder_path that starts with the article_id
            article_path_pred = [os.path.join(pred_folder_path, article) for article in os.listdir(pred_folder_path) if article.startswith(article_id)][0]
        except IndexError:
            print(f"Article {article_id} not found in the pred_folder_path")
            continue
        
        property_score_f1 = evaluate(article_path_true, article_path_pred)
        property_scores_f1.extend(property_score_f1)


    return property_scores_f1


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--true_folder_path", type=str, help="Path to the folder containing the true json files")
    parser.add_argument("--pred_folder_path", type=str, help="Path to the folder containing the predicted json files")
    args = parser.parse_args()

    property_scores_f1, num_unmatched_properties = main(args.true_folder_path, args.pred_folder_path)

    f1 = sum([score["f1"] for score in property_scores_f1]) / len(property_scores_f1)
    precision = sum([score["precision"] for score in property_scores_f1]) / len(property_scores_f1)
    recall = sum([score["recall"] for score in property_scores_f1]) / len(property_scores_f1)

    
    property_scores = [score["property_scores"] for score in property_scores_f1]

    scores = {"levenshtein headers": [], "frechet data": [], "average": []}

    for property_score in property_scores:
        for property in property_score:
            for key in property:
                scores[key].append(property[key])
    
    save_path = os.path.join("eval_results", args.pred_folder_path.split("/")[-1])
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(os.path.join(save_path, "property_scores_f1.json"), "w") as f:
        save_results = {
            "f1": f1,
            "precision": precision,
            "recall": recall,
            "mean header": sum(scores["levenshtein headers"]) / len(scores["levenshtein headers"]),
            "mean data": sum(scores["frechet data"]) / len(scores["frechet data"]),
            "mean average": sum(scores["average"]) / len(scores["average"]),
        }

        json.dump(save_results, f)