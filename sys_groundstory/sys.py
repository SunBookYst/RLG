import RLG.Request.Request as req

with open('sys_prompt.txt') as f:
    sys_prompt=f.read()
response=req.get_request_kimi(None,sys_prompt)
id,content=req.read_answer(response)