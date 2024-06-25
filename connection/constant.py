from openai import OpenAI
from random import choices

MAX_WINDOW = 5

# GPT-series api-key from free gpt api.
OPENAI_API_KEY = "sk-Vq96CR7NAcSYbUraA8Be7e5a74Ae4bBe9742EaEe819910Ee"
OPENAI_BASE_URL = "https://free.gpt.ge/v1/"
OPENAI_DEFAULT_HEADERS = {"x-foo": "true"}

GPT_CLIENT = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    default_headers=OPENAI_DEFAULT_HEADERS)

# KIMI
KIMI_API_KEY = "sk-47wB6H6EiLpclmcf7F34ILKvf7aXLIuUecfp7vzeywXPb8Nu"
KIMI_BASE_URL = "https://api.moonshot.cn/v1"

KIMI_CLIENT = OpenAI(
    api_key=KIMI_API_KEY,
    base_url=KIMI_BASE_URL)

# KIMI-server
SERVER_URL = "http://127.0.0.1:8000/v1/chat/completions"

TOKEN_CZY = ("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMzU0Mzg2NiwiaWF0IjoxNzE1NzY3"
             "ODY2LCJqdGkiOiJjcDI4a2VpdG5uMGdqOHQ1MmMxZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjcDI3ZzU0dWR1NjVqM2JkazlwZyIsI"
             "nNwYWNlX2lkIjoiY3AyN2c1NHVkdTY1ajNiZGs5bGciLCJhYnN0cmFjdF91c2VyX2lkIjoiY3AyN2c1NHVkdTY1ajNiZGs5bDAifQ.ToL"
             "bJbZa7wYZaSgqLUUQOzMQUhcKKsH3yP5nlykCvCoYK0SH8C8VQWkTUS7D-4mhDps8kUPLEwUnfzLjNOcARg")

TOKEN_YST = ("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMzEzNDc5NiwiaWF0IjoxNzE1MzU4"
             "Nzk2LCJqdGkiOiJjb3Y0b2oydms2Z2ZpNHJobjlnMCIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbWZvNHJlY3A3ZmZuYzR2dXQwMCIsI"
             "nNwYWNlX2lkIjoiY21mbzRyZWNwN2ZmbmM0dnVzdmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY21mbzRyZWNwN2ZmbmM0dnV0MDAifQ.rZQ"
             "vnlZtPzYMXwlL1-aeTZ9oED81ciASCwksdN5ui80Ryb7zqvRn6ffos5Nx8QCce19OND02zXJz37-6AWNfag")

TOKEN_LJL = ("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyNjEzMjU0NCwiaWF0IjoxNzE4MzU2"
             "NTQ0LCJqdGkiOiJjcG0wa2czM2Flc3Vob2FoZ2NuZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbzBoc2RzdWR1NmY4ODNxZWJkMCIsI"
             "nNwYWNlX2lkIjoiY28waHNkc3VkdTZmODgzcWViY2ciLCJhYnN0cmFjdF91c2VyX2lkIjoiY28waHNkc3VkdTZmODgzcWViYzAifQ._CC"
             "B8UhSF_k6LiMmOw--DrJb-ON0E7M9RcqQigx2_Aebutpbph99wqm8-xx8hrdohXRfms2PBRBBKtgEb-E6MA")

TOKEN_YSZ = ("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyNjk5ODU3NCwiaWF0IjoxNzE5MjIy"
             "NTc0LCJqdGkiOiJjcHNrMmJocDJrMTIycjY4Mm9wZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjcDA1cWtxdG5uMHF0MzI3M29xMCIsI"
             "nNwYWNlX2lkIjoiY3AwNXFrcXRubjBxdDMyNzNvcGciLCJhYnN0cmFjdF91c2VyX2lkIjoiY3AwNXFrcXRubjBxdDMyNzNvcDAifQ.YEX"
             "mBLjBQkq__s81s_Zvc_PGB_r4WBuvoMWI1AfPMlCJ__WHJsqdDb9drn47GHBaeqbTabvdW8l-J3zy58UYxg")

TOKEN_POOL = [TOKEN_CZY, TOKEN_YST, TOKEN_LJL, TOKEN_YSZ]


def get_valid_headers() -> dict:
    token = choices(TOKEN_POOL, k=1)[0]
    return {'Content-Type': 'application/json','Authorization': f"Bearer {token}"}
