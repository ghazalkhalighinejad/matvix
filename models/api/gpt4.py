from openai import OpenAI
import base64
import requests
import os 
import glob 
import numpy as np 
import pdb
import pandas as pd
import json 
from tqdm import tqdm
from time import sleep
client = OpenAI()
# OpenAI API Key
api_key = os.environ['OPENAI_API_KEY']

GPT_3_5_TURBO_CKPT = 'gpt-3.5-turbo-0125'
GPT_4o = 'gpt-4o'
GPT_4_TURBO = 'gpt-4-turbo'
# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

import requests
import base64

import requests

def call_gpt4o_vision(text_query, image_paths, temperature=0.0, max_tokens=1024):
    images_base64 = [encode_image(path) for path in image_paths]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

     # Create the content with text and all images
    content = [{"type": "text", "text": text_query}]
    for img_base64 in images_base64:
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_base64}"
                }
            }
        )

    payload = {
        "model": GPT_4o,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    response_content = response.json()['choices'][0]['message']['content']
    return response_content



def call_gpt4o(text_query, system_content="You extract structured data from scientific articles.", temperature=0.0, n=1):
    success = False
    while not success:
        try:
            response = client.chat.completions.create(
                model=GPT_4o, #gpt-4 turbo
                # response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": text_query },
                ],
                temperature = temperature,
                n = n
            )
            success = True
        except Exception as e:
            print(e)
            sleep(10)

    try:
        if n > 1:
            response = [response.choices[i].message.content for i in range(n)]
        else:
            response = response.choices[0].message.content
    except Exception as e:
        print(e)
        response = ""
    
    
    return response 

def call_gpt4_turbo_vision(text_query, image_paths, system_content="You extract structured data from scientific articles.", temperature=0.0, max_tokens=1024):
    images_base64 = [encode_image(path) for path in image_paths]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

     # Create the content with text and all images
    content = [{"type": "text", "text": text_query}]
    for img_base64 in images_base64:
        content.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_base64}"
                }
            }
        )

    payload = {
        "model": GPT_4_TURBO,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")

    response_content = response.json()['choices'][0]['message']['content']
    return response_content


def call_gpt4_turbo(text_query, system_content="You extract structured data from scientific articles.", temperature=0.0, n=1):
    success = False
    while not success:
        try:
            response = client.chat.completions.create(
                model=GPT_4_TURBO, #gpt-4 turbo
                # response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": text_query },
                ],
                temperature = temperature,
                n = n
            )
            success = True
        except Exception as e:
            print(e)
            sleep(10)

    try:
        if n > 1:
            response = [response.choices[i].message.content for i in range(n)]
        else:
            response = response.choices[0].message.content
    except Exception as e:
        print(e)
        response = ""
    
    return response 

def call_gpt3_5(text_query, system_content="You extract structured data from scientific articles.", temperature=0.0):
    success = False
    while not success:
        try:
            response = client.chat.completions.create(
                model=GPT_3_5_TURBO_CKPT,
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": text_query + "<json>"},
                ],
                temperature = temperature
            )
            success = True
        except Exception as e:
            print(e)
            sleep(10)

    try:
        response = response.choices[0].message.content
    except Exception as e:
        print(e)
        response = ""
    
    try:
        response = json.loads(response.lower())
    except:
        response = response
    return response 
