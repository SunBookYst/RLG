import requests
import io
import base64
from PIL import Image

from connection.llmapi import LLMAPI
from util.prompt import GENERATE_CHACTER_PROMPT, GENERATE_BACKGROUND_PROMPT

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
        self.prompt_generator_c = LLMAPI("KIMI-server")
        self.prompt_generator_b = LLMAPI("KIMI-server")

        self.character = {
            "prompt": "masterpiece,best quality, ultra-detailed, highres, clear face, only 1 character",
            "negative_prompt": "NSFW, (worst quality, low quality:1.3)",
            "seed": -1,
            "batch_size": 1,
            "n_iter": 1,
            "steps": 22,
            "cfg_scale": 9,
            "width": 512,
            "height": 512,
            "override_settings": {
                "sd_model_checkpoint": "etherBluMix_etherBluMix7.safetensors [686eec2aef]",
                "sd_vae": "kl-f8-anime2.ckpt",
            },
            "sampler_index": "DPM++ 2M Karras",
        }

        self.pp = {
            "resize_mode": 0,
            "gfpgan_visibility": 0,
            "codeformer_visibility": 0,
            "codeformer_weight": 0,
            "upscaling_resize": 2,
            "upscaling_resize_w": 512,
            "upscaling_resize_h": 512,
            "upscaler_1": "None",
            "upscaler_2": "None",
            "extras_upscaler_2_visibility": 0,
            "image": "",
        }

        self.background = {
            "prompt": "masterpiece,best quality, ultra-detailed, highres,",
            "negative_prompt": "low quality, ((human)), man, character",
            "seed": -1,
            "batch_size": 1,
            "n_iter": 1,
            "steps": 20,
            "cfg_scale": 7,
            "width": 512,
            "height": 256,
            "override_settings": {
                "sd_model_checkpoint": "etherBluMix_etherBluMix7.safetensors [686eec2aef]",
                "sd_vae": "kl-f8-anime2.ckpt",
            },
            "sampler_index": "DPM++ 2M Karras",
        }

        self.headers = {
            "Authorization": "Basic TXVZaVBhcmFzb2w6MjAwMzAxMjQ="
        }

    def initialize(self):


        self.prompt_generator_c.generateResponse(GENERATE_CHACTER_PROMPT)
        self.prompt_generator_b.generateResponse(GENERATE_BACKGROUND_PROMPT)

    def input_prompt(self, prompt):
        """
        Appends additional input to the current prompt.

        Args:
            prompt (str): Additional prompt to be appended.
        """
        print("Entering additional input for the prompt...")
        self.character['prompt'] += prompt

    def generate_images(self, prompt=None):
        """
        Generates images based on the current prompt.

        Makes an API request to the Stable Diffusion server to generate images.

        Returns:
            str: Base64 string of the generated image.
        """
        # Stable Diffusion API URL
        url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
        self.character['prompt'] += prompt
        # Make the API request
        print("Generating...")
        response = requests.post(url, json=self.character, headers=self.headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Process the response
        r = response.json()
        imgb = ""
        for i, img_data in enumerate(r['images']):
            # Decode the base64 image data
            img_bytes = base64.b64decode(img_data.split(",", 1)[0])
            imgb = img_data
            # Save the image
            with Image.open(io.BytesIO(img_bytes)) as img:
                img.save(f'output_{i}.png')

        print("Images saved successfully.")
        return imgb

    def generate_background(self, prompt=None):
        """
        Generates images based on the current prompt.

        Makes an API request to the Stable Diffusion server to generate images.

        Returns:
            str: Base64 string of the generated image.
        """
        # Stable Diffusion API URL
        url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
        self.background['prompt'] += prompt
        # Make the API request
        print("Generating...")
        response = requests.post(url, json=self.background, headers=self.headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Process the response
        r = response.json()
        imgb = ""
        for i, img_data in enumerate(r['images']):
            # Decode the base64 image data
            img_bytes = base64.b64decode(img_data.split(",", 1)[0])
            imgb = img_data
            # Save the image
            with Image.open(io.BytesIO(img_bytes)) as img:
                img.save(f'output_b.png')

        print("Images saved successfully.")
        return imgb

    def process_images(self, image):
        """
        Processes the given base64 image string using the defined parameters.

        Args:
            image (str): Base64 string of the image to be processed.
        """
        # Stable Diffusion API URL
        url = "http://127.0.0.1:7860/sdapi/v1/extra-single-image"

        # Make the API request
        print("Processing...")
        self.pp['image'] = image
        response = requests.post(url, json=self.pp, headers=self.headers)
        response.raise_for_status()  # Raise an error for bad status codes

        # Process the response
        r = response.json()
        # print(r)
        img_data = r['image']

        image = img_data.split(",", 1)[0]

        return image

    def standard_workflow(self, need, mode):
        """
        标准工作流程
        :param need: 需求描述
        :param mode: 1（人像模式）|2（背景模式）
        :return: 像素化后的图片
        """
        image = None

        if mode == 1:
            positive_prompt = self.prompt_generator_c.generateResponse(need)
            image = self.generate_images(positive_prompt)
        elif mode == 2:
            positive_prompt = self.prompt_generator_b.generateResponse(need)
            image = self.generate_background(positive_prompt)

        return self.process_images(image)


if __name__ == "__main__":
    sd = StableDiffusion()
    sd.initialize()
    sd.standard_workflow("一个小姑娘", 1)
    sd.standard_workflow("一栋房子", 2)

