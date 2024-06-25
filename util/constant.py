# This file mainly helps to define some constant, so that we can easily change them.

from datetime import timedelta
from enum import Enum

FLASK_SERVER = ("0.0.0.0",5000)

class BattleStatus(Enum):
    """
    Enum for the battle status.
    0: 等待接受
    1: 已接受
    2: 已拒绝
    3: 正在进行
    4: 已结束
    5: 意外结束
    """
    waiting    :int = 0
    accept     :int = 1
    refuse     :int = 2
    progressing:int = 3
    finished   :int = 4
    unexpected :int = 5


# configurations for the user.
INITIAL_DRAGON_EYE = 100
INITIAL_PHONEIX_FEATURE = 100
INITIAL_EXPERIENCE = 100

TASK_DISTRIBUTION = {
    "互动任务":0.20,
    "助人任务":0.20,
    "好汉任务":0.25,
    "豪杰任务":0.20,
    "英雄任务":0.15,
    "救世主任务":0.00
}


MAX_TASKNUM_QUEUE = 3
REFRESH_TASKQUEUE_INTERVAL_SECONDS = 600
SAVE_USER_INFO_INTERVAL_SECONDS = 300
CHECK_OFFLINE_INTERVAL_SECONDS = 30
CHECK_DEAD_BATTLE_INTERVAL_SECONDS = 60
WINNING_ROUND_TO_END = 3

USER_EXPIRE_TIME = timedelta(seconds=30)
TASK_EXPIRE_TIME = timedelta(minutes=1)


assert sum(TASK_DISTRIBUTION.values()) == 1.00, "The distribution of task type is rather not valid."



# Constant used in connection part.
MAX_WINDOW = 5




# Constant for Stable Diffusion.

STABLE_DIFFUSION_CHATACTER_JSON = {
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

STABLE_DIFFUSION_BACKGROUND_JSON = {
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

STABLE_DIFFUSION_HEADER = {
            "Authorization": "Basic TXVZaVBhcmFzb2w6MjAwMzAxMjQ="
        }

STABLE_DIFFUSION_PROCESS_JSON = {
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

STABLE_DIFFUSION_IPV4 = "http://127.0.0.1:7860/"

STABLE_DIFFUSION_URL_TEMPLATE = "http://127.0.0.1:7860/{}"