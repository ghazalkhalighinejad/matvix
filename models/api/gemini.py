import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import os 
from PIL import Image
import pdb
from time import sleep
import logging


logging.basicConfig(level=logging.INFO)

GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}
def call_gemini_pro_vision(text_query, image_paths, temperature=0.0):
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    imgs = [Image.open(image_path) for image_path in image_paths]

    success = False
    while not success:
        try:
            response = model.generate_content(
                contents = [text_query] + imgs,
                generation_config = genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=1024,
                    temperature=temperature
                ),
                safety_settings=safety_settings
            )
            success = True
        except Exception as e:
            print(e)
            sleep(10)
    try:
        response = response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        print(text_query)
        print(response)
        response = ""
    return response


def call_gemini_pro(text_query, temperature=0.0):
    model = genai.GenerativeModel('gemini-1.5-pro')

    success = False
    while not success:
        try:
            response = model.generate_content(
                text_query, \
                generation_config = genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=1024,
                    temperature=temperature
                ),
                safety_settings=safety_settings
            )
            success = True
        except Exception as e:
            print(e)
            sleep(10)
    
    try:
        response = response.candidates[0].content.parts[0].text
    except Exception as e:
        print(e)
        print(text_query)
        print(response)
        response = ""
    return response

## PaLM 2 is legacy, but we keep it here for text only evaluations
def call_palm_2(text_query, temperature=0.0):
    PALM_API_KEY=os.getenv('PALM_API_KEY')
    if PALM_API_KEY is None:
        print("Warning: PALM_API_KEY not set")
        PALM_API_KEY = GOOGLE_API_KEY
    genai.configure(api_key=PALM_API_KEY)
    success = False
    while not success:
        try:
            response = genai.generate_text(
                model='models/text-bison-001',
                prompt=text_query,
                temperature=temperature,
                candidate_count=1,
                max_output_tokens=1024,
            )
            success = True
        except Exception as e:
            print(e)
            sleep(60)
    # PaLM-2 has weird rate limiting issues
    # sleep one second after each query to resolve
    sleep(1)
    return response.result

if __name__ == '__main__':
    text_query = "are the two highlighed red nodes connected?"
    image_path = "graph/0_1_0_yes.png"
    response = call_gemini_pro_vision(text_query, image_path)
    pdb.set_trace()
    