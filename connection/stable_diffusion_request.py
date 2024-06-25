import requests
import io
import base64
from PIL import Image
from copy import deepcopy

from typing import Dict,Literal

from connection.llmapi import LLMAPI, initialize_llm
from util.prompt import GENERATE_CHACTER_PROMPT, GENERATE_BACKGROUND_PROMPT
from util.constant import STABLE_DIFFUSION_CHATACTER_JSON, STABLE_DIFFUSION_BACKGROUND_JSON, STABLE_DIFFUSION_HEADER, STABLE_DIFFUSION_PROCESS_JSON

from util.constant import STABLE_DIFFUSION_URL_TEMPLATE


# TODO: Some is useless.

from util.utils import debug_print

class StableDiffusion:
    """
    A class for handling Stable Diffusion model operations, including image generation and processing.

    This class provides methods to input prompts, generate images, and process images using a Stable Diffusion model.

    Attributes:
    ---
        - t2i (dict): Parameters for text-to-image generation.
        - pp (dict): Parameters for image processing.
        - url (str): The API endpoint for the Stable Diffusion server.
        - headers (dict): The headers for the API requests.

    Methods:
    ---
        - input_prompt(prompt: str): Appends additional input to the current prompt.
        - generate_images() -> str: Generates images based on the current prompt and returns the base64 string of the generated image.
        - process_images(image: str): Processes the given base64 image string using the defined parameters.
    """

    def __init__(self):
        """
        Initializes the StableDiffusion instance with default parameters for text-to-image generation and image processing.
        """
        self.prompt_generator_c:LLMAPI = initialize_llm(GENERATE_CHACTER_PROMPT)
        self.prompt_generator_b:LLMAPI = initialize_llm(GENERATE_BACKGROUND_PROMPT)

        # self.character  :Dict[str,str]  = STABLE_DIFFUSION_CHATACTER_JSON
        # self.pp         :Dict[str,str]  = STABLE_DIFFUSION_PROCESS_JSON
        # self.background :Dict[str,str]  = STABLE_DIFFUSION_BACKGROUND_JSON
        # self.headers    :Dict[str, str] = STABLE_DIFFUSION_HEADER

    def generateImages(self, mode:int, prompt:str = "") -> str:
        """
        Generates images based on the current prompt.

        Makes an API request to the Stable Diffusion server to generate images.

        Args:
            mode (int): [1 / 2] generate character / background
            prompt (str, optional): the need of the prompt. Defaults to "".

        Returns:
            str: the base64 string of the generated image.
        """
        url = STABLE_DIFFUSION_URL_TEMPLATE.format("sdapi/v1/txt2img")

        if mode == 1:
            temporary_json = deepcopy(STABLE_DIFFUSION_CHATACTER_JSON)
        elif mode == 2:
            temporary_json = deepcopy(STABLE_DIFFUSION_BACKGROUND_JSON)
        else:
            raise ValueError("Invalid mode. Must be 1 or 2.")

        temporary_json['prompt'] += prompt

        # Make the API request
        debug_print("Generating...")
        response = requests.post(url    = url, 
                                json    = temporary_json,
                                headers = STABLE_DIFFUSION_HEADER)

        response.raise_for_status()  # Raise an error for bad status codes

        # Process the response
        r = response.json()
        imgb = ""
        for i, img_data in enumerate(r['images']):
            # Decode the base64 image data
            img_bytes = base64.b64decode(img_data.split(",", 1)[0])
            imgb = img_data
            # Save the image
            if mode == 1:
                with Image.open(io.BytesIO(img_bytes)) as img:
                    img.save(f'output_{i}.png')
                    
            elif mode == 2:
                with Image.open(io.BytesIO(img_bytes)) as img:
                    img.save('output_b.png')

        debug_print("Images saved successfully.")
        return imgb

    def process_images(self, image:str)->str:
        """
        Processes the given base64 image string using the defined parameters.

        Args:
            image (str): Base64 string of the image to be processed.
        """
        # Stable Diffusion API URL
        url = STABLE_DIFFUSION_URL_TEMPLATE.format("sdapi/v1/extra-single-image")

        # Make the API request
        debug_print("Processing...")
        temporary_json = deepcopy(STABLE_DIFFUSION_PROCESS_JSON)
        temporary_json['image'] = image
        response = requests.post(url    = url, 
                                json    = temporary_json,
                                headers = STABLE_DIFFUSION_HEADER)
        response.raise_for_status()  # Raise an error for bad status codes

        # Process the response
        r = response.json()
        img_data = r['image']
        image = img_data.split(",", 1)[0]

        return image

    def standard_workflow(self, need:str, mode:int) -> str:
        """
        Standard workflow for generating images.

        Args:
            need (str): the need for generating the image.
            mode (int): [1 / 2], whether to generate a foreground image or a background image.

        Returns:
            str: base64 of the image, storing in str rather than Byte
        """
        image = None

        if mode == 1:
            positive_prompt = self.prompt_generator_c.generateResponse(need)
        elif mode == 2:
            positive_prompt = self.prompt_generator_b.generateResponse(need)
        else:
            raise ValueError("Invalid mode. Please choose 1 or 2.")
        
        image = self.generateImages(mode = mode, prompt = positive_prompt)

        return self.process_images(image)


if __name__ == "__main__":
    sd = StableDiffusion()
    sd.standard_workflow("一个小姑娘", 1)
    sd.standard_workflow("一栋房子", 2)

