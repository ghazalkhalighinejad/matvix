import numpy as np
import Levenshtein
import numpy as np
from matching_algorithm import match_samples

from frechet import DiscreteFrechet, euclidean


def eval_headers(headers_true, headers_pred):

    """
    headers_true and headers_pred are lists of ["x label", "y label"]
    """
    if headers_pred == [] or headers_pred == None:
        headers_pred = ['null', 'null']

    if headers_pred == [] or any([header == None for header in headers_pred]) or headers_pred == None:
        headers_pred = ['null', 'null']

    if headers_true == [] or any([header == None for header in headers_true]) or headers_true == None:
        headers_true = ['null', 'null']

    headers_true = [header.lower() for header in headers_true]
    headers_pred = [header.lower() for header in headers_pred]

    headers_true = ["".join(filter(str.isalpha, header)) for header in headers_true]
    headers_pred = ["".join(filter(str.isalpha, header)) for header in headers_pred]

    concat_pred = headers_pred[0] + headers_pred[1]
    concat_true = headers_true[0] + headers_true[1]

    concat_nl_dist = Levenshtein.distance(concat_true, concat_pred) / max(len(concat_true), len(concat_pred))
    concat_nl_dist = min(1, concat_nl_dist)

    return 1-concat_nl_dist

def eval_data(data_true, data_pred):
    """
    data is a list of tuples (x, y)
    """
    if data_true == [] or data_true is None or data_true == [[]]:
        data_true = 'null'
    if isinstance(data_true, list):
        if any([data == ['null', 'null'] for data in data_true]):
            data_true = 'null'
    if data_pred == [] or data_pred is None or data_pred == [[]]:
        data_pred = 'null'
    if isinstance(data_pred, list):
        if any([data == ['null', 'null'] for data in data_pred]):
            data_pred = 'null'
    if data_pred == data_true:
        return 1
    if data_pred == 'null' or data_true == 'null':
        return 0
        
    if not isinstance(data_pred, list) and data_pred != 'null':
        raise ValueError("data_pred should be a list of tuples")
    
    data_true = [[float(x_y[0]), float(x_y[1])] for x_y in data_true]
    try:
        data_pred = [[float(x_y[0]), float(x_y[1])] for x_y in data_pred]
    except KeyError:
        return 0

    data_true = np.array(data_true)
    data_pred = np.array(data_pred)
    
    if len(data_true) > 100:
        indices = np.random.choice(len(data_true), 100)
        data_true = data_true[indices]

    rdfd = DiscreteFrechet(euclidean)
    distance = rdfd.distance(data_true, data_pred)

    distance = min(1, distance / np.linalg.norm(data_true))

    return 1-distance 


def eval_property(data_true, data_pred):

    """
    data_true and data_pred are dictionaries with keys "headers" and "data"
    """
  
    data_true_header = data_true["headers"]
    try:
        data_pred_header = data_pred.get("headers")
    except Exception as e:
        data_pred_header = None

    data_true_data = data_true["data"]
    try:
        data_pred_data = data_pred.get("data")
    except Exception as e:
        data_pred_data = None

    lev_dist_headers = eval_headers(data_true_header, data_pred_header)

    frech_dist_data = eval_data(data_true_data, data_pred_data)

    scores = {}

    scores["levenshtein headers"] = lev_dist_headers
    scores["frechet data"] = frech_dist_data

    scores["average"] = lev_dist_headers * frech_dist_data

    return scores

def eval_properties(data_true, data_pred, task):

    if task == "pnc":
        data_true = data_true["Properties"]
        data_pred = data_pred["Properties"]
    elif task == "pbd":
        data_true = data_true["Biodegradation"]
        data_pred = data_pred["Biodegradation"]

    if data_true == None:
        data_true = []
    if data_pred == None:
        data_pred = []

    if not isinstance(data_pred, list):
        data_pred = [data_pred]

    property_scores = []

    is_js_scores = []   

    for i, property_true in enumerate(data_true):
        for j, property_pred in enumerate(data_pred):
            score = eval_property(property_true, property_pred)["levenshtein headers"]
            is_js_scores.append([i, j, -score])

    if len(is_js_scores) == 0:
        return property_scores
    
    else:
        matches = match_samples(is_js_scores, len(data_true), len(data_pred))

        matched_trues = [match[0] for match in matches]
        matched_preds = [match[1] for match in matches]

        for k in range(len(matched_trues)):
            i = matched_trues[k]
            property_true = data_true[i]
            j = matched_preds[k]
            property_pred = data_pred[j]
            scores = eval_property(property_true, property_pred)
            property_scores.append(scores)

        # add zero scores for unmatched properties]
        for i in range(len(data_true)):
            if i not in matched_trues:
                property_scores.append({"levenshtein headers": 0, "frechet data": 0, "average": 0})

        return property_scores




