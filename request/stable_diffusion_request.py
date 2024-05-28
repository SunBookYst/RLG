import requests
import io
import base64
from PIL import Image

from llmapi import LLMAPI


def read_file(path):
    """
    读取文件内容。

    Args:
        path (str): 文件路径。

    Returns:
        str: 文件内容。
    """
    with open(path, 'r', encoding='utf-8') as file:
        prompt = file.read()
    return prompt


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
        self.t2i = {
            "prompt": "masterpiece,best quality, ultra-detailed, highres, clear face, only 1 character",
            "negative_prompt": "bad hand, (ugly:1.5), lowres, bad anatomy, [:((No more than one thumb, "
                               "index finger, middle finger, ring finger and little finger on one hand),(mutated hands"
                               " and fingers:1.5 ), fused ears, one hand with more than 5 fingers, one hand with less"
                               " than 5 fingers):0.5],multiple breasts, (mutated hands and fingers:1.5 ), liquid body,"
                               " liquid tongue,anatomical nonsense,more than 2 nipples,different nipples,fused nipples,"
                               "bad hands, bad pussy, fused pussy, text, error, missing fingers, extra digit, "
                               "fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, "
                               "signature, watermark, username, blurry, Missing limbs, three arms, bad feet, text font "
                               "ui, signature, blurry, malformed hands, long neck, (long body :1.3), (mutation ,"
                               "poorly drawn :1.2), disfigured, malformed,mutated, three legs",
            "seed": -1,
            "batch_size": 1,
            "n_iter": 1,
            "steps": 30,
            "cfg_scale": 7,
            "width": 512,
            "height": 512,
            "override_settings": {
                "sd_model_checkpoint": "coffeensfw_v10.safetensors [ed47f47f0a]",
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

        # Authorization headers (if needed)
        self.headers = {
            "Authorization": "Basic TXVZaVBhcmFzb2w6MjAwMzAxMjQ="
        }

    def input_prompt(self, prompt):
        """
        Appends additional input to the current prompt.

        Args:
            prompt (str): Additional prompt to be appended.
        """
        print("Entering additional input for the prompt...")
        self.t2i['prompt'] += prompt

    def generate_images(self):
        """
        Generates images based on the current prompt.

        Makes an API request to the Stable Diffusion server to generate images.

        Returns:
            str: Base64 string of the generated image.
        """
        # Stable Diffusion API URL
        url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

        # Make the API request
        print("Generating...")
        response = requests.post(url, json=self.t2i, headers=self.headers)
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

        image = Image.open(io.BytesIO(base64.b64decode(img_data.split(",",1)[0])))

        # Save the image
        image.save(f'output_p.png')

        print("Images saved successfully.")


def main():
    t2i_prompt = read_file('../prompts/txt2img.txt')

    prompt_generator = LLMAPI("KIMI-server")
    response = prompt_generator.generateResponse(t2i_prompt)
    print(response)

    content = prompt_generator.generateResponse(input("请输入需求："))
    sd = StableDiffusion()
    sd.input_prompt(content)
    image = sd.generate_images()
    sd.process_images(image)


if __name__ == "__main__":
    main()
