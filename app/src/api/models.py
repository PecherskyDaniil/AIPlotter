from pydantic import BaseModel


class TextPrompt(BaseModel):
    prompt:str

class Response(BaseModel):
    success:bool
    message:str
    result:dict
