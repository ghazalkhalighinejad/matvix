
import os
import json 
from tqdm import tqdm
import argparse
import logging
import sys
sys.path.append("/usr/project/xtmp/gk126/nlp-for-materials/bench/modeling")

from transformers import AutoProcessor, Pix2StructForConditionalGeneration
from PIL import Image
from transformers import Pix2StructForConditionalGeneration
import re

from api.gpt4 import call_gpt4o_vision, call_gpt4o, call_gpt4_turbo_vision, call_gpt4_turbo

from api.gemini import call_gemini_pro_vision, call_gemini_pro
from api.claude import call_claude3_vision, call_claude3, call_claude35_vision, call_claude35

from prompts import get_prompt_dict

from merge_samples import save_merged_given_prediction



def figures_to_data(image, text):

    model = Pix2StructForConditionalGeneration.from_pretrained("google/deplot").to("cuda")
    processor = AutoProcessor.from_pretrained("google/deplot")
    inputs = processor(images=image, text=text, return_tensors="pt").to("cuda")
    predictions = model.generate(**inputs, max_new_tokens=512)
    return processor.decode(predictions[0], skip_special_tokens=True)


def replace_figures_with_data(latex, image_folder):

    pattern = r'\\includegraphics\[[^\]]*\]{([^}]*)}'
    matches = re.findall(pattern, latex)
    figures = [match + ".jpg" for match in matches]
    images = [Image.open(f"{image_folder}/{figure}") for figure in figures]

    after_latex = latex

    for i, match in enumerate(matches):

        returned_ = figures_to_data(images[i], "Generate underlying data table of the figure below:")
        after_latex = after_latex.replace("{" + match + "}", returned_)

    return after_latex


def get_sample_compositions(article_id, path_to_jsons):

    sample_compositions = []

    article_id = article_id[:4]
    
    try:
        folder = [folder for folder in os.listdir(path_to_jsons) if folder.startswith(article_id)][0]
    except IndexError:
        return []

    merged_folder = os.path.join(path_to_jsons, folder, "merged")

    for sample in os.listdir(merged_folder):
        with open(os.path.join(merged_folder, sample), "r") as f:
                
            sample_compositions.append(json.load(f))

 
    return json.dumps(sample_compositions)


def get_prompts(prompt_type, sample_compositions, article, images):


    all_prompts = get_prompt_dict(sample_compositions)
    
    prompts = []
    if "allin" in prompt_type and "multi-image" in prompt_type:

        text_query = all_prompts["allin_multi-image"]
        text_query = text_query + "\n" + article
        prompt = {
            "images": images,
            "text_query": text_query
        }
        prompts.append(prompt)
        
    elif "allin" in prompt_type and "single-image" in prompt_type:

        text_query = all_prompts["allin_single-image"]
        text_query = text_query + "\n" + article

        for image in images:
            prompt = {
                "images": [image],
                "text_query": text_query
            }
            prompts.append(prompt)

    elif "only-text" in prompt_type:

        text_query = all_prompts["only-text"]
        text_query = text_query + "\n" + article

        images = []
        prompt = {
            "text_query": text_query,
            "images": images
        }
        prompts.append(prompt)

    elif "only-image" in prompt_type and "single-image" in prompt_type:

        text_query = all_prompts["only-image_single-image"]


        for image in images:
            prompt = {
                "images": [image],
                "text_query": text_query
            }
            prompts.append(prompt)

    elif "only-image" in prompt_type and "multi-image" in prompt_type:
            
        text_query = all_prompts["only-image_multi-image"]
        
        prompt = {
            "images": images,
            "text_query": text_query
        }
        prompts.append(prompt)
    
    return prompts


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', action="store_true", help="resume from last checkpoint")
    parser.add_argument('--model', type=str, default="gpt4", help="model to use")
    parser.add_argument('--articles_path', type=str, default="articles/unzipped", help="path to articles json")
    parser.add_argument('--prompt_type', type=str, default="allin_single-image", help="should be one of allin_single-image, allin_multi-image, only-text, only-image_single-image, only-image_multi-image")
    parser.add_argument('--deplot', action="store_true", help="use deplot")
    parser.add_argument('--samples_path', type=str, default="pnc/samples", help="path to samples json already extracted in previous step")

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    logger.info(f"Using model {args.model} with prompt type {args.prompt_type} and {'deplot' if args.deplot else 'no deplot'}")

    save_path = f"predictions_{args.model}_{args.prompt_type}_{'deplot' if args.deplot else 'no_deplot'}"
    articles_processed = []

    if args.resume:
        if os.path.exists(f"pnc/{save_path}"):
            articles_processed = [file.split(".")[0] for file in os.listdir(f"pnc/{save_path}")]

    articles = os.listdir(args.articles_path)
    
    process_bar = tqdm(articles)

    for article in process_bar:
        
        if args.resume and article.split(".")[0] in articles_processed:
            continue
        
        article_id = article.split(".")[0]
        image_folder = os.path.join(args.articles_path, article, "images")

        for file in os.listdir(os.path.join(args.articles_path, article)):
            if file.endswith(".tex"):
                with open(os.path.join(args.articles_path, article, file), "r", encoding="utf-8") as f:
                    latex = f.read()
                    break
        
        if args.deplot and ("only-image" not in args.prompt_type):
            latex = replace_figures_with_data(latex, image_folder)

        if article_id in articles_processed:
            continue
        
        if args.prompt_type == "only-image_single-image" or args.prompt_type == "only-image_multi-image":
            sample_compositions = get_sample_compositions(article, args.samples_path)
        else:
            sample_compositions = []

 

        prompts = get_prompts(args.prompt_type, sample_compositions, latex, [os.path.join(image_folder, image) for image in os.listdir(image_folder)])
        
        for i, prompt in enumerate(prompts):
            text_query, image_paths = prompt["text_query"], prompt["images"]

            if "gpt4o" in args.model:
                if len(image_paths) > 0:
                    response = call_gpt4o_vision(text_query, image_paths)
                else:
                    response = call_gpt4o(text_query)
            elif "gpt4-turbo" in args.model:
                if len(image_paths) > 0:
                    response = call_gpt4_turbo_vision(text_query, image_paths)
                else:
                    response = call_gpt4_turbo(text_query)
            elif args.model == "gemini":
                if len(image_paths) > 0:
                    response = call_gemini_pro_vision(text_query, image_paths)
                else:
                    response = call_gemini_pro(text_query)
            elif args.model == "claude3":
                if len(image_paths) > 0:
                    response = call_claude3_vision(text_query, image_paths)
                else:
                    response = call_claude3(text_query)
            elif args.model == "claude35":
                if len(image_paths) > 0:
                    response = call_claude35_vision(text_query, image_paths, temperature=0)
                else:
                    response = call_claude35(text_query, temperature=0)
            else:
                print("Invalid model")
                sys.exit(1)

            if not os.path.exists(f"pnc/{save_path}/{article}/responses"):
                os.makedirs(f"pnc/{save_path}/{article}/responses")
            
            if not os.path.exists(f"pnc/{save_path}/{article}/prompts"):
                os.makedirs(f"pnc/{save_path}/{article}/prompts")

            with open(f"pnc/{save_path}/{article}/responses/response-{i}.txt", "w") as f:
                f.write(response)
            
            with open(f"pnc/{save_path}/{article}/prompts/prompt-{i}.txt", "w") as f:
                f.write(text_query + "\n" + str(image_paths))

        if not os.path.exists(f"pnc/{save_path}/{article}/merged"):
            os.makedirs(f"pnc/{save_path}/{article}/merged")

        save_merged_given_prediction(f"pnc/{save_path}/{article}/responses", f"pnc/{save_path}/{article}/merged")

            
            