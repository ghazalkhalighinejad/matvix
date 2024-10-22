import anthropic
import os 
import base64
from PIL import Image
import pdb
from time import sleep
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

CLAUDE_CKPT = "claude-3-opus-20240229"
CLAUDE35_CKPT = "claude-3-5-sonnet-20240620"

import logging


logging.basicConfig(level=logging.INFO)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def call_claude3_vision(text_query, image_paths, temperature=0.0):
    images_base64 = [encode_image(path) for path in image_paths]
    success = False
    while not success:
        try:
            logging.info("Calling Claude 3 with vision")

            # Create a list of image contents
            image_contents = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",  # assuming all images are JPEGs
                        "data": img
                    }
                } for img in images_base64
            ]

            # Add the text query to the content list
            text_content = {
                "type": "text",
                "text": text_query
            }

            # Combine image contents and text content into a single content list
            content = image_contents + [text_content]

            # Send the request
            response = client.messages.create(
                model=CLAUDE_CKPT,  # Your Claude model checkpoint
                max_tokens=1024,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )

            # Extract response
            response_text = response.content[0].text
            success = True
        except Exception as e:
            print(f"Error: {e}")
            sleep(60)
    
    return response_text

    

def call_claude3(text_query, system_content="You extract structured data from scientific articles.", temperature=0.0):
    success = False
    while not success:
        try:
            response = client.messages.create(
                model=CLAUDE_CKPT,
                max_tokens=1024,
                temperature=temperature,
                system=system_content,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": text_query
                            }
                        ]
                    }
                ]
            )
            response = response.content[0].text
            success = True
        except Exception as e:
            print(e)
            sleep(60)
    return response

def call_claude35_vision(text_query, image_paths, temperature=0.0):

    images_base64 = [encode_image(path) for path in image_paths]
    success = False
    while not success:
        try:
            logging.info("Calling Claude 35 with vision")

            # Create a list of image contents
            image_contents = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",  # assuming all images are JPEGs
                        "data": img
                    }
                } for img in images_base64
            ]

            # Add the text query to the content list
            text_content = {
                "type": "text",
                "text": text_query
            }

            # Combine image contents and text content into a single content list
            content = image_contents + [text_content]

            # Send the request
            response = client.messages.create(
                model=CLAUDE35_CKPT,  # Your Claude model checkpoint
                max_tokens=1024,
                temperature=temperature,
                messages=[
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )

            # Extract response
            response_text = response.content[0].text
            success = True
        except Exception as e:
            print(f"Error: {e}")
            sleep(60)
    
    return response_text


def call_claude35(text_query, system_content="You extract structured data from scientific articles.", temperature=0.0):
    success = False
    while not success:
        try:
            response = client.messages.create(
                model=CLAUDE35_CKPT,
                max_tokens=1024,
                temperature=temperature,
                system=system_content,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": text_query
                            }
                        ]
                    }
                ]
            )
            response = response.content[0].text
            success = True
        except Exception as e:
            print(e)
            sleep(60)
    return response