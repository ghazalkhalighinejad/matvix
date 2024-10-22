
from matching_algorithm import match_samples
from standardize import standardize


def scores(correct, false_positive, false_negative):
    
    if correct + false_positive == 0:
        precision = 0
    else:
        precision = correct / (correct + false_positive)
    if correct + false_negative == 0:
        recall = 0
    else:
        recall = correct / (correct + false_negative)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return f1, precision, recall


def exact_match_entities(pred_entity, true_entity, true_entity_abbr):
    pred_entity = str(pred_entity)
    true_entity = str(true_entity)
    
    pred_entity = pred_entity.lower().replace(" ", "").replace("-", "")
    true_entity = true_entity.lower().replace(" ", "").replace("-", "")
    
    pred_entity = ''.join(e for e in pred_entity if e.isalnum())
    true_entity = ''.join(e for e in true_entity if e.isalnum())

    if pred_entity.endswith("s") and not true_entity.endswith("s"):
        pred_entity = pred_entity[:-1]
    if true_entity.endswith("s") and not pred_entity.endswith("s"):
        true_entity = true_entity[:-1]

    if true_entity_abbr != None:
        true_entity_abbr = true_entity_abbr.lower().replace(" ", "").replace("-", "")
        true_entity_abbr = ''.join(e for e in true_entity_abbr if e.isalnum())

    return  (pred_entity == true_entity) or (pred_entity == true_entity_abbr)

def get_f1_pnc(sample, true_json):

    f1 = correct = false_positive = false_negative = exact_match = total = 0

    standardize_pred_sample = sample.copy()


    false_negatives = {"matrix chemical name": 0, "filler chemical name": 0, "composition": 0}
    false_positives = {"matrix chemical name": 0, "filler chemical name": 0, "composition": 0}
    corrects = {"matrix chemical name": 0, "filler chemical name": 0, "composition": 0}

    try:
        pred_chemname = sample["Matrix Component"]
    except KeyError:
        pred_chemname = None
    try:
        pred_chemname_abbr = sample["Matrix Abbreviation"]
    except KeyError:
        pred_chemname_abbr = None
    try:
        pred_chemname_abbr = sample["Matrix Abbreviation"]
    except KeyError:
        pass
    true_chemname = true_json["Matrix Component"]
    true_chemname_abbr = true_json["Matrix Abbreviation"]

    if pred_chemname == "null":
        pred_chemname = None
    if pred_chemname_abbr == "null":
        pred_chemname_abbr = None

    # make sure pred_chemname is not a list
    if pred_chemname != None and true_chemname != None:
        
        if exact_match_entities(pred_chemname, true_chemname, true_chemname_abbr):
            correct += 1
            corrects["matrix chemical name"] += 1
            
        else:
            pred_chemname = standardize(pred_chemname)
            standardize_pred_sample["Matrix Component"] = pred_chemname
            if exact_match_entities(pred_chemname, true_chemname, true_chemname_abbr):
                correct += 1
                corrects["matrix chemical name"] += 1
              
            else:
        

                false_positive += 1
                false_negative += 1
                false_positives["matrix chemical name"] += 1
                false_negatives["matrix chemical name"] += 1


    else: 
       
        false_negative += 1
        false_negatives["matrix chemical name"] += 1
    

    try:
        pred_filler_chemname = sample["Filler Chemical Name"]
    except KeyError:
        pred_filler_chemname = None
    true_filler_chemname = true_json["Filler Chemical Name"]
    true_filler_chemname_abbr = true_json["Filler Abbreviation"]

    if pred_filler_chemname == "null":
        pred_filler_chemname = None
    
    if pred_filler_chemname != None and true_filler_chemname != None:
        if exact_match_entities(pred_filler_chemname, true_filler_chemname, true_filler_chemname_abbr):
            correct += 1
            corrects["filler chemical name"] += 1
         
        else:
            pred_filler_chemname = standardize(pred_filler_chemname, filler = True)
            standardize_pred_sample["Filler Chemical Name"] = pred_filler_chemname
            if exact_match_entities(pred_filler_chemname, true_filler_chemname, true_filler_chemname_abbr):
                correct += 1
                corrects["filler chemical name"] += 1
                
            else:
               
                false_positive += 1
                false_negative += 1
                false_negatives["filler chemical name"] += 1
                false_positives["filler chemical name"] += 1
            
     
    elif pred_filler_chemname == None and true_filler_chemname != None:
        
        false_negative += 1
        false_negatives["filler chemical name"] += 1
        
    elif pred_filler_chemname != None and true_filler_chemname == None:
        
        false_positive += 1
        false_positives["filler chemical name"] += 1

    pred_mass = str(sample["Filler Composition Mass"])
    if pred_mass == "null" or pred_mass == "None":
        pred_mass = None
    true_mass = true_json["Filler Mass"]

    pred_vol = str(sample["Filler Composition Volume"])
    if pred_vol == "null" or pred_vol == "None":
        pred_vol = None
    true_vol = true_json["Filler Volume"]

    true_composition = true_mass if true_mass != None else true_vol
    pred_composition = pred_mass if pred_mass != None else pred_vol

    if pred_composition == None and true_composition == None:
        pass
    elif pred_composition != None and true_composition != None:
        if pred_composition == true_composition:
            correct += 1
            corrects["composition"] += 1
            
        
        elif any(char.isdigit() for char in pred_composition):
            # get rid of the non digits except for .
            vol = pred_composition
            pred_composition = ''.join(e for e in pred_composition if e.isdigit() or e == '.')
            
            try:
                pred_composition = float(pred_composition)
                if "%" in vol:
                    pred_composition = pred_composition / 100
            except:
                pass
            try:
                true_composition = float(true_composition)
            except:
                pass
            if pred_composition == true_composition:
                correct += 1
                corrects["composition"] += 1
                
            else:

                false_positive += 1
                false_negative += 1
                false_positives["composition"] += 1
                false_negatives["composition"] += 1

        else:
            
            false_positive += 1
            false_negative += 1
            false_positives["composition"] += 1
            false_negatives["composition"] += 1   
    
    elif pred_composition == None and true_composition != None:
        
        false_negative += 1
        false_negatives["composition"] += 1

    
    elif pred_composition != None and true_composition == None:
        
        false_positive += 1
        false_positives["composition"] += 1
        
    f1, precision, recall = scores(correct, false_positive, false_negative)    

    return f1, correct, false_positive, false_negative, exact_match, total, corrects, false_negatives, false_positives

def get_f1_pbd(sample, true_json):

    f1 = correct = false_positive = false_negative = exact_match = total = 0
    false_negatives = false_positives = corrects = {
        "polymer type": 0, "substitution type": 0, "degree of substitution": 0, "degree of hydrolysis": 0, "molecular weight": 0
    }
    
    for key in ["Polymer Type", "Substitution Type", "Degree of Substitution", "Degree of hydrolysis", "Molecular Weight"]:
        pred_value = sample.get(key.lower(), sample.get(key.title(), sample.get(key)))
        true_value = true_json.get(key.lower(), true_json.get(key.title(), true_json.get(key)))
        
        if pred_value is not None and true_value is not None:
            if (key in ["Degree of Substitution", "Molecular weight"] and pred_value == true_value) or \
               (key not in ["Degree of Substitution", "Molecular weight"] and exact_match_entities(str(pred_value), str(true_value))):
                correct += 1
                corrects[key.lower()] += 1
            else:
                false_positive += 1
                false_negative += 1
                false_positives[key.lower()] += 1
                false_negatives[key.lower()] += 1
        elif pred_value is None and true_value is not None:
            false_negative += 1
            false_negatives[key.lower()] += 1
        elif pred_value is not None and true_value is None:
            false_positive += 1
            false_positives[key.lower()] += 1
        
    f1, precision, recall = scores(correct, false_positive, false_negative)    

    return f1, correct, false_positive, false_negative, exact_match, total, corrects, false_negatives, false_positives


def eval_composition(pred_jsons, true_jsons, task):


    matched_compositions = []

    is_js_scores = []
    
    for i, true_json in enumerate(true_jsons):
        for j, sample in enumerate(pred_jsons):
            if task == "pnc":
                f1, _, _, _, _, _, _, _, _ = get_f1_pnc(sample, true_json)
            elif task == "pbd":
                f1, _, _, _, _, _, _, _, _ = get_f1_pbd(sample, true_json)
            is_js_scores.append([i, j, f1])
    
    matches = match_samples(is_js_scores, len(true_jsons), len(pred_jsons))
    
    matched_trues = [match[0] for match in matches]
    matched_preds = [match[1] for match in matches]

    for k in range(len(matched_trues)):
        i = matched_trues[k]
        true_json = true_jsons[i]
        j = matched_preds[k]
        sample = pred_jsons[j]
        if task == "pnc":
            f1, corrects, false_positives, false_negatives, exact_match, total, all_corrects, all_fns, all_fps = get_f1_pnc(sample, true_json)
        elif task == "pbd":
            f1, corrects, false_positives, false_negatives, exact_match, total, all_corrects, all_fns, all_fps = get_f1_pbd(sample, true_json)
        
        matched_compositions.append((sample, true_json, [corrects, false_positives, false_negatives]))
    

    return {"matched_compositions": matched_compositions, "len true": len(true_jsons), "len pred": len(pred_jsons)}
