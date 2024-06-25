from openai import OpenAI

from random import choices


MAX_WINDOW = 5
# GPT-series api-key from free gpt api.
OPENAI_API_KEY = "sk-Vq96CR7NAcSYbUraA8Be7e5a74Ae4bBe9742EaEe819910Ee"
OPENAI_BASE_URL = "https://free.gpt.ge/v1/"
OPENAI_DEFAULT_HEADERS = {"x-foo": "true"}

GPT_CLIENT = OpenAI(
        api_key         = OPENAI_API_KEY, 
        base_url        = OPENAI_BASE_URL, 
        default_headers = OPENAI_DEFAULT_HEADERS)

# KIMI
KIMI_API_KEY = "sk-47wB6H6EiLpclmcf7F34ILKvf7aXLIuUecfp7vzeywXPb8Nu"
KIMI_BASE_URL = "https://api.moonshot.cn/v1"

KIMI_CLIENT = OpenAI(
        api_key  = KIMI_API_KEY, 
        base_url = KIMI_BASE_URL)


# KIMI-server
SERVER_URL = "http://172.25.25.63:8000/v1/chat/completions"
TOKEN_CZY = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMzU0Mzg2NiwiaWF0IjoxNzE1NzY3ODY2LCJqdGkiOiJjcDI4a2VpdG5uMGdqOHQ1MmMxZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjcDI3ZzU0dWR1NjVqM2JkazlwZyIsInNwYWNlX2lkIjoiY3AyN2c1NHVkdTY1ajNiZGs5bGciLCJhYnN0cmFjdF91c2VyX2lkIjoiY3AyN2c1NHVkdTY1ajNiZGs5bDAifQ.ToLbJbZa7wYZaSgqLUUQOzMQUhcKKsH3yP5nlykCvCoYK0SH8C8VQWkTUS7D-4mhDps8kUPLEwUnfzLjNOcARg"
TOKEN_UNK = ('eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMzEzNDc5NiwiaWF0IjoxNzE1MzU4Nzk2LC'
        'JqdGkiOiJjb3Y0b2oydms2Z2ZpNHJobjlnMCIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbWZvNHJlY3A3ZmZuYzR2dXQwMCIsInNwYWNlX2lk'
        'IjoiY21mbzRyZWNwN2ZmbmM0dnVzdmciLCJhYnN0cmFjdF91c2VyX2lkIjoiY21mbzRyZWNwN2ZmbmM0dnV0MDAifQ.rZQvnlZtPzYMXwlL1-a'
        'eTZ9oED81ciASCwksdN5ui80Ryb7zqvRn6ffos5Nx8QCce19OND02zXJz37-6AWNfag')


TOKEN_YSZ = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyNjk5ODU3NCwiaWF0IjoxNzE5MjIyNTc0LCJqdGkiOiJjcHNrMmJocDJrMTIycjY4Mm9wZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjcDA1cWtxdG5uMHF0MzI3M29xMCIsInNwYWNlX2lkIjoiY3AwNXFrcXRubjBxdDMyNzNvcGciLCJhYnN0cmFjdF91c2VyX2lkIjoiY3AwNXFrcXRubjBxdDMyNzNvcDAifQ.YEXmBLjBQkq__s81s_Zvc_PGB_r4WBuvoMWI1AfPMlCJ__WHJsqdDb9drn47GHBaeqbTabvdW8l-J3zy58UYxg"


TOKEN_HEADERS = {'Content-Type': 'application/json','Authorization': f"Bearer {TOKEN_CZY}"}


TOKEN_POOL = [TOKEN_CZY, TOKEN_UNK]


def get_valid_headers():
        token = choices(TOKEN_POOL, k=1)[0]
        return {'Content-Type': 'application/json','Authorization': f"Bearer {token}"}


